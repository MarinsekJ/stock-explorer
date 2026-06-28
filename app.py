import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Stock Explorer",
    page_icon="",
    layout="wide",
)

st.title(" Stock Price Explorer")
st.caption(
    "This app uses Plotly's built-in normalized historical sample dataset. "
    "It is for comparison and learning only, not live market data or investment advice."
)

@st.cache_data
def load_data():
    """Load Plotly's built-in normalized stock dataset."""
    df = px.data.stocks()
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()
tickers = [column for column in df.columns if column != "date"]

chosen = st.sidebar.multiselect(
    "Choose stocks",
    tickers,
    default=["AAPL", "MSFT", "GOOG"],
)

if not chosen:
    st.warning("Pick at least one stock from the sidebar.")
    st.stop()

growth_data = pd.DataFrame(
    {
        "Stock": chosen,
        "Final value": [df[ticker].iloc[-1] for ticker in chosen],
    }
)
growth_data["Total growth"] = (growth_data["Final value"] - 1) * 100
best_performer = growth_data.loc[growth_data["Total growth"].idxmax()]

st.info(
    "Values are indexed to 1.00 at the start of the sample period, so each "
    "line shows relative growth since January 2018. These are normalized "
    "sample prices, not real-time quotes."
)

st.info(
    "Did you know? Apple introduced the original iPhone on January 9, 2007, "
    "as a combination of a mobile phone, a widescreen iPod, and an Internet "
    "communications device."
)
st.caption(
    "Source: Apple Newsroom, \"Apple Reinvents the Phone with iPhone\" "
    "(January 9, 2007)."
)

cols = st.columns(len(chosen))

for col, ticker in zip(cols, chosen):
    stock_growth = growth_data.loc[growth_data["Stock"] == ticker].iloc[0]
    col.metric(
        ticker,
        f"{stock_growth['Final value']:.2f}x",
        f"{stock_growth['Total growth']:+.1f}%",
    )

st.subheader("Best performer")
best_col, detail_col = st.columns([1, 2])
best_col.metric(
    "Top selected stock",
    best_performer["Stock"],
    f"{best_performer['Total growth']:+.1f}%",
)
detail_col.write(
    f"{best_performer['Stock']} had the highest total growth among the "
    "currently selected stocks in this normalized sample. A final value of "
    f"{best_performer['Final value']:.2f}x means the sample ended at "
    f"{best_performer['Final value']:.2f} times its starting index value."
)

fig = px.line(
    df,
    x="date",
    y=chosen,
    title="Normalized price over time",
)

st.plotly_chart(fig, use_container_width=True)

bar_fig = px.bar(
    growth_data.sort_values("Total growth", ascending=False),
    x="Stock",
    y="Total growth",
    text="Total growth",
    title="Total percentage growth by selected stock",
    labels={"Total growth": "Total growth (%)"},
)
bar_fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
bar_fig.update_layout(yaxis_ticksuffix="%", uniformtext_minsize=10)

st.plotly_chart(bar_fig, use_container_width=True)

st.subheader("What if I invested?")
calc_col, result_col = st.columns([1, 2])

with calc_col:
    investment_stock = st.selectbox(
        "Choose a stock for the calculator",
        chosen,
    )
    initial_investment = st.number_input(
        "Initial investment amount",
        min_value=0.0,
        value=1000.0,
        step=100.0,
        format="%.2f",
    )

selected_final_value = growth_data.loc[
    growth_data["Stock"] == investment_stock,
    "Final value",
].iloc[0]
estimated_value = initial_investment * selected_final_value
estimated_gain = estimated_value - initial_investment

with result_col:
    st.metric(
        "Estimated ending value",
        f"${estimated_value:,.2f}",
        f"${estimated_gain:,.2f}",
    )
    st.write(
        f"This estimate multiplies the entered amount by "
        f"{investment_stock}'s normalized sample growth factor of "
        f"{selected_final_value:.2f}x. It does not account for live prices, "
        "dividends, taxes, fees, inflation, or timing of real trades."
    )
