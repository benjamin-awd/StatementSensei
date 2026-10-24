import pandas as pd
import plotly.graph_objs as go
import streamlit as st


def show_stacked_bar_chart(df: pd.DataFrame):
    # the savings line needs to contrast with the page background
    savings_color = "white" if st.context.theme.type == "dark" else "black"

    income_trace = go.Bar(
        x=df.index,
        y=df["Income"],
        name="Income",
        marker={"color": "#00CEAA", "cornerradius": 10},
        hovertext=[f"${s:,.2f}" for s in df["Income"]],
        hoverinfo="text+name",
        offsetgroup=0,
    )

    expenses_trace = go.Bar(
        x=df.index,
        y=-df["Expenses"],
        name="Expenses",
        marker={"color": "#F63366", "cornerradius": 10},
        hovertext=[f"${s:,.2f}" for s in df["Expenses"]],
        hoverinfo="text+name",
        offsetgroup=0,
    )

    savings_trace = go.Scatter(
        x=df.index,
        y=df["Income"] - df["Expenses"],
        name="Savings",
        mode="lines",
        line={"color": savings_color, "width": 4},
        hoverinfo="text+name",
        text=[f"${s:,.2f}" for s in df["amount"]],
    )

    layout = go.Layout(
        title="Cash Flow",
        title_font={"size": 26},
        xaxis={"title": "Month", "showgrid": False, "dtick": "M1"},
        yaxis={
            "title": "Amount",
            "showgrid": False,
            "zeroline": True,
            "zerolinecolor": "#EFEFEF",
            "zerolinewidth": 2,
            "tickformat": "$,.1s",
        },
        barmode="relative",
        hovermode="x unified",
        bargap=0.5,
        showlegend=False,
    )

    fig = go.Figure(data=[income_trace, expenses_trace, savings_trace], layout=layout)
    st.plotly_chart(fig)

    total_income = round(df["Income"].sum())
    total_expenses = round(df["Expenses"].sum())
    total_savings = round(df["amount"].sum())

    # Avoid division by zero
    savings_rate = total_savings / total_income * 100 if total_income > 0 else 0
    formatted_total_savings = f"-${abs(total_savings):,}" if total_savings < 0 else f"${total_savings:,}"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Income", f"${total_income:,}", border=True)
    col2.metric("Expenses", f"${total_expenses:,}", border=True)
    col3.metric("Total Savings", formatted_total_savings, border=True)
    col4.metric("Savings Rate", f"{savings_rate:.2f}%", border=True)


st.markdown("# Visualizations")

if "df" in st.session_state:
    df: pd.DataFrame = st.session_state["df"].copy()
    df.index = pd.to_datetime(df["date"])
    df["Income"] = df["amount"].clip(lower=0)
    df["Expenses"] = df["amount"].clip(upper=0).abs()
    df = df[["amount", "Income", "Expenses"]].resample("MS").sum()

    show_stacked_bar_chart(df)
else:
    st.page_link("app.py", label="Convert a bank statement", icon=":material/arrow_forward:")
