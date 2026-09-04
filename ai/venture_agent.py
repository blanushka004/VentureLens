from analytics import overview
from analytics import investor_analysis, startup_analysis
from forecasting.funding_generator import FundingForecaster

class VentureAgent:
    def answer(self, question:str):
        q=question.lower().strip()
        try:
            if any(x in q for x in ['funding trend','forecast','future funding','funding growth']):
                f=FundingForecaster().get_forecast_summary(years_ahead=3)
                return f"Funding intelligence: {f}" if f else 'Forecast data is currently unavailable.'
            if any(x in q for x in ['industry','sector']):
                rows=overview.get_top_industries(5)
                if rows:
                    text='; '.join(f"{r['industry_name']} (${float(r['total_funding'] or 0):,.0f})" for r in rows)
                    return 'Top industries by recorded funding: '+text+'.'
            if 'investor' in q:
                rows=investor_analysis.get_top_investors(5)
                return 'Most active investors: '+', '.join(f"{r['investor_name']} ({r['investments_count']} investments)" for r in rows)+'.'
            if any(x in q for x in ['startup','company']):
                rows=startup_analysis.get_top_funded_startups(5)
                return 'Highly funded startups in the dataset: '+', '.join(r['startup_name'] for r in rows)+'. Ask me about an industry, investor, funding trend, or use Startup Evaluator for a custom venture assessment.'
            total=overview.get_total_startups().get('total_startups',0)
            funding=float(overview.get_total_funding().get('total_funding',0))
            return f"VentureLens currently analyzes {total} startups and ${funding:,.0f} in recorded funding. Try asking about top industries, investors, startups, or funding forecasts."
        except Exception as e:
            return f"I could not query the live intelligence layer: {e}"
