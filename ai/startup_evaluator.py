from ai.startup_scoring import evaluate_startup
from ai.recommendation_engine import generate_recommendations
from ai.investor_matcher import match_investors

def run_startup_evaluation(data:dict):
    result=evaluate_startup(data)
    result['recommendations']=generate_recommendations(data,result)
    try: result['investor_matches']=match_investors(data.get('industry','Other'),data.get('city'),5)
    except Exception: result['investor_matches']=[]
    result['disclaimer']='This is an analytical potential assessment based on user-provided information and VentureLens ecosystem signals. It is not a guarantee of startup success or investment.'
    return result
