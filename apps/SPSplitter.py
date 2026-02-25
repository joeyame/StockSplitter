import marimo

__generated_with = "0.13.6"
app = marimo.App(width="columns", layout_file="layouts/SPSplitter.grid.json")


@app.cell(column=0)
def _():
    import marimo as mo
    import requests
    import bs4
    import pandas as pd
    from io import StringIO
    import openpyxl
    return mo, pd, requests


@app.cell
def _(requests):
    url = "https://www.slickcharts.com/sp500"

    request = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE, OPTIONS",
            "Access-Control-Max-Age": "1000",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
            "Origin": "https://www.slickcharts.com",
        },
    )
    return


@app.cell
def _(get_num_stocks, invest_amount, spData):
    trimmed_stocks = spData.iloc[0 : get_num_stocks()]
    total_weight = trimmed_stocks["Weight"].sum()
    trimmed_stocks.loc[:, "Weight"] = trimmed_stocks["Weight"] / total_weight
    trimmed_stocks = trimmed_stocks.assign(
        InvestmentAmount=trimmed_stocks["Weight"] * invest_amount.value
    )
    return (trimmed_stocks,)


@app.cell
def _(pd):
    # Grab current S&P Holdings by Weight
    spData = pd.read_excel(
        "https://www.ssga.com/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx",
        skiprows=4,
        converters={"Weight": lambda x: float(x) / 100},
    ).dropna(subset=["Weight"])
    return (spData,)


@app.cell(column=1)
def _():
    # This column is for UI elements
    return


@app.cell
def _(mo):
    get_num_stocks, set_num_stocks = mo.state(50)
    return get_num_stocks, set_num_stocks


@app.cell
def _(get_num_stocks, mo, set_num_stocks):
    # Number of stocks state

    num_stocks = mo.ui.slider(
        1, 500, value=get_num_stocks(), on_change=set_num_stocks, full_width=True
    )
    return (num_stocks,)


@app.cell
def _(get_num_stocks, mo, set_num_stocks):
    num_stocks_text = mo.ui.number(
        1,
        500,
        value=get_num_stocks(),
        on_change=set_num_stocks,
        full_width=True,
        label="Number of Stocks",
    )
    return (num_stocks_text,)


@app.cell
def _(mo, num_stocks, num_stocks_text):
    stock_picker = mo.hstack(
        [
            mo.md("Number of Stocks"),
            mo.vstack(
                [num_stocks, num_stocks_text],
            ),
        ],
        align="center",
    )
    return


@app.cell
def _(mo):
    invest_amount = mo.ui.number(
        0, value=10.00, full_width=True, label="Investment Amount ($)"
    )
    return (invest_amount,)


@app.cell
def _(invest_amount, mo, num_stocks_text):
    mo.sidebar(mo.vstack([invest_amount, num_stocks_text], gap=0, heights=[0, 0]))
    return


@app.cell
def _(mo, trimmed_stocks):
    cards = []
    for i, row in trimmed_stocks.iterrows():
        symbol = row.Ticker
        card = mo.stat(
            label=symbol,
            value=f"${row.InvestmentAmount:.2f}",
            caption="To purchase",
            bordered=True,
        )
        cards.append(card)
    mo.hstack(cards, wrap=True, align="center", justify="center")
    return


if __name__ == "__main__":
    app.run()
