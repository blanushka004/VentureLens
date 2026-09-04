from sqlalchemy import text

from database.connection import engine


# ============================================================
# GEOGRAPHIC OVERVIEW
# ============================================================

def get_geographic_overview():

    query = text("""
        SELECT
            COUNT(DISTINCT l.location_id) AS total_cities,
            COUNT(DISTINCT s.startup_id) AS total_startups,
            COUNT(DISTINCT s.industry_id) AS industries_present,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM locations l
        LEFT JOIN startups s
            ON l.location_id = s.location_id
        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id
    """)

    with engine.connect() as conn:

        result = conn.execute(query).fetchone()

        return dict(result._mapping)


# ============================================================
# CITY-WISE STARTUP ECOSYSTEM
# ============================================================

def get_city_ecosystem():

    query = text("""
        SELECT
            l.city,

            COUNT(DISTINCT s.startup_id) AS startup_count,

            COUNT(DISTINCT s.industry_id) AS industries_present,

            COUNT(DISTINCT fr.round_id) AS funding_rounds,

            COALESCE(
                SUM(fr.funding_amount_usd),
                0
            ) AS total_funding

        FROM locations l

        LEFT JOIN startups s
            ON l.location_id = s.location_id

        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        GROUP BY l.city

        ORDER BY total_funding DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# TOP CITIES BY STARTUP COUNT
# ============================================================

def get_top_cities_by_startups(limit=10):

    query = text("""
        SELECT
            l.city,

            COUNT(DISTINCT s.startup_id) AS startup_count

        FROM locations l

        JOIN startups s
            ON l.location_id = s.location_id

        GROUP BY l.city

        ORDER BY startup_count DESC

        LIMIT :limit
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {"limit": limit}
        )

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# TOP CITIES BY FUNDING
# ============================================================

def get_top_cities_by_funding(limit=10):

    query = text("""
        SELECT
            l.city,

            COUNT(DISTINCT s.startup_id) AS startups_funded,

            COUNT(fr.round_id) AS funding_rounds,

            SUM(fr.funding_amount_usd) AS total_funding

        FROM locations l

        JOIN startups s
            ON l.location_id = s.location_id

        JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        GROUP BY l.city

        ORDER BY total_funding DESC

        LIMIT :limit
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {"limit": limit}
        )

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# INDUSTRY DISTRIBUTION BY CITY
# ============================================================

def get_city_industry_distribution():

    query = text("""
        SELECT
            l.city,

            ind.industry_name,

            COUNT(DISTINCT s.startup_id) AS startup_count,

            COALESCE(
                SUM(fr.funding_amount_usd),
                0
            ) AS total_funding

        FROM startups s

        JOIN locations l
            ON s.location_id = l.location_id

        JOIN industries ind
            ON s.industry_id = ind.industry_id

        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        GROUP BY
            l.city,
            ind.industry_name

        ORDER BY
            l.city,
            total_funding DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# LEADING INDUSTRY IN EACH CITY
# ============================================================

def get_city_leading_industries():

    query = text("""
        WITH city_industry AS (

            SELECT
                l.city,

                ind.industry_name,

                COUNT(DISTINCT s.startup_id) AS startup_count,

                COALESCE(
                    SUM(fr.funding_amount_usd),
                    0
                ) AS total_funding

            FROM startups s

            JOIN locations l
                ON s.location_id = l.location_id

            JOIN industries ind
                ON s.industry_id = ind.industry_id

            LEFT JOIN funding_rounds fr
                ON s.startup_id = fr.startup_id

            GROUP BY
                l.city,
                ind.industry_name
        ),

        ranked_industries AS (

            SELECT
                *,
                RANK() OVER (
                    PARTITION BY city
                    ORDER BY total_funding DESC
                ) AS industry_rank

            FROM city_industry
        )

        SELECT
            city,
            industry_name,
            startup_count,
            total_funding

        FROM ranked_industries

        WHERE industry_rank = 1

        ORDER BY total_funding DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# CITY FUNDING GROWTH BY YEAR
# ============================================================

def get_city_funding_growth():

    query = text("""
        SELECT
            l.city,

            fr.funding_year,

            COUNT(fr.round_id) AS funding_rounds,

            SUM(fr.funding_amount_usd) AS total_funding

        FROM funding_rounds fr

        JOIN startups s
            ON fr.startup_id = s.startup_id

        JOIN locations l
            ON s.location_id = l.location_id

        GROUP BY
            l.city,
            fr.funding_year

        ORDER BY
            l.city,
            fr.funding_year
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# CITY FUNDING CONCENTRATION
# ============================================================

def get_city_funding_concentration():

    query = text("""
        WITH city_funding AS (

            SELECT
                l.city,

                SUM(fr.funding_amount_usd) AS total_funding

            FROM funding_rounds fr

            JOIN startups s
                ON fr.startup_id = s.startup_id

            JOIN locations l
                ON s.location_id = l.location_id

            GROUP BY l.city
        )

        SELECT
            city,

            total_funding,

            ROUND(
                (
                    total_funding
                    /
                    SUM(total_funding) OVER ()
                ) * 100,
                2
            ) AS funding_percentage

        FROM city_funding

        ORDER BY total_funding DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# AVERAGE FUNDING PER STARTUP BY CITY
# ============================================================

def get_city_average_funding():

    query = text("""
        SELECT
            l.city,

            COUNT(DISTINCT s.startup_id) AS startup_count,

            SUM(fr.funding_amount_usd) AS total_funding,

            ROUND(
                SUM(fr.funding_amount_usd)
                /
                COUNT(DISTINCT s.startup_id),
                2
            ) AS average_funding_per_startup

        FROM locations l

        JOIN startups s
            ON l.location_id = s.location_id

        JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        GROUP BY l.city

        ORDER BY average_funding_per_startup DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# CITY INVESTMENT ACTIVITY
# ============================================================
def get_city_investment_activity():
    query = text("""
        WITH city_funding AS (
            SELECT
                l.city,
                COUNT(DISTINCT s.startup_id) AS startups,
                COUNT(DISTINCT fr.round_id) AS funding_rounds,
                COALESCE(SUM(fr.funding_amount_usd), 0) AS total_funding

            FROM locations l

            JOIN startups s
                ON l.location_id = s.location_id

            LEFT JOIN funding_rounds fr
                ON s.startup_id = fr.startup_id

            GROUP BY l.city
        ),

        city_investors AS (
            SELECT
                l.city,
                COUNT(DISTINCT i.investor_id) AS active_investors

            FROM locations l

            JOIN startups s
                ON l.location_id = s.location_id

            JOIN funding_rounds fr
                ON s.startup_id = fr.startup_id

            JOIN investments i
                ON fr.round_id = i.round_id

            GROUP BY l.city
        )

        SELECT
            cf.city,
            cf.startups,
            cf.funding_rounds,
            COALESCE(ci.active_investors, 0) AS active_investors,
            cf.total_funding

        FROM city_funding cf

        LEFT JOIN city_investors ci
            ON cf.city = ci.city

        ORDER BY cf.total_funding DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]