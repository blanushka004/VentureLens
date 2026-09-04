from analytics import overview

from forecasting.funding_generator import FundingForecaster

from ai.insights import AIInsights

from reports.report_generator import ReportGenerator


print("\n" + "=" * 70)
print("VENTURELENS SYSTEM TEST")
print("=" * 70)


# ============================================================
# OVERVIEW TEST
# ============================================================

print("\nEXECUTIVE OVERVIEW")

print("Total Startups:")
print(overview.get_total_startups())

print("\nTotal Funding:")
print(overview.get_total_funding())

print("\nTotal Investors:")
print(overview.get_total_investors())

print("\nTotal Funding Rounds:")
print(overview.get_total_funding_rounds())


# ============================================================
# FORECAST TEST
# ============================================================

print("\n" + "=" * 70)
print("FORECASTING TEST")
print("=" * 70)

forecaster = FundingForecaster()

print("\nHistorical Funding:")
print(
    forecaster.get_historical_funding()
)

print("\nForecast:")
print(
    forecaster.forecast(
        years_ahead=3
    )
)

print("\nTrend Analysis:")
print(
    forecaster.get_trend_analysis()
)


# ============================================================
# AI INSIGHTS TEST
# ============================================================

print("\n" + "=" * 70)
print("AI INSIGHTS TEST")
print("=" * 70)

ai = AIInsights()

insights = ai.generate_all_insights()

for category, items in insights.items():

    print(f"\n{category.upper()}")

    for item in items:

        print(f"• {item}")


# ============================================================
# REPORT TEST
# ============================================================

print("\n" + "=" * 70)
print("REPORT GENERATOR TEST")
print("=" * 70)

report_generator = ReportGenerator()

print(
    report_generator.generate_text_report()
)