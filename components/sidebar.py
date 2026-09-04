import streamlit as st


def render_sidebar():
    """
    Render the VentureLens application sidebar.
    """

    with st.sidebar:

        # =====================================================
        # BRANDING
        # =====================================================

        st.title("🚀 VentureLens")

        st.caption(
            "Indian Startup Intelligence Platform"
        )

        st.divider()

        # =====================================================
        # PLATFORM DESCRIPTION
        # =====================================================

        st.markdown(
            """
            ### Venture Intelligence

            Analyze the Indian startup ecosystem through:

            - Startup analytics
            - Funding intelligence
            - Industry trends
            - Investor activity
            - Geographic insights
            - AI-generated insights
            - Funding forecasts
            - Startup evaluation
            - AI question answering
            """
        )

        st.divider()

        # =====================================================
        # DATASET INFORMATION
        # =====================================================

        st.markdown("### 📊 Dataset")

        st.info(
            """
            **Region:** India

            **Domain:** Startup Ecosystem

            **Currency:** USD

            **Data Source:** Kaggle Startup Funding Dataset
            """
        )

        st.divider()

        # =====================================================
        # FILTER INFORMATION
        # =====================================================

        st.markdown("### ⚙️ Dashboard Controls")

        year_range = st.slider(
            "Select Year Range",
            min_value=2020,
            max_value=2028,
            value=(2020, 2025)
        )

        st.divider()

        # =====================================================
        # ABOUT
        # =====================================================

        st.markdown("### ℹ️ About")

        st.caption(
            "VentureLens combines PostgreSQL, ETL pipelines, "
            "analytics, OLAP queries, machine learning "
            "forecasting, and AI-driven insights."
        )

        st.caption(
            "Built for startup ecosystem intelligence."
        )

    return {
        "year_range": year_range
    }