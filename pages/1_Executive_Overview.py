import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_funding_metrics
from analytics import overview
from forecasting.funding_generator import FundingForecaster

st.set_page_config(page_title="Executive Overview | VentureLens", page_icon="🚀", layout="wide")
filters = render_sidebar()

@st.cache_data(ttl=300)
def load_data():
    return {
        "startups": overview.get_total_startups().get("total_startups", 0),
        "funding": float(overview.get_total_funding().get("total_funding", 0)),
        "investors": overview.get_total_investors().get("total_investors", 0),
        "rounds": overview.get_total_funding_rounds().get("total_funding_rounds", 0),
        "yearly": overview.get_funding_by_year(),
        "industries": overview.get_top_industries(10),
        "startups_rank": overview.get_top_startups(10),
        "cities": overview.get_top_cities(10),
        "types": overview.get_funding_by_type(),
    }

def main():
    st.title("📊 Executive Overview")
    st.caption("A high-level view of the Indian startup ecosystem")
    try:
        data = load_data()
    except Exception as e:
        st.error(f"Unable to load dashboard data: {e}"); st.stop()

    render_funding_metrics(data["funding"], data["startups"], data["investors"], data["rounds"])
    yearly = pd.DataFrame(data["yearly"])
    if not yearly.empty:
        start, end = filters["year_range"]
        yearly = yearly[yearly["funding_year"].between(start, end)]
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Funding Trend")
        if not yearly.empty:
            fig = px.line(yearly, x="funding_year", y="total_funding", markers=True, hover_data=["funding_rounds"])
            fig.update_layout(xaxis_title="Year", yaxis_title="Funding (USD)")
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Funding by Type")
        types = pd.DataFrame(data["types"])
        if not types.empty:
            st.plotly_chart(px.pie(types, names="funding_type", values="total_funding", hole=.45), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top Industries")
        df = pd.DataFrame(data["industries"])
        if not df.empty:
            st.plotly_chart(px.bar(df.sort_values("total_funding"), x="total_funding", y="industry_name", orientation="h"), use_container_width=True)
    with c2:
        st.subheader("Leading Startup Hubs")
        df = pd.DataFrame(data["cities"])
        if not df.empty:
            st.plotly_chart(px.bar(df.sort_values("total_funding"), x="total_funding", y="city", orientation="h"), use_container_width=True)

    st.subheader("Top Funded Startups")
    top = pd.DataFrame(data["startups_rank"])
    if not top.empty:
        st.dataframe(top, use_container_width=True, hide_index=True)

    forecaster = FundingForecaster()
    summary = forecaster.get_forecast_summary(3)
    if summary.get("status") == "Success":
        st.info(f"🔮 Funding forecast: {summary['forecast_year']} is projected at ${summary['forecast_funding']:,.0f} ({summary['projected_change_percent']:+.2f}% vs latest year).")

if __name__ == "__main__": main()
