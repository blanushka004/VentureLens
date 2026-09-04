import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from analytics import olap_queries

st.set_page_config(page_title='OLAP Analytics | VentureLens',page_icon='🧊',layout='wide')
render_sidebar()

@st.cache_data(ttl=300)
def base_data():
 return {
  'year':olap_queries.funding_rollup_by_year(),
  'city':olap_queries.funding_rollup_by_city(),
  'industry':olap_queries.funding_rollup_by_industry(),
  'year_month':olap_queries.funding_drilldown_year_to_month(),
  'industry_startup':olap_queries.industry_drilldown_to_startups(),
  'city_industry':olap_queries.city_drilldown_to_industry(),
  'pivot_ci':olap_queries.funding_pivot_city_industry(),
  'pivot_ys':olap_queries.funding_pivot_year_stage(),
 }

def main():
 st.title('🧊 OLAP Analytics')
 st.caption('Multidimensional startup funding analysis using roll-up, drill-down, slice, dice and pivot operations')
 try:data=base_data()
 except Exception as e:st.error(f'Unable to load OLAP analytics: {e}');st.stop()
 tabs=st.tabs(['Roll-Up','Drill-Down','Slice','Dice','Pivot'])
 with tabs[0]:
  mode=st.radio('Roll-up dimension',['Year','City','Industry'],horizontal=True)
  key={'Year':'year','City':'city','Industry':'industry'}[mode];df=pd.DataFrame(data[key])
  if not df.empty:
   category={'Year':'funding_year','City':'city','Industry':'industry_name'}[mode]
   st.plotly_chart(px.bar(df,x=category,y='total_funding'),use_container_width=True);st.dataframe(df,use_container_width=True,hide_index=True)
 with tabs[1]:
  mode=st.selectbox('Choose drill-down operation',['Year → Month','Industry → Startup','City → Industry'])
  key={'Year → Month':'year_month','Industry → Startup':'industry_startup','City → Industry':'city_industry'}[mode];df=pd.DataFrame(data[key])
  if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)
 with tabs[2]:
  option=st.selectbox('Slice dimension',['Industry','City','Year'])
  if option=='Industry':
   values=sorted(pd.DataFrame(data['industry']).industry_name.unique());value=st.selectbox('Industry',values);df=pd.DataFrame(olap_queries.funding_slice_by_industry(value))
  elif option=='City':
   values=sorted(pd.DataFrame(data['city']).city.unique());value=st.selectbox('City',values);df=pd.DataFrame(olap_queries.funding_slice_by_city(value))
  else:
   values=sorted(pd.DataFrame(data['year']).funding_year.unique());value=st.selectbox('Year',values);df=pd.DataFrame(olap_queries.funding_slice_by_year(int(value)))
  if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)
 with tabs[3]:
  industries=sorted(pd.DataFrame(data['industry']).industry_name.unique());cities=sorted(pd.DataFrame(data['city']).city.unique());years=sorted(pd.DataFrame(data['year']).funding_year.unique())
  selected_i=st.multiselect('Industries',industries,default=industries[:min(3,len(industries))]);selected_c=st.multiselect('Cities',cities,default=cities[:min(3,len(cities))]);yr=st.slider('Year range',int(min(years)),int(max(years)),(int(min(years)),int(max(years))))
  if selected_i and selected_c:
   df=pd.DataFrame(olap_queries.funding_dice(selected_i,selected_c,yr[0],yr[1]))
   if not df.empty:
    st.plotly_chart(px.bar(df,x='funding_year',y='total_funding',color='industry_name',facet_col='city'),use_container_width=True);st.dataframe(df,use_container_width=True,hide_index=True)
 with tabs[4]:
  c1,c2=st.columns(2)
  with c1:
   st.subheader('City × Industry Funding');df=pd.DataFrame(data['pivot_ci'])
   if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)
  with c2:
   st.subheader('Year × Funding Stage');df=pd.DataFrame(data['pivot_ys'])
   if not df.empty:st.dataframe(df,use_container_width=True,hide_index=True)

if __name__=='__main__':main()
