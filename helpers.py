import streamlit as st
from fitz import Document
from monopoly.processors import detect_processor
from pydantic import SecretStr
from st_aggrid import AgGrid, GridOptionsBuilder


def parse_bank_statement(document: Document, password: str = None) -> None:
    processor = detect_processor(
        file_bytes=document.tobytes(), passwords=[SecretStr(password)]
    )
    statement = processor.extract()
    df = processor.transform(statement)
    total_balance = df["amount"].sum()

    # cosmetic changes
    df.columns = ["Transaction Date", "Description", "Amount (SGD)"]
    st.dataframe(df, use_container_width=True, hide_index=True)
    groupby = st.checkbox("Group by date", False)

    gb = GridOptionsBuilder()
    gb.configure_default_column(
        resizable=True,
        filterable=True,
        sortable=True,
        editable=False,
    )
    gb.configure_column(
        field="Transaction Date",
        header_name="Transaction Date",
        flex=1,
        rowGroup=groupby,
        enableRowGroup=groupby,
        hide=groupby,
    )
    gb.configure_column(field="Description", header_name="Description", flex=1)
    gb.configure_column(
        field="Amount (SGD)", header_name="Amount (SGD)", flex=1, type=["numericColumn"]
    )

    csv = df.to_csv(index=False).encode("utf-8")
    grid_options = gb.build()
    gb.configure_grid_options(groupDefaultExpanded=1, grandTotalRow="bottom")

    AgGrid(df, gridOptions=grid_options, height=400)
    st.write(f"Total Balance: ${total_balance:.2f}")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{document.pdf_file_name.split('.')[0]}.csv",
        mime="text/csv",
    )
