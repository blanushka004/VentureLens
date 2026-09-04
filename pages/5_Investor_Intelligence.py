import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_metrics_row
from analytics import investor_analysis

st.set_page_config(page_title='Investor Intelligence | VentureLens',page_icon='🏦',layout='wide')
render_sidebar()

@st.cache_data(ttl=300)
def load_data():
    return {
      'top':investor_analysis.get_top_investors(15),
      'portfolio':investor_analysis.get_investor_portfolio(),
      'preferences':investor_analysis.get_investor_industry_preferences(30),
      'geo':investor_analysis.get_investor_geographic_reach(30),
      'activity':investor_analysis.get_investor_activity_by_year(),
      'diversified':investor_analysis.get_most_diversified_investors(15),
      'pairs':investor_analysis.get_co_investment_pairs(20),
    }

def main():
    st.title('🏦 Investor Intelligence')
    st.caption('Analyze investor activity, portfolios, sector preferences and co-investment patterns')
    try:data=load_data()
    except Exception as e:st.error(f'Unable to load investor analytics: {e}');st.stop()
    top=pd.DataFrame(data['top']); portfolio=pd.DataFrame(data['portfolio'])
    render_metrics_row([
      {'label':'Tracked Investors','value':f'{len(portfolio):,}'},
      {'label':'Most Active', 'value':top.iloc[0].investor_name if not top.empty else 'N/A'},
      {'label':'Highest Activity','value':f"{int(top.iloc[0].investments_count):,}" if not top.empty else '0'},
      {'label':'Largest Portfolio','value':f"{int(portfolio.iloc[0].portfolio_size):,}" if not portfolio.empty else '0'},
    ])
    c1,c2=st.columns(2)
    with c1:
      st.subheader('Most Active Investors')
      if not top.empty:st.plotly_chart(px.bar(top.sort_values('investments_count'),x='investments_count',y='investor_name',orientation='h',hover_data=['startups_invested']),use_container_width=True)
    with c2:
      st.subheader('Portfolio Size')
      if not portfolio.empty:st.plotly_chart(px.bar(portfolio.head(15).sort_values('portfolio_size'),x='portfolio_size',y='investor_name',orientation='h'),use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
      st.subheader('Industry Preferences')
      df=pd.DataFrame(data['preferences'])
      if not df.empty:st.plotly_chart(px.bar(df,x='industry_name',y='investments_count',color='investor_name'),use_container_width=True)
    with c2:
      st.subheader('Geographic Reach')
      df=pd.DataFrame(data['geo'])
      if not df.empty:st.plotly_chart(px.scatter(df,x='city',y='investments_count',size='startups_count',color='investor_name'),use_container_width=True)
    st.subheader('Investor Activity by Year')
    activity=pd.DataFrame(data['activity'])
    if not activity.empty:
      selected=st.multiselect('Investors for activity trend',sorted(activity.investor_name.unique()),default=sorted(activity.investor_name.unique())[:5])
      st.plotly_chart(px.line(activity[activity.investor_name.isin(selected)],x='funding_year',y='investments_count',color='investor_name',markers=True),use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
      st.subheader('Most Diversified Investors')
      df=pd.DataFrame(data['diversified'])
      if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)
    with c2:
      st.subheader('Co-Investment Network')
      df=pd.DataFrame(data['pairs'])
      if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)

if __name__=='__main__':main()
