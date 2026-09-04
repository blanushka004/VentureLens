import streamlit as st

from components.sidebar import render_sidebar

from components.metrics import (
    render_funding_metrics,
    render_forecast_metrics
)

from components.charts import (
    funding_trend_chart,
    horizontal_bar_chart,
    donut_chart,
    funding_forecast_chart
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VentureLens Component Test",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# SIDEBAR TEST
# ============================================================

filters = render_sidebar()


# ============================================================
# TITLE
# ============================================================

st.title("🧪 VentureLens Component Testing")

st.write(
    "Testing reusable sidebar, metrics, and chart components."
)


# ============================================================
# METRICS TEST
# ============================================================

st.header("1. Metrics Components")

render_funding_metrics(
    total_funding=28086243000,
    total_startups=180,
    total_investors=26,
    total_rounds=1100
)


st.divider()


# ============================================================
# FORECAST METRICS TEST
# ============================================================

st.header("2. Forecast Metrics")

render_forecast_metrics(
    latest_funding=2813215000,
    forecast_funding=3053006400,
    projected_change=8.52,
    forecast_year=2028
)


st.divider()


# ============================================================
# FUNDING TREND TEST
# ============================================================

st.header("3. Funding Trend Chart")

historical_data = [
    {
        "funding_year": 2020,
        "total_funding": 4756665000
    },
    {
        "funding_year": 2021,
        "total_funding": 6024899000
    },
    {
        "funding_year": 2022,
        "total_funding": 4509675000
    },
    {
        "funding_year": 2023,
        "total_funding": 4001981000
    },
    {
        "funding_year": 2024,
        "total_funding": 5979808000
    },
    {
        "funding_year": 2025,
        "total_funding": 2813215000
    }
]

fig = funding_trend_chart(
    historical_data
)

if fig:
    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# ============================================================
# HORIZONTAL BAR TEST
# ============================================================

st.header("4. Industry Ranking Chart")

industry_data = [
    {
        "industry_name": "EdTech",
        "total_funding": 3739262000
    },
    {
        "industry_name": "Mobility",
        "total_funding": 3200000000
    },
    {
        "industry_name": "Retail",
        "total_funding": 2800000000
    },
    {
        "industry_name": "FinTech",
        "total_funding": 2500000000
    }
]

fig = horizontal_bar_chart(
    industry_data,
    category_column="industry_name",
    value_column="total_funding",
    title="Top Industries by Funding"
)

if fig:
    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# ============================================================
# DONUT CHART TEST
# ============================================================

st.header("5. Funding Distribution")

funding_type_data = [
    {
        "funding_type": "Seed",
        "total_funding": 3000000000
    },
    {
        "funding_type": "Series A",
        "total_funding": 5000000000
    },
    {
        "funding_type": "Series B",
        "total_funding": 7000000000
    },
    {
        "funding_type": "Series C",
        "total_funding": 4000000000
    }
]

fig = donut_chart(
    funding_type_data,
    names_column="funding_type",
    values_column="total_funding",
    title="Funding by Type"
)

if fig:
    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# ============================================================
# FORECAST CHART TEST
# ============================================================

st.header("6. Historical vs Forecast")

forecast_data = [
    {
        "year": 2026,
        "predicted_funding": 3645000000
    },
    {
        "year": 2027,
        "predicted_funding": 3349000000
    },
    {
        "year": 2028,
        "predicted_funding": 3053006400
    }
]

historical_forecast_data = [
    {
        "year": 2020,
        "total_funding": 4756665000
    },
    {
        "year": 2021,
        "total_funding": 6024899000
    },
    {
        "year": 2022,
        "total_funding": 4509675000
    },
    {
        "year": 2023,
        "total_funding": 4001981000
    },
    {
        "year": 2024,
        "total_funding": 5979808000
    },
    {
        "year": 2025,
        "total_funding": 2813215000
    }
]

fig = funding_forecast_chart(
    historical_forecast_data,
    forecast_data
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SIDEBAR FILTER TEST
# ============================================================

st.divider()

st.header("7. Sidebar Filter Output")

st.write(
    "Selected Year Range:",
    filters["year_range"]
)