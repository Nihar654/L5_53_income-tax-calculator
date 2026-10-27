# Static Code Analysis Issue Table

Repository: `L5_53_income-tax-calculator`\
File analyzed: `tax_calculator.py`

  ----------------------------------------------------------------------------------------------------------
  Issue               Type              Original finding /   Fix applied
                                        risk                 
  ------------------- ----------------- -------------------- -----------------------------------------------
  Unsafe XML parsing  Security (Bandit) Parsing untrusted    Replaced `minidom` with
  with                                  XML with the         `defusedxml.ElementTree` for safer XML parsing.
  `xml.dom.minidom`                     standard DOM parser  
                                        can expose the       
                                        application to       
                                        XML-related attacks. 

  CGI handler usage   Security (Bandit) The imported and     Removed the unused `CGIHandler` import and the
                                        exposed CGI handler  `runAsCgi` function.
                                        was flagged as a     
                                        risky legacy         
                                        interface.           

  AES used in ECB     Security (Bandit) ECB does not provide Replaced AES-ECB with AES-GCM, using a fresh
  mode                                  semantic security    random 12-byte nonce for each encryption. The
                                        and can reveal       returned hexadecimal value contains the nonce
                                        patterns when        followed by the authenticated ciphertext.
                                        encrypting repeated  
                                        blocks.              

  RSA key size was    Security (Bandit) The original RSA key Increased the generated RSA private key size to
  1024 bits                             size was below the   2048 bits.
                                        recommended modern   
                                        baseline and was     
                                        flagged by Bandit.   

  PAN validation      Correctness /     The original         Used
  accepted trailing   code quality      regular-expression   `re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan)`
  characters                            check used           and checked that the input is a string.
                                        `re.match`, which    
                                        checks from the      
                                        start of a string    
                                        and could accept a   
                                        valid-looking prefix 
                                        followed by extra    
                                        characters.          

  XML fields were     Robustness        Missing `<salary>`   Added explicit checks for both elements and
  accessed without                      or `<tds>` elements  raise a clear `ValueError` when either is
  validation                            could lead to        missing.
                                        unclear failures     
                                        when parsing Form 16 
                                        data.                

  RSA key strength    Security          A 1024-bit RSA key   Updated key generation to use a 2048-bit key.
                                        is no longer an      
                                        appropriate choice   
                                        for a new            
                                        implementation.      

  Missing module and  Code quality      Pylint reported      Added a module docstring and docstrings for the
  function docstrings (Pylint)          missing              functions.
                                        documentation for    
                                        the module and       
                                        functions.           

  Non-standard        Code quality      CamelCase function   Renamed functions and variables, for example
  identifiers         (Pylint)          and variable names   `newRegimeTax` to `new_regime_tax` and
                                        did not follow the   `taxAmount` to `tax_amount`.
                                        conventional Python  
                                        `snake_case` naming  
                                        style.               

  Unused variables,   Code quality      The original code    Removed unused imports and variables, and
  imports, and        (Pylint)          included unused      removed unused parameters from the relevant
  arguments                             variables and        functions.
                                        imports, plus        
                                        parameters that were 
                                        not used.            

  Multiple statements Style (Flake8 /   The original file    Split statements onto separate lines, formatted
  on one line and     Pylint)           contained formatting expressions and function calls, and corrected
  formatting issues                     problems such as     whitespace.
                                        multiple statements  
                                        on one line and      
                                        other PEP 8          
                                        violations.          

  Missing final       Style (Flake8)    Flake8 reported      Added a newline at the end of
  newline                               `W292` because the   `tax_calculator.py`.
                                        source file did not  
                                        end with a newline.  
  ----------------------------------------------------------------------------------------------------------

## Verification

After the changes, the recorded checks were:

-   **Pylint:** 10.00/10.
-   **Bandit:** no issues identified.
-   **Flake8:** no output, indicating no reported violations.

These results should be confirmed by rerunning the tools against the
final committed version before submission.

## Notes

-   Line numbers are intentionally omitted because they can change as
    the source file is edited.
-   The PAN example `ABCDE1234FXYZ` is now rejected because it contains
    more than the required ten characters.
-   AES-GCM uses a random nonce, so encrypting the same PAN twice should
    normally produce different ciphertexts. The nonce must be stored
    with the ciphertext to decrypt it later.
