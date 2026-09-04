import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_metrics_row, format_currency
from analytics import industry_analysis

st.set_page_config(page_title="Industry Intelligence | VentureLens", page_icon="🏭", layout="wide")
render_sidebar()

@st.cache_data(ttl=300)
def load_data():
    return {
        'overview':industry_analysis.get_industry_overview(),
        'trend':industry_analysis.get_industry_funding_trend(),
        'top':industry_analysis.get_top_industries_by_funding(15),
        'growth':industry_analysis.get_industry_growth(),
        'share':industry_analysis.get_industry_market_share(),
    }

def main():
    st.title('🏭 Industry Intelligence')
    st.caption('Compare sectors by startup activity, capital allocation, growth and market share')
    try:data=load_data()
    except Exception as e:st.error(f'Unable to load industry analytics: {e}');st.stop()
    ov=pd.DataFrame(data['overview'])
    if not ov.empty:
        render_metrics_row([
            {'label':'Industries Tracked','value':f'{len(ov):,}'},
            {'label':'Top Industry', 'value':str(ov.iloc[0]['industry_name'])},
            {'label':'Top Industry Funding','value':format_currency(ov.iloc[0]['total_funding'] or 0)},
            {'label':'Total Ecosystem Funding','value':format_currency(pd.to_numeric(ov['total_funding'],errors='coerce').fillna(0).sum())},
        ])
    c1,c2=st.columns(2)
    with c1:
        st.subheader('Top Industries by Funding')
        df=pd.DataFrame(data['top'])
        if not df.empty:st.plotly_chart(px.bar(df.sort_values('total_funding'),x='total_funding',y='industry_name',orientation='h',hover_data=['funding_rounds','startups']),use_container_width=True)
    with c2:
        st.subheader('Industry Market Share')
        df=pd.DataFrame(data['share'])
        if not df.empty:st.plotly_chart(px.pie(df.head(10),names='industry_name',values='market_share_percentage',hole=.45),use_container_width=True)
    st.subheader('Industry Funding Trend')
    trend=pd.DataFrame(data['trend'])
    if not trend.empty:
        selected=st.multiselect('Select industries',sorted(trend.industry_name.unique()),default=sorted(trend.industry_name.unique())[:5])
        filtered=trend[trend.industry_name.isin(selected)]
        st.plotly_chart(px.line(filtered,x='funding_year',y='total_funding',color='industry_name',markers=True),use_container_width=True)
    st.subheader('Industry Growth Analysis')
    growth=pd.DataFrame(data['growth'])
    if not growth.empty:
        latest=growth.dropna(subset=['growth_percentage']).sort_values('funding_year').groupby('industry_name').tail(1).sort_values('growth_percentage',ascending=False)
        st.plotly_chart(px.bar(latest,x='industry_name',y='growth_percentage'),use_container_width=True)
    st.subheader('Complete Industry Overview')
    if not ov.empty:st.dataframe(ov,use_container_width=True,hide_index=True)

if __name__=='__main__':main()
