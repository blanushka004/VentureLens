from sqlalchemy import text

from database.connection import engine


# ============================================================
# GENERIC QUERY EXECUTOR
# ============================================================

def execute_query(query, params=None):

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            params or {}
        )

        return [
            dict(row._mapping)
            for row in result
        ]


# ============================================================
# TOTAL STARTUPS
# ============================================================

def get_total_startups():

    query = """
        SELECT
            COUNT(*) AS total_startups
        FROM startups;
    """

    return execute_query(query)[0]


# ============================================================
# TOTAL FUNDING
# ============================================================

def get_total_funding():

    query = """
        SELECT
            COALESCE(
                SUM(funding_amount_usd),
                0
            ) AS total_funding
        FROM funding_rounds;
    """

    return execute_query(query)[0]


# ============================================================
# TOTAL INVESTORS
# ============================================================

def get_total_investors():

    query = """
        SELECT
            COUNT(*) AS total_investors
        FROM investors;
    """

    return execute_query(query)[0]


# ============================================================
# TOTAL FUNDING ROUNDS
# ============================================================

def get_total_funding_rounds():

    query = """
        SELECT
            COUNT(*) AS total_funding_rounds
        FROM funding_rounds;
    """

    return execute_query(query)[0]


# ============================================================
# FUNDING BY YEAR
# ============================================================

def get_funding_by_year():

    query = """
        SELECT
            funding_year,

            COUNT(*) AS funding_rounds,

            SUM(funding_amount_usd) AS total_funding

        FROM funding_rounds

        GROUP BY funding_year

        ORDER BY funding_year;
    """

    return execute_query(query)


# ============================================================
# FUNDING BY TYPE
# ============================================================

def get_funding_by_type():

    query = """
        SELECT
            funding_type,

            COUNT(*) AS funding_rounds,

            SUM(funding_amount_usd) AS total_funding

        FROM funding_rounds

        GROUP BY funding_type

        ORDER BY total_funding DESC;
    """

    return execute_query(query)


# ============================================================
# TOP INDUSTRIES
# ============================================================

def get_top_industries(limit=10):

    query = """
        SELECT
            i.industry_name,

            COUNT(DISTINCT s.startup_id)
                AS startup_count,

            COUNT(fr.round_id)
                AS funding_rounds,

            COALESCE(
                SUM(fr.funding_amount_usd),
                0
            ) AS total_funding

        FROM industries i

        LEFT JOIN startups s
            ON i.industry_id = s.industry_id

        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        GROUP BY i.industry_name

        ORDER BY total_funding DESC

        LIMIT :limit;
    """

    return execute_query(
        query,
        {"limit": limit}
    )


# ============================================================
# TOP STARTUPS
# ============================================================

def get_top_startups(limit=10):

    query = """
        SELECT
            s.startup_name,

            i.industry_name,

            l.city,

            COUNT(fr.round_id)
                AS funding_rounds,

            COALESCE(
                SUM(fr.funding_amount_usd),
                0
            ) AS total_funding

        FROM startups s

        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        JOIN industries i
            ON s.industry_id = i.industry_id

        JOIN locations l
            ON s.location_id = l.location_id

        GROUP BY
            s.startup_name,
            i.industry_name,
            l.city

        ORDER BY total_funding DESC

        LIMIT :limit;
    """

    return execute_query(
        query,
        {"limit": limit}
    )


# ============================================================
# TOP INVESTORS
# ============================================================

def get_top_investors(limit=10):

    query = """
        SELECT
            i.investor_name,

            COUNT(inv.investment_id)
                AS investments_count,

            COUNT(DISTINCT fr.startup_id)
                AS startups_invested

        FROM investors i

        JOIN investments inv
            ON i.investor_id = inv.investor_id

        JOIN funding_rounds fr
            ON inv.round_id = fr.round_id

        GROUP BY i.investor_name

        ORDER BY investments_count DESC

        LIMIT :limit;
    """

    return execute_query(
        query,
        {"limit": limit}
    )


# ============================================================
# TOP CITIES
# ============================================================

def get_top_cities(limit=10):

    query = """
        SELECT
            l.city,

            COUNT(DISTINCT s.startup_id)
                AS startup_count,

            COUNT(fr.round_id)
                AS funding_rounds,

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

        LIMIT :limit;
    """

    return execute_query(
        query,
        {"limit": limit}
    )