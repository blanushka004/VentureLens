from datetime import datetime

from analytics import overview
from forecasting.funding_generator import FundingForecaster
from ai.insights import AIInsights


class ReportGenerator:
    """
    Generates a complete VentureLens Executive Intelligence Report.

    The report combines:
    - Executive analytics
    - Funding intelligence
    - Industry intelligence
    - Investor intelligence
    - Geographic intelligence
    - Forecasting
    - AI-generated insights
    """

    def __init__(self):

        self.forecaster = FundingForecaster()
        self.ai_insights = AIInsights()

    # =========================================================
    # REPORT METADATA
    # =========================================================

    def get_report_metadata(self):

        return {
            "report_title": "VentureLens Executive Intelligence Report",
            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "data_scope": "Indian Startup Ecosystem",
            "currency": "USD"
        }

    # =========================================================
    # EXECUTIVE SUMMARY
    # =========================================================

    def get_executive_summary(self):

        startups = overview.get_total_startups()
        funding = overview.get_total_funding()
        investors = overview.get_total_investors()
        rounds = overview.get_total_funding_rounds()

        return {
            "total_startups":
                startups.get("total_startups", 0),

            "total_funding":
                float(
                    funding.get(
                        "total_funding",
                        0
                    )
                ),

            "total_investors":
                investors.get(
                    "total_investors",
                    0
                ),

            "total_funding_rounds":
                rounds.get(
                    "total_funding_rounds",
                    0
                )
        }

    # =========================================================
    # FUNDING ANALYSIS
    # =========================================================

    def get_funding_section(self):

        funding_by_year = (
            overview.get_funding_by_year()
        )

        funding_by_type = (
            overview.get_funding_by_type()
        )

        return {
            "funding_by_year":
                funding_by_year,

            "funding_by_type":
                funding_by_type
        }

    # =========================================================
    # INDUSTRY INTELLIGENCE
    # =========================================================

    def get_industry_section(self):

        industries = (
            overview.get_top_industries(
                limit=10
            )
        )

        return {
            "top_industries":
                industries
        }

    # =========================================================
    # STARTUP INTELLIGENCE
    # =========================================================

    def get_startup_section(self):

        startups = (
            overview.get_top_startups(
                limit=10
            )
        )

        return {
            "top_startups":
                startups
        }

    # =========================================================
    # INVESTOR INTELLIGENCE
    # =========================================================

    def get_investor_section(self):

        investors = (
            overview.get_top_investors(
                limit=10
            )
        )

        return {
            "top_investors":
                investors
        }

    # =========================================================
    # GEOGRAPHIC INTELLIGENCE
    # =========================================================

    def get_geographic_section(self):

        cities = (
            overview.get_top_cities(
                limit=10
            )
        )

        return {
            "top_cities":
                cities
        }

    # =========================================================
    # FORECAST SECTION
    # =========================================================

    def get_forecast_section(self):

        forecast_df = (
            self.forecaster.forecast(
                years_ahead=3
            )
        )

        trend_analysis = (
            self.forecaster.get_trend_analysis()
        )

        forecast_summary = (
            self.forecaster.get_forecast_summary(
                years_ahead=3
            )
        )

        forecast_data = []

        if not forecast_df.empty:

            forecast_data = (
                forecast_df.to_dict(
                    orient="records"
                )
            )

        return {
            "forecast":
                forecast_data,

            "trend_analysis":
                trend_analysis,

            "forecast_summary":
                forecast_summary
        }

    # =========================================================
    # AI INSIGHTS SECTION
    # =========================================================

    def get_ai_insights_section(self):

        return (
            self.ai_insights.generate_all_insights()
        )

    # =========================================================
    # COMPLETE REPORT
    # =========================================================

    def generate_report(self):

        report = {

            "metadata":
                self.get_report_metadata(),

            "executive_summary":
                self.get_executive_summary(),

            "funding_intelligence":
                self.get_funding_section(),

            "industry_intelligence":
                self.get_industry_section(),

            "startup_intelligence":
                self.get_startup_section(),

            "investor_intelligence":
                self.get_investor_section(),

            "geographic_intelligence":
                self.get_geographic_section(),

            "forecasting":
                self.get_forecast_section(),

            "ai_insights":
                self.get_ai_insights_section()
        }

        return report

    # =========================================================
    # TEXT REPORT
    # =========================================================

    def generate_text_report(self):

        report = self.generate_report()

        metadata = report["metadata"]
        summary = report["executive_summary"]

        lines = []

        lines.append("=" * 70)
        lines.append(
            metadata["report_title"]
        )
        lines.append("=" * 70)

        lines.append(
            f"Generated: {metadata['generated_at']}"
        )

        lines.append(
            f"Data Scope: {metadata['data_scope']}"
        )

        lines.append("")

        # -----------------------------------------------------
        # EXECUTIVE SUMMARY
        # -----------------------------------------------------

        lines.append(
            "EXECUTIVE SUMMARY"
        )

        lines.append("-" * 70)

        lines.append(
            f"Total Startups: "
            f"{summary['total_startups']:,}"
        )

        lines.append(
            f"Total Funding: "
            f"${summary['total_funding']:,.2f}"
        )

        lines.append(
            f"Total Investors: "
            f"{summary['total_investors']:,}"
        )

        lines.append(
            f"Total Funding Rounds: "
            f"{summary['total_funding_rounds']:,}"
        )

        lines.append("")

        # -----------------------------------------------------
        # AI INSIGHTS
        # -----------------------------------------------------

        lines.append(
            "KEY INTELLIGENCE INSIGHTS"
        )

        lines.append("-" * 70)

        ai_insights = report["ai_insights"]

        for category, insights in ai_insights.items():

            lines.append("")
            lines.append(
                category.replace(
                    "_",
                    " "
                ).upper()
            )

            for insight in insights:

                lines.append(
                    f"• {insight}"
                )

        lines.append("")

        # -----------------------------------------------------
        # FORECAST
        # -----------------------------------------------------

        lines.append(
            "FUNDING FORECAST"
        )

        lines.append("-" * 70)

        forecast_summary = (
            report["forecasting"][
                "forecast_summary"
            ]
        )

        if (
            forecast_summary.get("status")
            == "Success"
        ):

            lines.append(
                f"Latest Funding Year: "
                f"{forecast_summary['latest_year']}"
            )

            lines.append(
                f"Forecast Year: "
                f"{forecast_summary['forecast_year']}"
            )

            lines.append(
                f"Projected Funding: "
                f"${forecast_summary['forecast_funding']:,.2f}"
            )

            lines.append(
                f"Projected Change: "
                f"{forecast_summary['projected_change_percent']:.2f}%"
            )

            lines.append(
                f"Forecast Trend: "
                f"{forecast_summary['trend']}"
            )

        else:

            lines.append(
                "Forecast data unavailable."
            )

        lines.append("")
        lines.append("=" * 70)
        lines.append(
            "END OF VENTURELENS REPORT"
        )
        lines.append("=" * 70)

        return "\n".join(lines)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    generator = ReportGenerator()

    print(
        generator.generate_text_report()
    )