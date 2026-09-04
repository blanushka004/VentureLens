import streamlit as st


def format_currency(value):
    """
    Format numeric values as USD.
    """

    if value is None:
        return "$0"

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"

    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"

    elif abs(value) >= 1_000:
        return f"${value / 1_000:.2f}K"

    return f"${value:,.2f}"


def format_number(value):
    """
    Format large numeric values.
    """

    if value is None:
        return "0"

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def render_metric(
    label,
    value,
    delta=None,
    help_text=None
):
    """
    Render a single Streamlit metric card.
    """

    st.metric(
        label=label,
        value=value,
        delta=delta,
        help=help_text
    )


def render_metrics_row(metrics):
    """
    Render multiple metrics in a responsive row.

    Expected format:

    metrics = [
        {
            "label": "Total Startups",
            "value": "180",
            "delta": "+12%"
        }
    ]
    """

    if not metrics:
        return

    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):

        with column:

            st.metric(
                label=metric.get(
                    "label",
                    ""
                ),

                value=metric.get(
                    "value",
                    "0"
                ),

                delta=metric.get(
                    "delta",
                    None
                ),

                help=metric.get(
                    "help",
                    None
                )
            )


def render_funding_metrics(
    total_funding,
    total_startups,
    total_investors,
    total_rounds
):
    """
    Render standard VentureLens executive metrics.
    """

    metrics = [

        {
            "label": "💰 Total Funding",
            "value": format_currency(
                total_funding
            ),
            "help": "Total recorded startup funding"
        },

        {
            "label": "🚀 Startups",
            "value": format_number(
                total_startups
            ),
            "help": "Total tracked startups"
        },

        {
            "label": "🏦 Investors",
            "value": format_number(
                total_investors
            ),
            "help": "Total tracked investors"
        },

        {
            "label": "📈 Funding Rounds",
            "value": format_number(
                total_rounds
            ),
            "help": "Total recorded funding rounds"
        }
    ]

    render_metrics_row(metrics)


def render_forecast_metrics(
    latest_funding,
    forecast_funding,
    projected_change,
    forecast_year
):
    """
    Render funding forecast metrics.
    """

    metrics = [

        {
            "label": "Latest Funding",
            "value": format_currency(
                latest_funding
            )
        },

        {
            "label": f"Forecast {forecast_year}",
            "value": format_currency(
                forecast_funding
            )
        },

        {
            "label": "Projected Change",
            "value": f"{projected_change:.2f}%"
        }
    ]

    render_metrics_row(metrics)
