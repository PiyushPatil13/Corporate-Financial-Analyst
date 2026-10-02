import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go


def render_market():

    st.title("Live Market")
    st.caption("Market data and historical price analysis")

    st.subheader("Select Stock")

    col1, col2 = st.columns([3, 1])

    with col1:
        ticker_symbol = st.text_input(
            "Enter NSE ticker",
            value="SUNPHARMA.NS",
            placeholder="Example: RELIANCE.NS"
        ).upper().strip()

    with col2:
        period = st.selectbox(
            "Period",
            ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y", "MAX"],
            index=5
        )

    # yfinance period mapping
    period_map = {
        "1D": "1d",
        "5D": "5d",
        "1M": "1mo",
        "3M": "3mo",
        "6M": "6mo",
        "1Y": "1y",
        "5Y": "5y",
        "MAX": "max"
    }
    try:

        stock = yf.Ticker(ticker_symbol)

        data = stock.history(
            period=period_map[period],
            interval="1d",
            auto_adjust=False
        )

        if data.empty:
            st.error(
                "No market data found. Check the ticker symbol."
            )
            return

    except Exception as e:

        st.error(f"Unable to fetch market data: {e}")
        return

    latest = data.iloc[-1]

    current_price = latest["Close"]
    open_price = latest["Open"]
    high_price = latest["High"]
    low_price = latest["Low"]
    volume = latest["Volume"]

    if len(data) > 1:

        previous_close = data["Close"].iloc[-2]

        price_change = current_price - previous_close

        percentage_change = (
            price_change / previous_close
        ) * 100

    else:

        previous_close = current_price
        price_change = 0
        percentage_change = 0

    # Moving averages
    data["MA_52"] = data["Close"].rolling(
        window=52
    ).mean()

    data["MA_200"] = data["Close"].rolling(
        window=200
    ).mean()

    # Historical statistics
    period_high = data["High"].max()
    period_low = data["Low"].min()

    average_price = data["Close"].mean()

    average_volume = data["Volume"].mean()

    # 52-week statistics
    year_data = stock.history(
        period="1y",
        interval="1d",
        auto_adjust=False
    )

    if not year_data.empty:

        week_52_high = year_data["High"].max()
        week_52_low = year_data["Low"].min()

    else:

        week_52_high = period_high
        week_52_low = period_low

    st.subheader(ticker_symbol)

    price_col, change_col = st.columns([2, 1])

    with price_col:

        st.metric(
            "Current Price",
            f"₹{current_price:,.2f}"
        )

    with change_col:

        st.metric(
            "Change",
            f"{price_change:+.2f}",
            f"{percentage_change:+.2f}%"
        )

    st.subheader("Market Data")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Open",
            f"₹{open_price:,.2f}"
        )

    with col2:
        st.metric(
            "High",
            f"₹{high_price:,.2f}"
        )

    with col3:
        st.metric(
            "Low",
            f"₹{low_price:,.2f}"
        )

    with col4:
        st.metric(
            "Previous Close",
            f"₹{previous_close:,.2f}"
        )

    with col5:
        st.metric(
            "Volume",
            f"{volume:,.0f}"
        )

    st.subheader("Price Performance")

    chart_col, indicator_col = st.columns([2, 2])

    with chart_col:

        chart_type = st.radio(
            "Chart Type",
            [
                "Candlestick",
                "Line",
                "Area"
            ],
            horizontal=True
        )

    with indicator_col:

        indicators = st.multiselect(
            "Indicators",
            [
                "52-Day Moving Average",
                "200-Day Moving Average",
                "Volume"
            ],
            default=[
                "52-Day Moving Average"
            ]
        )

    fig = go.Figure()

    if chart_type == "Candlestick":

        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="Price"
            )
        )

    elif chart_type == "Line":

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Close Price"
            )
        )

    elif chart_type == "Area":

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                fill="tozeroy",
                name="Close Price"
            )
        )


    if "52-Day Moving Average" in indicators:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA_52"],
                mode="lines",
                name="52-Day MA"
            )
        )

    if "200-Day Moving Average" in indicators:

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["MA_200"],
                mode="lines",
                name="200-Day MA"
            )
        )

    fig.update_layout(

        height=600,

        xaxis_title="Date",

        yaxis_title="Price (₹)",

        xaxis_rangeslider_visible=False,

        hovermode="x unified",

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    if "Volume" in indicators:

        st.subheader("Trading Volume")

        volume_fig = go.Figure()

        volume_fig.add_trace(
            go.Bar(
                x=data.index,
                y=data["Volume"],
                name="Volume"
            )
        )

        volume_fig.update_layout(
            height=250,
            xaxis_title="Date",
            yaxis_title="Volume",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            volume_fig,
            use_container_width=True
        )


    st.subheader("Historical Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            f"{period} High",
            f"₹{period_high:,.2f}"
        )

    with col2:

        st.metric(
            f"{period} Low",
            f"₹{period_low:,.2f}"
        )

    with col3:

        st.metric(
            "Average Price",
            f"₹{average_price:,.2f}"
        )

    with col4:

        st.metric(
            "Average Volume",
            f"{average_volume:,.0f}"
        )

    st.subheader("52-Week Range")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "52-Week High",
            f"₹{week_52_high:,.2f}"
        )

    with col2:

        st.metric(
            "52-Week Low",
            f"₹{week_52_low:,.2f}"
        )

    with col3:

        if not pd.isna(data["MA_52"].iloc[-1]):

            st.metric(
                "52-Day Moving Average",
                f"₹{data['MA_52'].iloc[-1]:,.2f}"
            )

        else:

            st.metric(
                "52-Day Moving Average",
                "Not enough data"
            )