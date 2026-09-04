import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# FUNDING TREND CHART
# ============================================================

def funding_trend_chart(
    data,
    x_column="funding_year",
    y_column="total_funding",
    title="Startup Funding Trend"
):
    """
    Create a funding trend line chart.
    """

    df = pd.DataFrame(data)

    if df.empty:
        return None

    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        markers=True,
        title=title
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Funding Amount (USD)",
        hovermode="x unified"
    )

    return fig


# ============================================================
# BAR CHART
# ============================================================

def bar_chart(
    data,
    x_column,
    y_column,
    title,
    orientation="v"
):
    """
    Create a reusable bar chart.
    """

    df = pd.DataFrame(data)

    if df.empty:
        return None

    fig = px.bar(
        df,
        x=x_column,
        y=y_column,
        title=title,
        orientation=orientation
    )

    fig.update_layout(
        hovermode="closest"
    )

    return fig


# ============================================================
# HORIZONTAL BAR CHART
# ============================================================

def horizontal_bar_chart(
    data,
    category_column,
    value_column,
    title
):
    """
    Create a horizontal ranking chart.
    """

    df = pd.DataFrame(data)

    if df.empty:
        return None

    df = df.sort_values(
        by=value_column,
        ascending=True
    )

    fig = px.bar(
        df,
        x=value_column,
        y=category_column,
        orientation="h",
        title=title
    )

    fig.update_layout(
        yaxis_title="",
        xaxis_title=value_column.replace(
            "_",
            " "
        ).title()
    )

    return fig


# ============================================================
# PIE / DONUT CHART
# ============================================================

def donut_chart(
    data,
    names_column,
    values_column,
    title
):
    """
    Create a donut chart.
    """

    df = pd.DataFrame(data)

    if df.empty:
        return None

    fig = px.pie(
        df,
        names=names_column,
        values=values_column,
        title=title,
        hole=0.45
    )

    return fig


# ============================================================
# FORECAST CHART
# ============================================================

def funding_forecast_chart(
    historical_data,
    forecast_data
):
    """
    Create combined historical and forecast funding chart.
    """

    historical_df = pd.DataFrame(
        historical_data
    )

    forecast_df = pd.DataFrame(
        forecast_data
    )

    fig = go.Figure()

    # Historical funding
    if not historical_df.empty:

        fig.add_trace(
            go.Scatter(
                x=historical_df["year"],
                y=historical_df[
                    "total_funding"
                ],
                mode="lines+markers",
                name="Historical Funding"
            )
        )

    # Forecast funding
    if not forecast_df.empty:

        fig.add_trace(
            go.Scatter(
                x=forecast_df["year"],
                y=forecast_df[
                    "predicted_funding"
                ],
                mode="lines+markers",
                name="Forecast",
                line=dict(
                    dash="dash"
                )
            )
        )

    fig.update_layout(
        title="Historical Funding vs Forecast",
        xaxis_title="Year",
        yaxis_title="Funding Amount (USD)",
        hovermode="x unified"
    )

    return fig


# ============================================================
# GROUPED BAR CHART
# ============================================================

def grouped_bar_chart(
    data,
    x_column,
    y_column,
    color_column,
    title
):
    """
    Create grouped bar charts for comparative analytics.
    """

    df = pd.DataFrame(data)

    if df.empty:
        return None

    fig = px.bar(
        df,
        x=x_column,
        y=y_column,
        color=color_column,
        barmode="group",
        title=title
    )

    return fig


# ============================================================
# SCATTER CHART
# ============================================================

def scatter_chart(
    data,
    x_column,
    y_column,
    title,
    size_column=None,
    color_column=None
):
    """
    Create a scatter chart for relationship analysis.
    """

    df = pd.DataFrame(data)

    if df.empty:
        return None

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        size=size_column,
        color=color_column,
        title=title
    )

    return fig