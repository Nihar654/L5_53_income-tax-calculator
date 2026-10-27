# Static Code Analysis Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without requiring the program
to be executed. It helps identify potential security vulnerabilities,
code-quality problems, and style violations early in development. In
this lab, the tools provided complementary checks: Pylint focused on
code quality and maintainability, Bandit highlighted risky security
patterns, and Flake8 checked formatting and PEP 8 compliance. Using all
three gave a more complete view than relying on only one tool.

## 2. What did you learn from Pylint, Bandit, and Flake8?

I learned that each tool serves a different purpose. Pylint identified
problems such as missing docstrings, non-standard naming, unused
variables, and unnecessary code patterns. Bandit highlighted security
concerns in the original implementation, including AES-ECB usage, a
1024-bit RSA key, and unsafe XML parsing. Flake8 helped catch formatting
issues, including the missing newline at the end of the file. Together,
the tools made it easier to identify and verify fixes systematically.

## 3. Which issues were most important, and why?

The security findings were the highest priority because insecure
cryptography and unsafe parsing can put sensitive information and
application behavior at risk. I replaced AES-ECB with AES-GCM using a
random nonce, increased the RSA key size to 2048 bits, and switched XML
parsing to `defusedxml.ElementTree`. I also tightened PAN validation to
check the entire input and added checks for required Form 16 fields.
These changes address both security risks and input-validation
robustness.

## 4. How did static analysis improve the code's quality and maintainability?

The analysis process encouraged consistent naming, useful docstrings,
removal of unused code, and clearer formatting. The resulting code is
easier to read and maintain, and the checks provide repeatable evidence
that common issues have been addressed. After the fixes, Pylint reached
10.00/10, Bandit reported no issues, and Flake8 produced no violations.
Static analysis does not prove that a program is completely correct or
secure, so runtime testing and careful review are still necessary.
