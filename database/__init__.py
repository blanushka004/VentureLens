from database.connection import Base, engine

# Import models so SQLAlchemy registers all tables
from database.models import (
    Industry,
    Location,
    Startup,
    Investor,
    FundingRound,
    Investment
)


def initialize_database():

    print("Creating VentureLens database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    initialize_database()