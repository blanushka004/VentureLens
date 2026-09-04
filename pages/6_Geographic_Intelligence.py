import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_metrics_row, format_currency
from analytics import geographic_analysis

st.set_page_config(page_title='Geographic Intelligence | VentureLens',page_icon='🌍',layout='wide')
render_sidebar()

@st.cache_data(ttl=300)
def load_data():
 return {
  'overview':geographic_analysis.get_geographic_overview(),
  'ecosystem':geographic_analysis.get_city_ecosystem(),
  'startups':geographic_analysis.get_top_cities_by_startups(15),
  'funding':geographic_analysis.get_top_cities_by_funding(15),
  'industry':geographic_analysis.get_city_industry_distribution(),
  'leading':geographic_analysis.get_city_leading_industries(),
  'growth':geographic_analysis.get_city_funding_growth(),
  'concentration':geographic_analysis.get_city_funding_concentration(),
  'average':geographic_analysis.get_city_average_funding(),
  'activity':geographic_analysis.get_city_investment_activity(),
 }

def main():
 st.title('🌍 Geographic Intelligence')
 st.caption('Explore startup ecosystems, funding concentration and investment activity across Indian cities')
 try:data=load_data()
 except Exception as e:st.error(f'Unable to load geographic analytics: {e}');st.stop()
 o=data['overview']
 render_metrics_row([
  {'label':'Cities','value':f"{o.get('total_cities',0):,}"},
  {'label':'Startups','value':f"{o.get('total_startups',0):,}"},
  {'label':'Industries Present','value':f"{o.get('industries_present',0):,}"},
  {'label':'Total Funding','value':format_currency(o.get('total_funding',0))},
 ])
 c1,c2=st.columns(2)
 with c1:
  st.subheader('Cities by Startup Count');df=pd.DataFrame(data['startups'])
  if not df.empty:st.plotly_chart(px.bar(df.sort_values('startup_count'),x='startup_count',y='city',orientation='h'),use_container_width=True)
 with c2:
  st.subheader('Cities by Funding');df=pd.DataFrame(data['funding'])
  if not df.empty:st.plotly_chart(px.bar(df.sort_values('total_funding'),x='total_funding',y='city',orientation='h'),use_container_width=True)
 c1,c2=st.columns(2)
 with c1:
  st.subheader('Funding Concentration');df=pd.DataFrame(data['concentration'])
  if not df.empty:st.plotly_chart(px.pie(df.head(10),names='city',values='funding_percentage',hole=.45),use_container_width=True)
 with c2:
  st.subheader('Average Funding per Startup');df=pd.DataFrame(data['average'])
  if not df.empty:st.plotly_chart(px.bar(df.sort_values('average_funding_per_startup'),x='average_funding_per_startup',y='city',orientation='h'),use_container_width=True)
 st.subheader('City Funding Growth')
 growth=pd.DataFrame(data['growth'])
 if not growth.empty:
  selected=st.multiselect('Select cities',sorted(growth.city.unique()),default=sorted(growth.city.unique())[:5])
  st.plotly_chart(px.line(growth[growth.city.isin(selected)],x='funding_year',y='total_funding',color='city',markers=True),use_container_width=True)
 c1,c2=st.columns(2)
 with c1:
  st.subheader('Leading Industry by City');df=pd.DataFrame(data['leading'])
  if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)
 with c2:
  st.subheader('City Investment Activity');df=pd.DataFrame(data['activity'])
  if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)
 st.subheader('Complete City Ecosystem');df=pd.DataFrame(data['ecosystem'])
 if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)

if __name__=='__main__':main()
