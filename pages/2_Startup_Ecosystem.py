import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_metrics_row, format_currency
from analytics import startup_analysis

st.set_page_config(page_title="Startup Ecosystem | VentureLens", page_icon="🚀", layout="wide")
render_sidebar()

@st.cache_data(ttl=300)
def load_data():
    return {
        "overview": startup_analysis.get_startup_overview(),
        "top": startup_analysis.get_top_funded_startups(15),
        "active": startup_analysis.get_most_active_startups(15),
        "industry": startup_analysis.get_startup_distribution_by_industry(),
        "city": startup_analysis.get_startup_distribution_by_city(),
        "recent": startup_analysis.get_recently_funded_startups(15),
        "momentum": startup_analysis.get_startup_funding_momentum(),
    }

def main():
    st.title("🚀 Startup Ecosystem")
    st.caption("Understand startup distribution, activity, funding and ecosystem momentum")
    try: data = load_data()
    except Exception as e: st.error(f"Unable to load startup analytics: {e}"); st.stop()
    o = data["overview"]
    render_metrics_row([
        {"label":"🚀 Total Startups","value":f"{o.get('total_startups',0):,}"},
        {"label":"🏭 Industries","value":f"{o.get('total_industries',0):,}"},
        {"label":"🌍 Startup Cities","value":f"{o.get('total_locations',0):,}"},
        {"label":"💰 Funded Startups","value":f"{o.get('funded_startups',0):,}"},
    ])
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Startup Distribution by Industry")
        df=pd.DataFrame(data['industry'])
        if not df.empty: st.plotly_chart(px.bar(df, x='industry_name', y='startup_count'), use_container_width=True)
    with c2:
        st.subheader("Startup Distribution by City")
        df=pd.DataFrame(data['city'])
        if not df.empty: st.plotly_chart(px.bar(df.sort_values('startup_count'), x='startup_count', y='city', orientation='h'), use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Top Funded Startups")
        df=pd.DataFrame(data['top'])
        if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
    with c2:
        st.subheader("Most Active Startups")
        df=pd.DataFrame(data['active'])
        if not df.empty: st.dataframe(df, use_container_width=True, hide_index=True)
    st.subheader("Recent Funding Activity")
    recent=pd.DataFrame(data['recent'])
    if not recent.empty: st.dataframe(recent, use_container_width=True, hide_index=True)
    st.subheader("Startup Funding Momentum")
    momentum=pd.DataFrame(data['momentum'])
    if not momentum.empty:
        momentum['total_period_funding']=momentum['recent_funding'].astype(float)+momentum['previous_funding'].astype(float)
        st.plotly_chart(px.scatter(momentum.head(30), x='previous_funding', y='recent_funding', size='recent_rounds', color='industry_name', hover_name='startup_name'), use_container_width=True)

if __name__ == '__main__': main()
