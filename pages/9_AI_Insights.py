import streamlit as st
from components.sidebar import render_sidebar
from ai.insights import AIInsights
from ai.venture_agent import VentureAgent

st.set_page_config(page_title='AI Intelligence | VentureLens',page_icon='🤖',layout='wide')
render_sidebar()
@st.cache_data(ttl=300)
def load_insights(): return AIInsights().generate_all_insights()
def show_section(title,items,icon):
    st.subheader(f'{icon} {title}')
    for item in items or []: st.markdown(f'- {item}')
def main():
    st.title('🤖 VentureLens AI Intelligence')
    tab1,tab2=st.tabs(['Automated Intelligence','Ask VentureLens'])
    with tab1:
        if st.button('🔄 Refresh AI Insights'): st.cache_data.clear()
        try: insights=load_insights()
        except Exception as e: st.error(f'Unable to generate AI insights: {e}'); insights={}
        c1,c2=st.columns(2)
        with c1: show_section('Executive Insights',insights.get('executive_insights',[]),'📊')
        with c2: show_section('Funding Insights',insights.get('funding_insights',[]),'💰')
        c1,c2=st.columns(2)
        with c1: show_section('Industry Insights',insights.get('industry_insights',[]),'🏭')
        with c2: show_section('Investor Insights',insights.get('investor_insights',[]),'🏦')
        show_section('Forecast Insights',insights.get('forecast_insights',[]),'🔮')
    with tab2:
        st.caption('Ask questions about the startup ecosystem using the live VentureLens intelligence layer.')
        if 'agent_messages' not in st.session_state: st.session_state.agent_messages=[]
        for m in st.session_state.agent_messages:
            with st.chat_message(m['role']): st.write(m['content'])
        q=st.chat_input('Ask about industries, investors, startups, or funding trends...')
        if q:
            st.session_state.agent_messages.append({'role':'user','content':q})
            with st.chat_message('user'): st.write(q)
            with st.chat_message('assistant'):
                answer=VentureAgent().answer(q); st.write(answer)
            st.session_state.agent_messages.append({'role':'assistant','content':answer})
        if st.button('Clear conversation'): st.session_state.agent_messages=[]; st.rerun()
if __name__=='__main__': main()
