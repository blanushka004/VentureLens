import streamlit as st

from components.sidebar import render_sidebar
from components.metrics import render_funding_metrics

from analytics import overview
from forecasting.funding_generator import FundingForecaster


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="VentureLens",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

filters = render_sidebar()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=300)
def load_executive_data():

    total_startups = (
        overview.get_total_startups()
        .get("total_startups", 0)
    )

    total_funding = float(
        overview.get_total_funding()
        .get("total_funding", 0)
    )

    total_investors = (
        overview.get_total_investors()
        .get("total_investors", 0)
    )

    total_rounds = (
        overview.get_total_funding_rounds()
        .get("total_funding_rounds", 0)
    )

    funding_by_year = (
        overview.get_funding_by_year()
    )

    top_industries = (
        overview.get_top_industries(limit=5)
    )

    top_cities = (
        overview.get_top_cities(limit=5)
    )

    return {
        "total_startups": total_startups,
        "total_funding": total_funding,
        "total_investors": total_investors,
        "total_rounds": total_rounds,
        "funding_by_year": funding_by_year,
        "top_industries": top_industries,
        "top_cities": top_cities
    }


@st.cache_data(ttl=300)
def load_forecast_data():

    forecaster = FundingForecaster()

    return forecaster.get_forecast_summary(
        years_ahead=3
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">🚀 VentureLens</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Indian Startup Ecosystem Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()


    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    try:

        data = load_executive_data()
        forecast = load_forecast_data()

    except Exception as error:

        st.error(
            f"Unable to load VentureLens data: {error}"
        )

        st.stop()


    # --------------------------------------------------------
    # EXECUTIVE METRICS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    render_funding_metrics(
        total_funding=data["total_funding"],
        total_startups=data["total_startups"],
        total_investors=data["total_investors"],
        total_rounds=data["total_rounds"]
    )


    # --------------------------------------------------------
    # PLATFORM OVERVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Platform Intelligence</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.subheader("📊 Ecosystem Analytics")

        st.write(
            "Explore startup growth, funding activity, "
            "industries, investors, and geographic trends."
        )

    with col2:

        st.subheader("🔮 Funding Forecasting")

        if forecast.get("status") == "Success":

            st.write(
                f"Funding is projected to reach "
                f"${forecast['forecast_funding']:,.0f} "
                f"by {forecast['forecast_year']}."
            )

        else:

            st.write(
                "Forecasting insights are currently unavailable."
            )

    with col3:

        st.subheader("🤖 AI Intelligence")

        st.write(
            "Generate automated insights, identify risks, "
            "discover opportunities, and analyze ecosystem trends."
        )


    # --------------------------------------------------------
    # QUICK DATA PREVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Ecosystem Snapshot</div>',
        unsafe_allow_html=True
    )

    left_col, right_col = st.columns(2)


    with left_col:

        st.subheader("🏭 Leading Industries")

        if data["top_industries"]:

            st.dataframe(
                data["top_industries"],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Industry data unavailable."
            )


    with right_col:

        st.subheader("🌍 Leading Startup Hubs")

        if data["top_cities"]:

            st.dataframe(
                data["top_cities"],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Geographic data unavailable."
            )


    # --------------------------------------------------------
    # NAVIGATION GUIDE
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-title">Explore VentureLens</div>',
        unsafe_allow_html=True
    )

    navigation_col1, navigation_col2, navigation_col3 = st.columns(3)


    with navigation_col1:

        st.markdown(
            """
            ### 📈 Intelligence

            - Executive Overview
            - Startup Ecosystem
            - Funding Intelligence
            - Industry Intelligence
            """
        )


    with navigation_col2:

        st.markdown(
            """
            ### 🏦 Investment

            - Investor Intelligence
            - Geographic Intelligence
            - Startup Explorer
            - OLAP Analytics
            """
        )


    with navigation_col3:

        st.markdown(
            """
            ### 🤖 Advanced Analytics

            - AI Insights
            - Funding Forecast
            - Reports & Export
            """
        )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "VentureLens • Indian Startup Ecosystem Intelligence Platform "
        "• Powered by PostgreSQL, Analytics, Forecasting & AI"
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    main()