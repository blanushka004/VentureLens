def generate_recommendations(data:dict, evaluation:dict):
    rec=[]
    if data.get('monthly_users',0)<1000: rec.append('Prioritize customer discovery and measurable user acquisition before aggressively scaling.')
    if data.get('monthly_revenue',0)<=0: rec.append('Validate willingness to pay and test a repeatable revenue model.')
    if data.get('monthly_growth',0)<10: rec.append('Define one growth loop and track month-over-month activation, retention, and acquisition metrics.')
    if evaluation['risk_level']!='Low': rec.append('Reduce execution risk by setting 90-day milestones for product, traction, and runway.')
    if evaluation['funding_readiness']<60: rec.append('Build an investor-ready data room with traction, unit economics, market sizing, and a clear use of funds.')
    if data.get('competition') in ('High','Very High'): rec.append('Strengthen differentiation through a focused niche, proprietary data, partnerships, or superior distribution.')
    if not rec: rec.append('Focus on maintaining growth efficiency and improving retention while preparing for the next stage of scale.')
    return rec[:6]
