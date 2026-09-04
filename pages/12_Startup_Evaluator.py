import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar
from ai.startup_evaluator import run_startup_evaluation

st.set_page_config(page_title='Startup Evaluator | VentureLens', page_icon='🚀', layout='wide')
render_sidebar()

def main():
    st.title('🚀 Startup Evaluator')
    st.caption('Get a data-informed venture potential assessment based on your startup characteristics.')
    with st.form('startup_evaluation_form'):
        c1,c2,c3=st.columns(3)
        with c1:
            name=st.text_input('Startup Name', placeholder='Optional')
            industry=st.selectbox('Industry',['AI','HealthTech','FinTech','SaaS','ClimateTech','EdTech','Mobility','E-commerce','Retail','Other'])
            city=st.text_input('City',value='Hyderabad')
            stage=st.selectbox('Startup Stage',['Idea','Prototype/MVP','Early Revenue','Growth','Scale'])
        with c2:
            team=st.number_input('Team Size',1,100,3)
            experience=st.slider('Founder Experience (years)',0,20,3)
            users=st.number_input('Monthly Active Users / Customers',0,10000000,0,step=100)
            revenue=st.number_input('Monthly Revenue (USD)',0,100000000,0,step=1000)
        with c3:
            funding=st.number_input('Funding Raised (USD)',0,1000000000,0,step=10000)
            market=st.number_input('Estimated Market Size (USD Millions)',1,1000000,100)
            growth=st.slider('Monthly Growth (%)',0.0,100.0,5.0)
            competition=st.selectbox('Competition Level',['Low','Medium','High','Very High'])
            model=st.selectbox('Business Model',['B2B SaaS','Subscription','Marketplace','B2C','Enterprise','Other'])
        submitted=st.form_submit_button('🔍 Evaluate My Startup',use_container_width=True)
    if not submitted: return
    data={'startup_name':name,'industry':industry,'city':city,'stage':stage,'team_size':team,'founder_experience':experience,'monthly_users':users,'monthly_revenue':revenue,'funding_raised':funding,'market_size':market,'monthly_growth':growth,'competition':competition,'business_model':model}
    with st.spinner('Analyzing venture potential...'):
        result=run_startup_evaluation(data)
    st.divider(); st.subheader('Venture Assessment')
    a,b,c,d=st.columns(4)
    a.metric('Venture Score',f"{result['venture_score']}/100",result['potential_level'])
    b.metric('Success Potential',f"{result['success_potential']}%")
    c.metric('Funding Readiness',f"{result['funding_readiness']}%")
    d.metric('Risk Level',result['risk_level'])
    scores=pd.DataFrame({'Dimension':list(result['component_scores'].keys()),'Score':list(result['component_scores'].values())})
    st.plotly_chart(px.bar(scores,x='Dimension',y='Score',range_y=[0,100],text='Score'),use_container_width=True)
    l,r=st.columns(2)
    with l:
        st.success('### Strengths')
        for x in result['strengths']: st.write('• '+x)
        st.info('### Recommendations')
        for x in result['recommendations']: st.write('• '+x)
    with r:
        st.warning('### Risks / Weaknesses')
        for x in result['weaknesses']: st.write('• '+x)
        st.subheader('🎯 Potential Investor Matches')
        matches=result.get('investor_matches',[])
        if matches: st.dataframe(pd.DataFrame(matches),use_container_width=True,hide_index=True)
        else: st.info('No live investor matches available for the selected profile.')
    st.caption(result['disclaimer'])
if __name__=='__main__': main()
