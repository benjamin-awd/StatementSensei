# pylint: disable=line-too-long
import base64
from html import escape
from importlib.metadata import version

import streamlit as st

from webapp.constants import SUPPORTED_BANKS

st.markdown("# About")


def _text_width(text: str) -> int:
    # rough Verdana 11px advance; textLength below stretches the glyphs to fit exactly
    return round(sum(4.0 if c in "ilj.:,;|!'" else 7.5 if c.isupper() or c in "mw" else 6.5 for c in text)) + 10


def badge_svg(left: str, right: str, left_color: str, right_color: str) -> str:
    """Flat two-part badge in the shields.io style."""
    lw, rw = _text_width(left), _text_width(right)
    w = lw + rw
    left, right = escape(left), escape(right)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" role="img" aria-label="{left}: {right}">
<linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient>
<clipPath id="r"><rect width="{w}" height="20" rx="3" fill="#fff"/></clipPath>
<g clip-path="url(#r)"><rect width="{lw}" height="20" fill="{left_color}"/><rect x="{lw}" width="{rw}" height="20" fill="{right_color}"/><rect width="{w}" height="20" fill="url(#s)"/></g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
<text x="{lw / 2}" y="15" fill="#010101" fill-opacity=".3" textLength="{lw - 10}">{left}</text><text x="{lw / 2}" y="14" textLength="{lw - 10}">{left}</text>
<text x="{lw + rw / 2}" y="15" fill="#010101" fill-opacity=".3" textLength="{rw - 10}">{right}</text><text x="{lw + rw / 2}" y="14" textLength="{rw - 10}">{right}</text>
</g></svg>"""


def badge_link(label: str, ver: str, url: str, color: str) -> str:
    """Render a linked badge; the alt text carries the version, which the smoke test reads."""
    svg = badge_svg(label, f"v{ver}", "#555", color)
    uri = f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"
    return f"[![{label} v{ver}]({uri})]({url})"


st.markdown(
    badge_link(
        "StatementSensei", version("statement_sensei"), "https://github.com/benjamin-awd/statementsensei", "#2ea44f"
    )
    + "&nbsp;&nbsp;&nbsp;"
    + badge_link("monopoly", version("monopoly-core"), "https://github.com/benjamin-awd/monopoly", "#007ec6")
)

faq_tab, banks_tab, contact_tab = st.tabs(["FAQ", "Supported banks", "Contact"])

with faq_tab:
    st.markdown(
        """
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

    ### What is monopoly?
    StatementSensei is a web interface for [monopoly](https://github.com/benjamin-awd/monopoly),
    an open-source Python library and CLI that does the actual PDF parsing.
    If you'd rather not upload statements anywhere, you can run monopoly locally.
    """
    )

with banks_tab:
    st.markdown(SUPPORTED_BANKS)

with contact_tab:
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
