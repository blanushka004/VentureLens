import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_forecast_metrics, render_metrics_row, format_currency
from forecasting.funding_generator import FundingForecaster

st.set_page_config(page_title='Funding Forecast | VentureLens',page_icon='🔮',layout='wide')
render_sidebar()

def main():
 st.title('🔮 Funding Forecast')
 st.caption('Machine-learning based funding projections using Linear Regression on historical ecosystem funding')
 years=st.slider('Forecast horizon (years)',1,5,3)
 try:
  forecaster=FundingForecaster();historical=forecaster.get_historical_funding();forecast=forecaster.forecast(years);summary=forecaster.get_forecast_summary(years);trend=forecaster.get_trend_analysis()
 except Exception as e:st.error(f'Unable to generate forecast: {e}');st.stop()
 if summary.get('status')!='Success':st.warning(summary.get('message','Forecast unavailable.'));st.stop()
 render_forecast_metrics(summary['latest_funding'],summary['forecast_funding'],summary['projected_change_percent'],summary['forecast_year'])
 c1,c2=st.columns([2,1])
 with c1:
  st.subheader('Historical Funding vs Forecast')
  hist=historical.rename(columns={'total_funding':'funding'}).copy();hist['type']='Historical'
  fc=forecast.rename(columns={'predicted_funding':'funding'}).copy();fc['type']='Forecast'
  combined=pd.concat([hist[['year','funding','type']],fc[['year','funding','type']]],ignore_index=True)
  st.plotly_chart(px.line(combined,x='year',y='funding',color='type',markers=True),use_container_width=True)
 with c2:
  st.subheader('Trend Analysis')
  st.metric('Long-Term Trend',trend.get('trend','Unknown'))
  st.metric('Historical Change',f"{trend.get('growth_rate',0):+.2f}%")
  st.metric('Model Slope',format_currency(trend.get('slope',0)))
  st.info(trend.get('message',''))
 st.subheader('Forecast Table')
 display=forecast.copy();display['predicted_funding']=display['predicted_funding'].map(lambda x:f'${x:,.0f}')
 st.dataframe(display,use_container_width=True,hide_index=True)
 st.subheader('Historical Data')
 st.dataframe(historical,use_container_width=True,hide_index=True)
 st.warning('Model note: this forecast uses Linear Regression and is intended as an analytical projection, not an investment guarantee.')

if __name__=='__main__':main()
