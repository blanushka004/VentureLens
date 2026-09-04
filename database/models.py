from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


# ============================================================
# INDUSTRIES
# ============================================================

class Industry(Base):

    __tablename__ = "industries"

    industry_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    industry_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    startups = relationship(
        "Startup",
        back_populates="industry"
    )


# ============================================================
# LOCATIONS
# ============================================================

class Location(Base):

    __tablename__ = "locations"

    location_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    city: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100),
        default="India",
        nullable=False
    )

    startups = relationship(
        "Startup",
        back_populates="location"
    )


# ============================================================
# STARTUPS
# ============================================================

class Startup(Base):

    __tablename__ = "startups"

    startup_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    startup_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    sub_vertical: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    industry_id: Mapped[int] = mapped_column(
        ForeignKey("industries.industry_id"),
        nullable=False
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.location_id"),
        nullable=False
    )

    industry = relationship(
        "Industry",
        back_populates="startups"
    )

    location = relationship(
        "Location",
        back_populates="startups"
    )

    funding_rounds = relationship(
        "FundingRound",
        back_populates="startup",
        cascade="all, delete-orphan"
    )


# ============================================================
# INVESTORS
# ============================================================

class Investor(Base):

    __tablename__ = "investors"

    investor_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    investor_name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    investments = relationship(
        "Investment",
        back_populates="investor",
        cascade="all, delete-orphan"
    )


# ============================================================
# FUNDING ROUNDS
# ============================================================

class FundingRound(Base):

    __tablename__ = "funding_rounds"

    round_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    startup_id: Mapped[int] = mapped_column(
        ForeignKey("startups.startup_id"),
        nullable=False
    )

    funding_date: Mapped[datetime | None] = mapped_column(
        Date,
        nullable=True
    )

    funding_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    funding_amount_usd: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True
    )

    funding_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    funding_month: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    startup = relationship(
        "Startup",
        back_populates="funding_rounds"
    )

    investments = relationship(
        "Investment",
        back_populates="funding_round",
        cascade="all, delete-orphan"
    )


# ============================================================
# INVESTMENTS
# Bridge Table: Funding Rounds <-> Investors
# ============================================================

class Investment(Base):

    __tablename__ = "investments"

    investment_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    round_id: Mapped[int] = mapped_column(
        ForeignKey("funding_rounds.round_id"),
        nullable=False
    )

    investor_id: Mapped[int] = mapped_column(
        ForeignKey("investors.investor_id"),
        nullable=False
    )

    funding_round = relationship(
        "FundingRound",
        back_populates="investments"
    )

    investor = relationship(
        "Investor",
        back_populates="investments"
    )

    __table_args__ = (
        UniqueConstraint(
            "round_id",
            "investor_id",
            name="unique_round_investor"
        ),
    )