from decimal import Decimal

from sqlalchemy import select

from database.connection import SessionLocal
from database.models import (
    Industry,
    Location,
    Startup,
    Investor,
    FundingRound,
    Investment
)

from etl.extract import extract_data
from etl.transform import transform_data


def get_or_create_industry(session, industry_name):

    industry = session.scalar(
        select(Industry).where(
            Industry.industry_name == industry_name
        )
    )

    if not industry:
        industry = Industry(
            industry_name=industry_name
        )

        session.add(industry)
        session.flush()

    return industry


def get_or_create_location(session, city):

    location = session.scalar(
        select(Location).where(
            Location.city == city
        )
    )

    if not location:
        location = Location(
            city=city,
            country="India"
        )

        session.add(location)
        session.flush()

    return location


def get_or_create_startup(
    session,
    startup_name,
    sub_vertical,
    industry,
    location
):

    startup = session.scalar(
        select(Startup).where(
            Startup.startup_name == startup_name
        )
    )

    if not startup:

        startup = Startup(
            startup_name=startup_name,
            sub_vertical=sub_vertical,
            industry_id=industry.industry_id,
            location_id=location.location_id
        )

        session.add(startup)
        session.flush()

    return startup


def get_or_create_investor(session, investor_name):

    investor = session.scalar(
        select(Investor).where(
            Investor.investor_name == investor_name
        )
    )

    if not investor:

        investor = Investor(
            investor_name=investor_name
        )

        session.add(investor)
        session.flush()

    return investor


def split_investors(investors_string):

    if not investors_string:
        return []

    investors = [
        investor.strip()
        for investor in investors_string.split(",")
        if investor.strip()
    ]

    return investors


def load_data():

    print("\nStarting VentureLens ETL Load...")

    # --------------------------------------------------
    # EXTRACT + TRANSFORM
    # --------------------------------------------------

    raw_data = extract_data()

    df = transform_data(raw_data)

    session = SessionLocal()

    try:

        # --------------------------------------------------
        # LOAD RECORDS
        # --------------------------------------------------

        for index, row in df.iterrows():

            # INDUSTRY
            industry = get_or_create_industry(
                session,
                row["Industry"]
            )

            # LOCATION
            location = get_or_create_location(
                session,
                row["City"]
            )

            # STARTUP
            startup = get_or_create_startup(
                session=session,
                startup_name=row["Startup"],
                sub_vertical=row["SubVertical"],
                industry=industry,
                location=location
            )

            # FUNDING ROUND
            funding_round = FundingRound(

                startup_id=startup.startup_id,

                funding_date=row["Date"].date(),

                funding_type=row["InvestmentType"],

                funding_amount_usd=Decimal(
                    str(row["InvestmentAmount_USD"])
                ),

                funding_year=int(row["FundingYear"]),

                funding_month=int(row["FundingMonth"])
            )

            session.add(funding_round)

            session.flush()

            # --------------------------------------------------
            # INVESTORS
            # --------------------------------------------------

            investor_names = split_investors(
                row["Investors"]
            )

            for investor_name in investor_names:

                investor = get_or_create_investor(
                    session,
                    investor_name
                )

                investment = Investment(

                    round_id=funding_round.round_id,

                    investor_id=investor.investor_id
                )

                session.add(investment)

            # Progress indicator
            if (index+1) % 100 == 0:

                print(
                    f"Loaded {index + 1} / {len(df)} records"
                )

        # --------------------------------------------------
        # COMMIT
        # --------------------------------------------------

        session.commit()

        print("\nVentureLens data loaded successfully!")

        print(f"Total funding records loaded: {len(df)}")

    except Exception as error:

        session.rollback()

        print("\nERROR OCCURRED DURING DATA LOADING")

        print(error)

        raise

    finally:

        session.close()


if __name__ == "__main__":

    load_data()
    
    