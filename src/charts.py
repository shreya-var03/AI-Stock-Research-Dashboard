import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_price_chart(data, symbol, support=None, resistance=None, chart_type="Candlestick"):
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25],
    )

    if chart_type == "Candlestick":
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="Price",
                increasing_line_color="#14b8a6",
                decreasing_line_color="#ef4444",
            ),
            row=1,
            col=1,
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Price",
                line=dict(color="#2563eb", width=2),
            ),
            row=1,
            col=1,
        )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["DMA_50"],
            mode="lines",
            name="50 DMA",
            line=dict(color="#22c55e", width=2),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["DMA_200"],
            mode="lines",
            name="200 DMA",
            line=dict(color="#ef4444", width=2),
        ),
        row=1,
        col=1,
    )

    volume_colors = [
        "#04A376" if close >= open_price else "#ef3030"
        for close, open_price in zip(data["Close"], data["Open"])
    ]

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume",
            marker_color=volume_colors,
            opacity=0.9,
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Avg_Volume_20"],
            mode="lines",
            name="20D Avg Volume",
            line=dict(color="#f59e0b", width=2),
        ),
        row=2,
        col=1,
    )

    if support is not None:
        fig.add_hline(
            y=support,
            line_dash="dash",
            line_color="green",
            annotation_text="Support",
            row=1,
            col=1,
        )

    if resistance is not None:
        fig.add_hline(
            y=resistance,
            line_dash="dash",
            line_color="red",
            annotation_text="Resistance",
            row=1,
            col=1,
        )

    fig.update_layout(
        title=f"{symbol} Price + Volume Chart",
        height=760,
        template="plotly_white",
        hovermode="x unified",
        dragmode="pan",
        xaxis_rangeslider_visible=False,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=40, r=30, t=80, b=40),
    )

    fig.update_yaxes(title_text="Price", row=1, col=1, fixedrange=False)
    fig.update_yaxes(title_text="Volume", row=2, col=1, fixedrange=False)
    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)

    return fig