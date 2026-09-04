from __future__ import annotations

INDUSTRY_BASE = {
    "AI": 82, "HealthTech": 80, "FinTech": 79, "SaaS": 78,
    "ClimateTech": 78, "EdTech": 74, "Mobility": 75,
    "E-commerce": 70, "Retail": 68
}
STAGE_BASE = {"Idea": 40, "Prototype/MVP": 55, "Early Revenue": 68, "Growth": 80, "Scale": 88}

def _norm(value, low, high):
    if high <= low: return 0
    return max(0, min(1, (float(value)-low)/(high-low)))

def evaluate_startup(data: dict) -> dict:
    industry = data.get('industry', 'Other')
    stage = data.get('stage', 'Idea')
    industry_score = INDUSTRY_BASE.get(industry, 65)
    stage_score = STAGE_BASE.get(stage, 50)
    team = min(100, _norm(data.get('team_size',1), 1, 15)*100)
    experience = min(100, float(data.get('founder_experience', 5))*10)
    users = _norm(data.get('monthly_users',0), 0, 100000)*100
    revenue = _norm(data.get('monthly_revenue',0), 0, 2000000)*100
    growth = _norm(data.get('monthly_growth',0), 0, 30)*100
    funding = _norm(data.get('funding_raised',0), 0, 10000000)*100
    market = _norm(data.get('market_size',0), 1, 10000)*100
    competition_map={'Low':85,'Medium':70,'High':52,'Very High':38}
    competition = competition_map.get(data.get('competition','Medium'),65)
    model_map={'B2B SaaS':85,'Subscription':82,'Marketplace':74,'B2C':70,'Enterprise':82,'Other':65}
    business_model = model_map.get(data.get('business_model','Other'),65)

    score = (industry_score*.10 + stage_score*.10 + team*.08 + experience*.10 + users*.12 + revenue*.15 + growth*.12 + funding*.06 + market*.07 + competition*.05 + business_model*.05)
    score=round(max(0,min(100,score)),1)
    success=round(max(5,min(95, score*.82 + growth*.10 + experience*.08)),1)
    funding_readiness=round(max(0,min(100, revenue*.28+users*.22+growth*.20+team*.10+market*.10+stage_score*.10)),1)
    risk=round(100-score,1)
    level='High Potential' if score>=75 else 'Promising' if score>=60 else 'Developing' if score>=45 else 'Early Risk'
    risk_level='Low' if risk<30 else 'Medium' if risk<50 else 'High'
    strengths=[]; weaknesses=[]
    if growth>=60: strengths.append('Strong recent growth signal')
    if users>=45: strengths.append('Meaningful customer traction')
    if revenue>=40: strengths.append('Revenue validation is visible')
    if experience>=60: strengths.append('Experienced founding capability')
    if market>=50: strengths.append('Large addressable market')
    if not strengths: strengths.append('The startup has an identifiable opportunity and can improve with stronger validation')
    if competition<60: weaknesses.append('Competitive pressure may make customer acquisition expensive')
    if users<25: weaknesses.append('Limited user traction at the current stage')
    if revenue<20: weaknesses.append('Revenue validation remains weak')
    if funding<15 and stage not in ('Idea','Prototype/MVP'): weaknesses.append('Funding runway may constrain execution')
    if not weaknesses: weaknesses.append('No critical structural weakness detected from the provided inputs')
    return {'venture_score':score,'success_potential':success,'funding_readiness':funding_readiness,'risk_score':risk,'potential_level':level,'risk_level':risk_level,'strengths':strengths[:5],'weaknesses':weaknesses[:5], 'component_scores':{'Market Opportunity':round((industry_score+market)/2,1),'Team':round((team+experience)/2,1),'Traction':round((users+revenue+growth)/3,1),'Funding Readiness':funding_readiness,'Competition Position':competition}}
