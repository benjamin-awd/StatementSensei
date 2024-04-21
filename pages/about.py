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
