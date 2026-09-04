import numpy as np
import pandas as pd

from sqlalchemy import text
from sklearn.linear_model import LinearRegression

from database.connection import engine


class FundingForecaster:
    """
    Forecasts future startup funding trends using historical
    funding data stored in PostgreSQL.
    """

    def __init__(self):
        self.engine = engine
        self.model = LinearRegression()

    # =========================================================
    # LOAD HISTORICAL FUNDING DATA
    # =========================================================

    def get_historical_funding(self):
        """
        Fetch total startup funding grouped by year.
        """

        query = text("""
            SELECT
                funding_year AS year,
                SUM(funding_amount_usd) AS total_funding
            FROM funding_rounds
            WHERE funding_year IS NOT NULL
              AND funding_amount_usd IS NOT NULL
            GROUP BY funding_year
            ORDER BY funding_year;
        """)

        try:
            df = pd.read_sql(query, self.engine)

            if df.empty:
                return pd.DataFrame(
                    columns=["year", "total_funding"]
                )

            df["year"] = df["year"].astype(int)

            df["total_funding"] = pd.to_numeric(
                df["total_funding"],
                errors="coerce"
            )

            df = df.dropna()

            return df

        except Exception as error:
            print(
                f"Error loading historical funding data: {error}"
            )

            return pd.DataFrame(
                columns=["year", "total_funding"]
            )

    # =========================================================
    # PREPARE DATA
    # =========================================================

    def prepare_data(self):
        """
        Prepare historical funding data for machine learning.
        """

        df = self.get_historical_funding()

        if df.empty or len(df) < 2:
            return None, None, df

        X = df[["year"]]
        y = df["total_funding"]

        return X, y, df

    # =========================================================
    # TRAIN MODEL
    # =========================================================

    def train_model(self):
        """
        Train Linear Regression model using historical funding.
        """

        X, y, _ = self.prepare_data()

        if X is None:
            return None

        self.model.fit(X, y)

        return self.model

    # =========================================================
    # GENERATE FORECAST
    # =========================================================

    def forecast(self, years_ahead=3):
        """
        Predict total startup funding for future years.
        """

        historical_df = self.get_historical_funding()

        if historical_df.empty or len(historical_df) < 2:
            return pd.DataFrame(
                columns=[
                    "year",
                    "predicted_funding",
                    "growth_rate"
                ]
            )

        model = self.train_model()

        if model is None:
            return pd.DataFrame(
                columns=[
                    "year",
                    "predicted_funding",
                    "growth_rate"
                ]
            )

        last_year = int(
            historical_df["year"].max()
        )

        future_years = np.arange(
            last_year + 1,
            last_year + years_ahead + 1
        )

        future_df = pd.DataFrame({
            "year": future_years
        })

        predictions = model.predict(
            future_df[["year"]]
        )

        # Funding cannot be negative
        predictions = np.maximum(predictions, 0)

        forecast_df = pd.DataFrame({
            "year": future_years,
            "predicted_funding": predictions
        })

        # Calculate year-over-year predicted growth
        growth_rates = []

        previous_value = float(
            historical_df.iloc[-1]["total_funding"]
        )

        for prediction in predictions:

            if previous_value > 0:
                growth = (
                    (prediction - previous_value)
                    / previous_value
                ) * 100
            else:
                growth = 0

            growth_rates.append(
                round(float(growth), 2)
            )

            previous_value = prediction

        forecast_df["growth_rate"] = growth_rates

        return forecast_df

    # =========================================================
    # COMBINE HISTORICAL + FORECAST DATA
    # =========================================================

    def get_forecast_comparison(self, years_ahead=3):
        """
        Return historical and forecast funding data together.
        Useful for Streamlit visualizations.
        """

        historical_df = self.get_historical_funding()
        forecast_df = self.forecast(years_ahead)

        if historical_df.empty:
            return pd.DataFrame(
                columns=[
                    "year",
                    "funding",
                    "type"
                ]
            )

        historical = historical_df.copy()

        historical = historical.rename(
            columns={
                "total_funding": "funding"
            }
        )

        historical["type"] = "Historical"

        if forecast_df.empty:
            return historical[
                ["year", "funding", "type"]
            ]

        forecast_data = forecast_df.copy()

        forecast_data = forecast_data.rename(
            columns={
                "predicted_funding": "funding"
            }
        )

        forecast_data["type"] = "Forecast"

        combined = pd.concat(
            [
                historical[
                    ["year", "funding", "type"]
                ],
                forecast_data[
                    ["year", "funding", "type"]
                ]
            ],
            ignore_index=True
        )

        return combined

    # =========================================================
    # TREND ANALYSIS
    # =========================================================

    def get_trend_analysis(self):
        """
        Analyze the overall historical funding trend.
        """

        df = self.get_historical_funding()

        if df.empty or len(df) < 2:
            return {
                "trend": "Insufficient Data",
                "growth_rate": 0.0,
                "slope": 0.0,
                "message": (
                    "Not enough historical funding data "
                    "for trend analysis."
                )
            }

        first_value = float(
            df.iloc[0]["total_funding"]
        )

        last_value = float(
            df.iloc[-1]["total_funding"]
        )

        if first_value > 0:
            growth_rate = (
                (last_value - first_value)
                / first_value
            ) * 100
        else:
            growth_rate = 0.0

        model = self.train_model()

        if model is None:
            slope = 0.0
        else:
            slope = float(model.coef_[0])

        if slope > 0:
            trend = "Growing"
        elif slope < 0:
            trend = "Declining"
        else:
            trend = "Stable"

        return {
            "trend": trend,
            "growth_rate": round(
                growth_rate,
                2
            ),
            "slope": round(
                slope,
                2
            ),
            "message": (
                f"Startup funding is showing a "
                f"{trend.lower()} long-term trend."
            )
        }

    # =========================================================
    # FORECAST SUMMARY
    # =========================================================

    def get_forecast_summary(self, years_ahead=3):
        """
        Generate a business-friendly forecast summary.
        """

        historical_df = self.get_historical_funding()

        forecast_df = self.forecast(
            years_ahead
        )

        if (
            historical_df.empty
            or forecast_df.empty
        ):
            return {
                "status": "No Data",
                "message": (
                    "Insufficient historical funding data "
                    "to generate forecast."
                )
            }

        latest_year = int(
            historical_df.iloc[-1]["year"]
        )

        latest_funding = float(
            historical_df.iloc[-1]["total_funding"]
        )

        forecast_year = int(
            forecast_df.iloc[-1]["year"]
        )

        forecast_funding = float(
            forecast_df.iloc[-1]["predicted_funding"]
        )

        if latest_funding > 0:
            projected_change = (
                (forecast_funding - latest_funding)
                / latest_funding
            ) * 100
        else:
            projected_change = 0.0

        if projected_change > 0:
            trend = "Growth"
        elif projected_change < 0:
            trend = "Decline"
        else:
            trend = "Stable"

        return {
            "status": "Success",
            "latest_year": latest_year,
            "latest_funding": latest_funding,
            "forecast_year": forecast_year,
            "forecast_funding": forecast_funding,
            "projected_change_percent": round(
                projected_change,
                2
            ),
            "trend": trend,
            "forecast_period": years_ahead
        }


# =========================================================
# QUICK TEST
# =========================================================

if __name__ == "__main__":

    forecaster = FundingForecaster()

    print("\nHISTORICAL FUNDING")
    print("-" * 50)
    print(
        forecaster.get_historical_funding()
    )

    print("\nFUNDING FORECAST")
    print("-" * 50)
    print(
        forecaster.forecast(
            years_ahead=3
        )
    )

    print("\nTREND ANALYSIS")
    print("-" * 50)
    print(
        forecaster.get_trend_analysis()
    )

    print("\nFORECAST SUMMARY")
    print("-" * 50)
    print(
        forecaster.get_forecast_summary(
            years_ahead=3
        )
    )