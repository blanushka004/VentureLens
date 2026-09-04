from analytics import overview

from forecasting.funding_generator import FundingForecaster


class AIInsights:
    """
    VentureLens AI Insight Engine.

    Generates data-driven business insights from
    VentureLens analytics and forecasting modules.
    """

    def __init__(self):
        self.forecaster = FundingForecaster()

    # =========================================================
    # EXECUTIVE INSIGHTS
    # =========================================================

    def get_executive_insights(self):

        insights = []

        try:
            startups_data = overview.get_total_startups()
            funding_data = overview.get_total_funding()
            investors_data = overview.get_total_investors()
            rounds_data = overview.get_total_funding_rounds()

            total_startups = startups_data.get(
                "total_startups", 0
            )

            total_funding = float(
                funding_data.get(
                    "total_funding", 0
                )
            )

            total_investors = investors_data.get(
                "total_investors", 0
            )

            total_rounds = rounds_data.get(
                "total_funding_rounds", 0
            )

            insights.append(
                f"The VentureLens database tracks "
                f"{total_startups:,} startups across "
                f"the Indian startup ecosystem."
            )

            insights.append(
                f"Total recorded startup funding is "
                f"${total_funding:,.2f}."
            )

            insights.append(
                f"The ecosystem includes "
                f"{total_investors:,} tracked investors."
            )

            insights.append(
                f"A total of {total_rounds:,} funding rounds "
                f"have been recorded."
            )

        except Exception as error:
            insights.append(
                f"Unable to generate executive insights: {error}"
            )

        return insights

    # =========================================================
    # FUNDING INSIGHTS
    # =========================================================

    def get_funding_insights(self):

        insights = []

        try:
            funding_by_year = overview.get_funding_by_year()

            if funding_by_year:

                peak_year = max(
                    funding_by_year,
                    key=lambda x: float(
                        x["total_funding"] or 0
                    )
                )

                insights.append(
                    f"The highest startup funding was recorded "
                    f"in {peak_year['funding_year']}, reaching "
                    f"${float(peak_year['total_funding']):,.0f}."
                )

                latest_year = funding_by_year[-1]

                insights.append(
                    f"The latest available year "
                    f"({latest_year['funding_year']}) recorded "
                    f"${float(latest_year['total_funding']):,.0f} "
                    f"across {latest_year['funding_rounds']} "
                    f"funding rounds."
                )

            trend_data = (
                self.forecaster.get_trend_analysis()
            )

            trend = trend_data.get(
                "trend",
                "Unknown"
            )

            growth_rate = trend_data.get(
                "growth_rate",
                0
            )

            insights.append(
                f"The long-term funding trend is "
                f"{trend.lower()}."
            )

            if growth_rate < 0:
                insights.append(
                    f"Historical funding changed by "
                    f"{growth_rate:.2f}% across the "
                    f"observed period."
                )

            elif growth_rate > 0:
                insights.append(
                    f"Historical funding increased by "
                    f"{growth_rate:.2f}% across the "
                    f"observed period."
                )

        except Exception as error:
            insights.append(
                f"Unable to generate funding insights: {error}"
            )

        return insights

    # =========================================================
    # INDUSTRY INSIGHTS
    # =========================================================

    def get_industry_insights(self):

        insights = []

        try:
            industries = overview.get_top_industries(limit=5)

            if industries:

                top_industry = industries[0]

                industry_name = (
                    top_industry["industry_name"]
                )

                funding = float(
                    top_industry["total_funding"] or 0
                )

                insights.append(
                    f"{industry_name} is the most highly funded "
                    f"industry, with approximately "
                    f"${funding:,.0f} in recorded investment."
                )

                if len(industries) >= 3:

                    top_three = [
                        item["industry_name"]
                        for item in industries[:3]
                    ]

                    insights.append(
                        "The leading industries are "
                        + ", ".join(top_three)
                        + "."
                    )

        except Exception as error:
            insights.append(
                f"Unable to generate industry insights: {error}"
            )

        return insights

    # =========================================================
    # STARTUP INSIGHTS
    # =========================================================

    def get_startup_insights(self):

        insights = []

        try:
            startups = overview.get_top_startups(limit=5)

            if startups:

                top_startup = startups[0]

                startup_name = (
                    top_startup["startup_name"]
                )

                industry = (
                    top_startup["industry_name"]
                )

                funding = float(
                    top_startup["total_funding"] or 0
                )

                insights.append(
                    f"{startup_name}, operating in the "
                    f"{industry} sector, is among the "
                    f"highest-funded startups with "
                    f"${funding:,.0f} in recorded funding."
                )

        except Exception as error:
            insights.append(
                f"Unable to generate startup insights: {error}"
            )

        return insights

    # =========================================================
    # INVESTOR INSIGHTS
    # =========================================================

    def get_investor_insights(self):

        insights = []

        try:
            investors = overview.get_top_investors(limit=5)

            if investors:

                top_investor = investors[0]

                investor_name = (
                    top_investor["investor_name"]
                )

                investment_count = (
                    top_investor["investments_count"]
                )

                startup_count = (
                    top_investor["startups_invested"]
                )

                insights.append(
                    f"{investor_name} is the most active "
                    f"tracked investor, participating in "
                    f"{investment_count} funding rounds across "
                    f"{startup_count} startups."
                )

                insights.append(
                    "Startup investment activity shows concentration "
                    "among a relatively small group of highly "
                    "active investors."
                )

        except Exception as error:
            insights.append(
                f"Unable to generate investor insights: {error}"
            )

        return insights

    # =========================================================
    # GEOGRAPHIC INSIGHTS
    # =========================================================

    def get_geographic_insights(self):

        insights = []

        try:
            cities = overview.get_top_cities(limit=5)

            if cities:

                top_city = cities[0]

                city = top_city["city"]

                startup_count = (
                    top_city["startup_count"]
                )

                funding = float(
                    top_city["total_funding"] or 0
                )

                insights.append(
                    f"{city} is the leading startup hub in the "
                    f"dataset, with {startup_count} startups and "
                    f"${funding:,.0f} in recorded funding."
                )

                if len(cities) >= 3:

                    top_cities = [
                        city_data["city"]
                        for city_data in cities[:3]
                    ]

                    insights.append(
                        "Startup activity is primarily concentrated "
                        "in major innovation hubs including "
                        + ", ".join(top_cities)
                        + "."
                    )

        except Exception as error:
            insights.append(
                f"Unable to generate geographic insights: {error}"
            )

        return insights

    # =========================================================
    # FORECAST INSIGHTS
    # =========================================================

    def get_forecast_insights(self):

        insights = []

        try:
            forecast = (
                self.forecaster.get_forecast_summary(
                    years_ahead=3
                )
            )

            if forecast.get("status") == "Success":

                forecast_year = (
                    forecast["forecast_year"]
                )

                forecast_funding = (
                    forecast["forecast_funding"]
                )

                projected_change = (
                    forecast[
                        "projected_change_percent"
                    ]
                )

                insights.append(
                    f"Startup funding is projected to reach "
                    f"${forecast_funding:,.0f} by "
                    f"{forecast_year}."
                )

                if projected_change > 0:

                    insights.append(
                        f"This represents a projected "
                        f"{projected_change:.2f}% increase compared "
                        f"with the latest recorded funding level."
                    )

                elif projected_change < 0:

                    insights.append(
                        f"This represents a projected "
                        f"{abs(projected_change):.2f}% decline compared "
                        f"with the latest recorded funding level."
                    )

        except Exception as error:
            insights.append(
                f"Unable to generate forecast insights: {error}"
            )

        return insights

    # =========================================================
    # OPPORTUNITIES
    # =========================================================

    def get_opportunities(self):

        opportunities = []

        try:
            industries = overview.get_top_industries(limit=5)

            if industries:

                top_industry = industries[0]

                opportunities.append(
                    f"The {top_industry['industry_name']} sector "
                    f"shows strong investment activity and may "
                    f"represent a significant opportunity area."
                )

            forecast = (
                self.forecaster.get_forecast_summary(
                    years_ahead=3
                )
            )

            if (
                forecast.get("status") == "Success"
                and forecast.get("projected_change_percent", 0) > 0
            ):

                opportunities.append(
                    "The funding forecast indicates potential "
                    "capital market recovery in the coming years."
                )

            opportunities.append(
                "Emerging startup ecosystems outside dominant "
                "cities may provide opportunities for expansion "
                "and lower competitive pressure."
            )

        except Exception as error:
            opportunities.append(
                f"Unable to identify opportunities: {error}"
            )

        return opportunities

    # =========================================================
    # RISKS
    # =========================================================

    def get_risks(self):

        risks = []

        try:
            trend = (
                self.forecaster.get_trend_analysis()
            )

            if trend.get("trend") == "Declining":

                risks.append(
                    "The declining long-term funding trend may "
                    "increase fundraising challenges for startups."
                )

            historical = (
                self.forecaster.get_historical_funding()
            )

            if not historical.empty:

                latest_funding = float(
                    historical.iloc[-1]["total_funding"]
                )

                peak_funding = float(
                    historical["total_funding"].max()
                )

                if latest_funding < peak_funding * 0.7:

                    risks.append(
                        "Latest funding levels remain significantly "
                        "below historical peak levels."
                    )

            risks.append(
                "High concentration of startup activity in major "
                "cities may create geographic ecosystem dependency."
            )

            risks.append(
                "Heavy dependence on a limited group of active "
                "investors may increase funding concentration risk."
            )

        except Exception as error:
            risks.append(
                f"Unable to identify risks: {error}"
            )

        return risks

    # =========================================================
    # COMPLETE INSIGHT REPORT
    # =========================================================

    def generate_all_insights(self):

        return {

            "executive_insights":
                self.get_executive_insights(),

            "funding_insights":
                self.get_funding_insights(),

            "industry_insights":
                self.get_industry_insights(),

            "startup_insights":
                self.get_startup_insights(),

            "investor_insights":
                self.get_investor_insights(),

            "geographic_insights":
                self.get_geographic_insights(),

            "forecast_insights":
                self.get_forecast_insights(),

            "opportunities":
                self.get_opportunities(),

            "risks":
                self.get_risks()
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    ai = AIInsights()

    insights = ai.generate_all_insights()

    print("\n" + "=" * 60)
    print("VENTURELENS AI INSIGHTS")
    print("=" * 60)

    for category, items in insights.items():

        print(f"\n{category.upper()}")
        print("-" * 60)

        for item in items:
            print(f"• {item}")