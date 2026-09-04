import streamlit as st
import pandas as pd
import plotly.express as px

from components.sidebar import render_sidebar
from components.metrics import render_metrics_row, format_currency
from analytics import funding_analysis

st.set_page_config(page_title="Funding Intelligence | VentureLens", page_icon="💰", layout="wide")
filters=render_sidebar()

@st.cache_data(ttl=300)
def load_data():
    return {
        'summary': funding_analysis.get_funding_summary(),
        'yearly': funding_analysis.get_yearly_funding_trend(),
        'quarterly': funding_analysis.get_quarterly_funding_trend(),
        'types': funding_analysis.get_funding_distribution_by_type(),
        'type_trend': funding_analysis.get_funding_type_trend(),
        'largest': funding_analysis.get_largest_funding_rounds(20),
        'growth': funding_analysis.get_year_over_year_growth(),
        'monthly': funding_analysis.get_monthly_funding_trend(),
    }

def main():
    st.title("💰 Funding Intelligence")
    st.caption("Analyze funding volume, investment stages, growth and major rounds")
    try: data=load_data()
    except Exception as e: st.error(f"Unable to load funding analytics: {e}"); st.stop()
    s=data['summary']
    render_metrics_row([
        {'label':'Funding Rounds','value':f"{s.get('total_rounds',0):,}"},
        {'label':'Total Funding','value':format_currency(s.get('total_funding',0))},
        {'label':'Average Round','value':format_currency(s.get('average_funding',0))},
        {'label':'Largest Round','value':format_currency(s.get('largest_round',0))},
    ])
    yearly=pd.DataFrame(data['yearly']); start,end=filters['year_range']
    if not yearly.empty: yearly=yearly[yearly.funding_year.between(start,end)]
    c1,c2=st.columns(2)
    with c1:
        st.subheader('Annual Funding Trend')
        if not yearly.empty: st.plotly_chart(px.line(yearly,x='funding_year',y='total_funding',markers=True,hover_data=['funding_rounds','average_funding']),use_container_width=True)
    with c2:
        st.subheader('Year-over-Year Growth')
        growth=pd.DataFrame(data['growth'])
        if not growth.empty:
            growth=growth[growth.funding_year.between(start,end)]
            st.plotly_chart(px.bar(growth,x='funding_year',y='growth_percentage'),use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        st.subheader('Funding Distribution by Type')
        df=pd.DataFrame(data['types'])
        if not df.empty: st.plotly_chart(px.pie(df,names='funding_type',values='total_funding',hole=.45),use_container_width=True)
    with c2:
        st.subheader('Funding Type Trend')
        df=pd.DataFrame(data['type_trend'])
        if not df.empty: st.plotly_chart(px.bar(df[df.funding_year.between(start,end)],x='funding_year',y='total_funding',color='funding_type',barmode='stack'),use_container_width=True)
    st.subheader('Quarterly Funding Activity')
    q=pd.DataFrame(data['quarterly'])
    if not q.empty:
        q=q[q.funding_year.between(start,end)]; q['period']=q['funding_year'].astype(str)+' '+q['quarter']
        st.plotly_chart(px.bar(q,x='period',y='total_funding',hover_data=['funding_rounds']),use_container_width=True)
    st.subheader('Largest Funding Rounds')
    largest=pd.DataFrame(data['largest'])
    if not largest.empty: st.dataframe(largest,use_container_width=True,hide_index=True)

if __name__=='__main__': main()
