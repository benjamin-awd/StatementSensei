from typing import TYPE_CHECKING

import pandas as pd
import plotly.graph_objs as go
import streamlit as st

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


def render_metric(column: "DeltaGenerator", title, value, title_color="#262730", value_color="#262730"):
    column.markdown(
        f"""
        <div style="text-align:center;">
            <div style="font-size:16px; color:{title_color};">{title}</div>
            <div style="font-size:36px; color:{value_color};">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_stacked_bar_chart(df: pd.DataFrame):
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
        y=[-expense for expense in df["Expenses"]],
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
        line={"color": "black", "width": 4},
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
    chart = st.plotly_chart(fig, use_container_width=True)

    total_income = round(df["Income"].sum())
    total_expenses = round(df["Expenses"].sum())
    total_savings = round(df["amount"].sum())

    # Avoid division by zero
    savings_rate = total_savings / total_income * 100 if total_income > 0 else 0
    formatted_savings_rate = f"{savings_rate:.2f}%"
    formatted_total_savings = f"${total_savings:,.0f}"
    formatted_total_savings = f"-${abs(total_savings):,}" if total_savings < 0 else f"${total_savings:,}"

    col1, col2, col3, col4 = st.columns(4)

    if chart:
        render_metric(col1, "Income", f"${total_income:,}", value_color="#00CEAA")
        render_metric(col2, "Expenses", f"${total_expenses:,}", value_color="#F63366")
        render_metric(col3, "Total Savings", formatted_total_savings)
        render_metric(col4, "Savings Rate", formatted_savings_rate)


st.markdown("# Visualizations")

if "df" in st.session_state:
    df: pd.DataFrame = st.session_state["df"].copy()
    df.index = pd.to_datetime(df["date"])
    df["Bank"] = df["bank"]
    df["Income"] = df["amount"].apply(lambda x: max(0, x))
    df["Expenses"] = df["amount"].apply(lambda x: abs(x) if x < 0 else 0)
    df = df.drop(columns=["description", "date"])
    df = df.resample("MS").sum()

    show_stacked_bar_chart(df)

if "df" not in st.session_state:
    switch_page_button = st.button("Convert a bank statement")
    if switch_page_button:
        st.switch_page("app.py")
