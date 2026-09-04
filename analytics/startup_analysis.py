from sqlalchemy import text

from database.connection import engine


# ============================================================
# STARTUP OVERVIEW
# ============================================================

def get_startup_overview():

    query = text("""
        SELECT
            COUNT(DISTINCT s.startup_id) AS total_startups,
            COUNT(DISTINCT s.industry_id) AS total_industries,
            COUNT(DISTINCT s.location_id) AS total_locations,
            COUNT(DISTINCT fr.startup_id) AS funded_startups
        FROM startups s
        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id
    """)

    with engine.connect() as conn:

        result = conn.execute(query).fetchone()

        return dict(result._mapping)


# ============================================================
# TOP FUNDED STARTUPS
# ============================================================

def get_top_funded_startups(limit=10):

    query = text("""
        SELECT
            s.startup_name,
            ind.industry_name,
            l.city,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM startups s
        JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id
        JOIN industries ind
            ON s.industry_id = ind.industry_id
        JOIN locations l
            ON s.location_id = l.location_id
        GROUP BY
            s.startup_name,
            ind.industry_name,
            l.city
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
# MOST ACTIVE STARTUPS
# ============================================================

def get_most_active_startups(limit=10):

    query = text("""
        SELECT
            s.startup_name,
            ind.industry_name,
            l.city,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding,
            MAX(fr.funding_year) AS latest_funding_year
        FROM startups s
        JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id
        JOIN industries ind
            ON s.industry_id = ind.industry_id
        JOIN locations l
            ON s.location_id = l.location_id
        GROUP BY
            s.startup_name,
            ind.industry_name,
            l.city
        ORDER BY
            funding_rounds DESC,
            total_funding DESC
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
# STARTUP FUNDING HISTORY
# ============================================================

def get_startup_funding_history(startup_name):

    query = text("""
        SELECT
            s.startup_name,
            fr.funding_date,
            fr.funding_year,
            fr.funding_type,
            fr.funding_amount_usd
        FROM startups s
        JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id
        WHERE LOWER(s.startup_name) = LOWER(:startup_name)
        ORDER BY fr.funding_date
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {"startup_name": startup_name}
        )

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# STARTUP DISTRIBUTION BY INDUSTRY
# ============================================================

def get_startup_distribution_by_industry():

    query = text("""
        SELECT
            ind.industry_name,
            COUNT(s.startup_id) AS startup_count,
            COUNT(fr.round_id) AS funding_rounds,
            COALESCE(SUM(fr.funding_amount_usd), 0) AS total_funding
        FROM industries ind
        LEFT JOIN startups s
            ON ind.industry_id = s.industry_id
        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id
        GROUP BY ind.industry_name
        ORDER BY startup_count DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# STARTUP DISTRIBUTION BY CITY
# ============================================================

def get_startup_distribution_by_city():

    query = text("""
        SELECT
            l.city,
            COUNT(DISTINCT s.startup_id) AS startup_count,
            COUNT(fr.round_id) AS funding_rounds,
            COALESCE(SUM(fr.funding_amount_usd), 0) AS total_funding
        FROM locations l
        LEFT JOIN startups s
            ON l.location_id = s.location_id
        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id
        GROUP BY l.city
        ORDER BY startup_count DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# RECENTLY FUNDED STARTUPS
# ============================================================

def get_recently_funded_startups(limit=10):

    query = text("""
        SELECT
            s.startup_name,
            ind.industry_name,
            l.city,
            fr.funding_date,
            fr.funding_year,
            fr.funding_type,
            fr.funding_amount_usd
        FROM funding_rounds fr
        JOIN startups s
            ON fr.startup_id = s.startup_id
        JOIN industries ind
            ON s.industry_id = ind.industry_id
        JOIN locations l
            ON s.location_id = l.location_id
        ORDER BY fr.funding_date DESC
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
# STARTUP FUNDING MOMENTUM
# ============================================================

def get_startup_funding_momentum():

    query = text("""
        SELECT
            s.startup_name,
            ind.industry_name,

            SUM(
                CASE
                    WHEN fr.funding_year >= 2024
                    THEN fr.funding_amount_usd
                    ELSE 0
                END
            ) AS recent_funding,

            SUM(
                CASE
                    WHEN fr.funding_year < 2024
                    THEN fr.funding_amount_usd
                    ELSE 0
                END
            ) AS previous_funding,

            COUNT(
                CASE
                    WHEN fr.funding_year >= 2024
                    THEN 1
                END
            ) AS recent_rounds

        FROM startups s

        JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        JOIN industries ind
            ON s.industry_id = ind.industry_id

        GROUP BY
            s.startup_name,
            ind.industry_name

        ORDER BY recent_funding DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]
