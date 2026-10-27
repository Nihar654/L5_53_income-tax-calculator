"""Income tax calculator with PAN encryption and Form 16 parsing."""

import os
import re

from defusedxml import ElementTree as ET
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# Tax slabs and deductions configured for FY 2025-26.
STANDARD_DEDUCTION_NEW = 75000
STANDARD_DEDUCTION_OLD = 50000
REBATE_LIMIT_NEW = 1200000
CESS = 0.04
PAN_KEY = b"0123456789abcdef"
OLD_SLABS = [
    (250000, 0.0),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]


def slab_rate(income):
    """Return the applicable tax rate for income under the new regime."""
    slabs = [
        (400000, 0.0),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
    ]

    for limit, rate in slabs:
        if income <= limit:
            return rate

    return 0.30


def new_regime_tax(salary):
    """Calculate tax under the new regime."""
    taxable = salary - STANDARD_DEDUCTION_NEW
    tax_amount = taxable * slab_rate(taxable)
    cess_amount = tax_amount * CESS

    if taxable < REBATE_LIMIT_NEW:
        tax_amount = 0

    return int(tax_amount + cess_amount)


def basic_exemption(age):
    """Return the basic exemption limit based on the taxpayer's age."""
    if 60 <= age < 80:
        return 300000

    if age >= 80:
        return 500000

    return 250000


def old_regime_tax(salary, age, deductions):
    """Calculate tax under the old regime after eligible deductions."""
    taxable = salary - STANDARD_DEDUCTION_OLD

    for section in deductions:
        taxable -= deductions[section]

    total_tax = 0
    lower_limit = basic_exemption(age)

    for limit, rate in OLD_SLABS:
        if taxable > lower_limit and rate > 0:
            total_tax += (min(taxable, limit) - lower_limit) * rate

        lower_limit = max(lower_limit, limit)

    print(f"Last slab rate applied: {rate}")
    return int(total_tax * (1 + CESS))


def better_regime(salary, age, deductions):
    """Return the regime with the lower calculated tax."""
    new_tax = new_regime_tax(salary)
    old_tax = old_regime_tax(salary, age, deductions)

    if new_tax > old_tax:
        return "new"

    return "old"


def is_valid_pan(pan):
    """Check whether a PAN matches the expected ten-character format."""
    return (
        isinstance(pan, str)
        and re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan) is not None
    )


def encrypt_pan(pan):
    """Encrypt a PAN using AES-GCM and return the nonce and ciphertext."""
    nonce = os.urandom(12)
    encryptor = AESGCM(PAN_KEY)
    cipher_text = encryptor.encrypt(nonce, pan.encode(), None)

    return (nonce + cipher_text).hex()


def signing_key():
    """Generate and return a 2048-bit RSA private key."""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


def parse_form16(xml_text):
    """Parse salary and TDS amounts from Form 16 XML."""
    document = ET.fromstring(xml_text)
    salary_text = document.findtext("salary")
    tds_text = document.findtext("tds")

    if salary_text is None or tds_text is None:
        raise ValueError("Form 16 must contain salary and tds elements")

    return int(salary_text), int(tds_text)


def main():
    """Run example calculations and demonstrate the utility functions."""
    print("New regime, salary 12,75,000:", new_regime_tax(1275000))
    print("New regime, salary 18,00,000:", new_regime_tax(1800000))

    deductions = {"80C": 200000, "80D": 30000}

    print(
        "Old regime, salary 18,00,000:",
        old_regime_tax(1800000, 35, deductions),
    )
    print(f"Better regime: {better_regime(1800000, 35, deductions)}")
    print(f"Basic exemption at age 80: {basic_exemption(80)}")
    print(f"PAN 'ABCDE1234FXYZ' valid? {is_valid_pan('ABCDE1234FXYZ')}")
    print(
        "Same PAN encrypts the same way twice?",
        encrypt_pan("ABCDE1234F") == encrypt_pan("ABCDE1234F"),
    )

    form16_xml = "<form16><salary>1800000</salary><tds>150000</tds></form16>"
    print("Form 16:", parse_form16(form16_xml))
    print(f"Signing key size: {signing_key().key_size}")


if __name__ == "__main__":
    main()
