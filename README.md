# Stock Explorer

`Stock Explorer` is a small Streamlit app for comparing normalized stock performance using Plotly's built-in sample dataset. It lets you select stocks, review relative growth, compare top performers, and estimate how a hypothetical investment would have changed over the sample period.

## Features

- Multi-select stock comparison from the sidebar
- KPI cards for selected stocks
- Best-performer summary
- Line chart for normalized price movement
- Bar chart for total percentage growth
- Simple investment outcome calculator

## Architecture

```mermaid
flowchart LR
    U[User] --> SB[Streamlit Sidebar Controls]
    SB --> APP[app.py]

    APP --> LD[load_data()]
    LD --> PX[Plotly Sample Dataset<br/>px.data.stocks()]
    LD --> DF[Pandas DataFrame]

    DF --> GM[Growth Metrics]
    DF --> LC[Line Chart]
    GM --> KPIs[Metric Cards]
    GM --> BP[Best Performer]
    GM --> BC[Bar Chart]
    GM --> IC[Investment Calculator]

    APP --> UI[Streamlit UI]
    KPIs --> UI
    BP --> UI
    LC --> UI
    BC --> UI
    IC --> UI
    UI --> U
```

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

## Notes

- The app uses Plotly's normalized sample stock dataset, not live market data.
- Values are indexed to `1.00` at the start of the sample period, so the charts show relative growth rather than raw prices.
