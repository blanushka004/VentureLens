import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_metrics_row, format_currency
from analytics import startup_analysis

st.set_page_config(page_title='Startup Explorer | VentureLens',page_icon='🔎',layout='wide')
render_sidebar()

@st.cache_data(ttl=300)
def load_startups(): return startup_analysis.get_top_funded_startups(500)

@st.cache_data(ttl=300)
def load_history(name): return startup_analysis.get_startup_funding_history(name)

def main():
 st.title('🔎 Startup Explorer')
 st.caption('Search and investigate individual startups using recorded funding history')
 try:df=pd.DataFrame(load_startups())
 except Exception as e:st.error(f'Unable to load startup explorer: {e}');st.stop()
 if df.empty:st.warning('No startup records available.');st.stop()
 search=st.text_input('Search startup by name')
 filtered=df.copy()
 if search:filtered=filtered[filtered.startup_name.str.contains(search,case=False,na=False)]
 c1,c2=st.columns(2)
 with c1:
  industries=['All']+sorted(df.industry_name.dropna().unique().tolist())
  industry=st.selectbox('Filter by industry',industries)
 with c2:
  cities=['All']+sorted(df.city.dropna().unique().tolist())
  city=st.selectbox('Filter by city',cities)
 if industry!='All':filtered=filtered[filtered.industry_name==industry]
 if city!='All':filtered=filtered[filtered.city==city]
 st.subheader(f'Startup Directory ({len(filtered)} results)')
 st.dataframe(filtered,use_container_width=True,hide_index=True)
 if filtered.empty:return
 selected=st.selectbox('Select a startup to investigate',filtered.startup_name.tolist())
 record=df[df.startup_name==selected].iloc[0]
 render_metrics_row([
  {'label':'Startup','value':selected},
  {'label':'Industry','value':record.industry_name},
  {'label':'City','value':record.city},
  {'label':'Total Funding','value':format_currency(record.total_funding)},
 ])
 history=pd.DataFrame(load_history(selected))
 st.subheader('Funding History')
 if not history.empty:
  c1,c2=st.columns([2,1])
  with c1:st.plotly_chart(px.line(history,x='funding_year',y='funding_amount_usd',markers=True,hover_data=['funding_type']),use_container_width=True)
  with c2:st.plotly_chart(px.pie(history,names='funding_type',values='funding_amount_usd',hole=.45),use_container_width=True)
  st.dataframe(history,use_container_width=True,hide_index=True)
 else:st.info('No detailed funding history available for this startup.')

if __name__=='__main__':main()
