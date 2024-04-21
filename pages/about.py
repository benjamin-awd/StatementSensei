import streamlit as st
from streamlit_extras.switch_page_button import switch_page 

st.markdown("# About")

st.markdown("""
Monopoly is a Python library that converts Singapore bank statement PDFs to CSV using pdftotext.
            
I started this project because I got tired of having to manually extract my transactions from 
poorly formatted PDF bank statements.
""")
 
st.markdown("""Currently supported banks:
| Bank                | Credit Statement    | Debit Statement     |
| --------------------| --------------------| --------------------|
| Citibank            | :white_check_mark:  | :x:                 |
| DBS                 | :white_check_mark:  | :white_check_mark:  |
| HSBC                | :white_check_mark:  | :x:                 |
| OCBC                | :white_check_mark:  | :white_check_mark:  |
| Standard Chartered  | :white_check_mark:  | :x:                 |
""")

st.write("\n")

st.markdown("# Usage")
switch_page_button = st.button("Convert a bank statement")
if switch_page_button:
    switch_page("app")

st.markdown("# Contact")
st.markdown("""
    [![Github](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/benjamin-awd/monopoly)
    [![Linkedin](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/benjamindornel/)
""")
st.markdown("If you need support for a bank/statement type or run into any bugs, feel free to [contact me](mailto:benjamindornel@gmail.com).")

st.markdown("""
# FAQ
### Is this app secure?
Monopoly on Streamlit takes the following security measures:
- Uploaded files are stored in memory as a byte stream, and are not saved to the disk or uploaded to any external location besides Streamlit.
- Passwords are wrapped in Pydantic's `SecretStr` class when passed to the underlying Python code, which masks passwords as `**********` and prevents them from appearing in any logging or tracebacks. 
- Passwords are never saved anywhere, and are only used to unlock PDFs via the `authenticate()` method.
- The underlying source code focuses on transactions, and does not attempt to extract personal identifiable information (PII) such as your name or address.

### Is Streamlit secure?
When a file is uploaded via Streamlit, the data is copied to the Streamlit backend via the browser, 
and contained in a BytesIO buffer in Python memory (i.e. RAM, not disk).
            
As files are stored in memory, they get deleted immediately as soon as they're not needed anymore.

This means Streamlit removes a file from memory when:
- The user uploads another file, replacing the original one
- The user clears the file uploader
- The user closes the browser tab where they uploaded the file

Streamlit is
**[SOC 2 Type 1 compliant](https://blog.streamlit.io/streamlit-cloud-is-now-soc-2-type-1-compliant/)**,
which means it was audited and found to have appropriate systems in place to ensure the security of 
the system (protecting against unauthorized access) and the confidentiality of the information processed 
by the system (ensuring that sensitive data is accessed only by authorized individuals) 
at a specific point in time.
            
### How can I achieve a better security posture as a user?
Despite all the security measures listed above, uploading sensitive data to the internet always comes with a risk. 
            
With that in mind, here are some measures for a better security posture:
- Use the [offline](https://github.com/benjamin-awd/monopoly) version of Monopoly
- Redact any sensitive information in transactions e.g. card numbers, names etc.
- Change the default password of your bank statement PDFs (i.e. not NRIC/DOB)
"""
)
