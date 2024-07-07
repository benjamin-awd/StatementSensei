# pylint: disable=line-too-long
from importlib.metadata import version

import pybadges
import streamlit as st

from webapp.helpers import switch_page

st.markdown("# About")

app_version = version("statement_sensei")

app_version_badge = pybadges.badge(
    left_text="app",
    right_text=f"v{app_version}",
    left_color="#555",
    right_color="#007ec6",
)

st.image(app_version_badge)

st.markdown(
    """Currently supported banks:
| Bank                | Credit Statement    | Debit Statement     |
| --------------------| --------------------| --------------------|
| Citibank            | ✅                 | ❌                  |
| DBS/POSB            | ✅                 | ✅                  |
| HSBC                | ✅                 | ❌                  |
| Maybank             | ✅                 | ✅                  |
| OCBC                | ✅                 | ✅                  |
| Standard Chartered  | ✅                 | ❌                  |
"""
)

st.write("\n")

st.markdown("# Usage")
switch_page_button = st.button("Convert a bank statement")
if switch_page_button:
    switch_page("app")

st.markdown(
    """
# FAQ
### Is this app secure?
StatementSensei on Streamlit takes the following security measures:
- Uploaded files are stored in memory as a byte stream, and are not saved to the disk or
uploaded to any external location besides Streamlit.
- Passwords are wrapped in Pydantic's `SecretStr` class when passed to the underlying Python code,
which masks passwords as `**********` and prevents them from appearing in any logging or tracebacks.
- Passwords are never saved anywhere, and are only used to unlock PDFs via the `authenticate()` method.
- The underlying source code focuses on transactions, and does not attempt to extract personal
identifiable information (PII) such as your name or address.

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
- Use the monopoly [CLI](https://github.com/benjamin-awd/monopoly), or the [offline](https://github.com/benjamin-awd/statementsensei/releases) version of the app
- Redact any sensitive information in transactions e.g. card numbers, names etc.
"""
)

st.markdown("# Contact")

st.markdown(
    """
    [![Github](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/benjamin-awd/monopoly)
    [![Linkedin](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/benjamindornel/)
"""
)
st.markdown(
    """If you need support or run into any bugs,
    feel free to raise an issue at https://github.com/benjamin-awd/statementsensei/issues
    or [contact me](mailto:benjamindornel@gmail.com).
    """
)
