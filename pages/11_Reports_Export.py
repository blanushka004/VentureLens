import streamlit as st
import json
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet

from components.sidebar import render_sidebar
from reports.report_generator import ReportGenerator

st.set_page_config(page_title='Reports & Export | VentureLens',page_icon='📄',layout='wide')
render_sidebar()

def make_pdf(text_report):
 buffer=BytesIO();doc=SimpleDocTemplate(buffer,pagesize=A4);styles=getSampleStyleSheet();story=[Paragraph('VentureLens Executive Intelligence Report',styles['Title']),Spacer(1,12),Preformatted(text_report,styles['Code'])];doc.build(story);return buffer.getvalue()

def main():
 st.title('📄 Reports & Export')
 st.caption('Generate and export a consolidated VentureLens Executive Intelligence Report')
 if 'venture_report' not in st.session_state or st.button('🔄 Generate Latest Report'):
  with st.spinner('Generating executive intelligence report...'):
   try:
    generator=ReportGenerator();st.session_state.venture_report=generator.generate_report();st.session_state.venture_text=generator.generate_text_report()
   except Exception as e:st.error(f'Unable to generate report: {e}');st.stop()
 report=st.session_state.get('venture_report');text=st.session_state.get('venture_text','')
 if not report:return
 meta=report['metadata'];summary=report['executive_summary']
 st.success(f"Report generated: {meta['generated_at']}")
 c1,c2,c3,c4=st.columns(4)
 c1.metric('Startups',f"{summary['total_startups']:,}");c2.metric('Total Funding',f"${summary['total_funding']:,.0f}");c3.metric('Investors',f"{summary['total_investors']:,}");c4.metric('Funding Rounds',f"{summary['total_funding_rounds']:,}")
 st.subheader('Report Preview');st.text(text)
 st.subheader('Export Options')
 json_bytes=json.dumps(report,default=str,indent=2).encode('utf-8')
 pdf_bytes=make_pdf(text)
 summary_csv=pd.DataFrame([summary]).to_csv(index=False).encode('utf-8')
 c1,c2,c3=st.columns(3)
 with c1:st.download_button('⬇️ Download TXT',text,file_name='venturelens_report.txt',mime='text/plain',use_container_width=True)
 with c2:st.download_button('⬇️ Download JSON',json_bytes,file_name='venturelens_report.json',mime='application/json',use_container_width=True)
 with c3:st.download_button('⬇️ Download PDF',pdf_bytes,file_name='venturelens_report.pdf',mime='application/pdf',use_container_width=True)
 st.download_button('⬇️ Download Executive Summary CSV',summary_csv,file_name='venturelens_executive_summary.csv',mime='text/csv')

if __name__=='__main__':main()
