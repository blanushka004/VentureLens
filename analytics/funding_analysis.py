from analytics.overview import execute_query


# ============================================================
# FUNDING SUMMARY
# ============================================================

def get_funding_summary():

    query = """
        SELECT
            COUNT(*) AS total_rounds,

            SUM(funding_amount_usd) AS total_funding,

            AVG(funding_amount_usd) AS average_funding,

            MAX(funding_amount_usd) AS largest_round,

            MIN(funding_amount_usd) AS smallest_round

        FROM funding_rounds;
    """

    return execute_query(query)[0]


# ============================================================
# FUNDING TREND BY YEAR
# ============================================================

def get_yearly_funding_trend():

    query = """
        SELECT
            funding_year,

            COUNT(*) AS funding_rounds,

            SUM(funding_amount_usd) AS total_funding,

            AVG(funding_amount_usd) AS average_funding

        FROM funding_rounds

        GROUP BY funding_year

        ORDER BY funding_year;
    """

    return execute_query(query)


# ============================================================
# FUNDING TREND BY QUARTER
# ============================================================

def get_quarterly_funding_trend():

    query = """
        SELECT
            funding_year,

            CASE
                WHEN funding_month BETWEEN 1 AND 3 THEN 'Q1'
                WHEN funding_month BETWEEN 4 AND 6 THEN 'Q2'
                WHEN funding_month BETWEEN 7 AND 9 THEN 'Q3'
                WHEN funding_month BETWEEN 10 AND 12 THEN 'Q4'
            END AS quarter,

            COUNT(*) AS funding_rounds,

            SUM(funding_amount_usd) AS total_funding

        FROM funding_rounds

        GROUP BY
            funding_year,
            quarter

        ORDER BY
            funding_year,
            quarter;
    """

    return execute_query(query)


# ============================================================
# FUNDING BY TYPE
# ============================================================

def get_funding_distribution_by_type():

    query = """
        SELECT
            funding_type,

            COUNT(*) AS funding_rounds,

            SUM(funding_amount_usd) AS total_funding,

            AVG(funding_amount_usd) AS average_funding

        FROM funding_rounds

        GROUP BY funding_type

        ORDER BY total_funding DESC;
    """

    return execute_query(query)


# ============================================================
# FUNDING TYPE BY YEAR
# ============================================================

def get_funding_type_trend():

    query = """
        SELECT
            funding_year,
            funding_type,

            COUNT(*) AS funding_rounds,

            SUM(funding_amount_usd) AS total_funding

        FROM funding_rounds

        GROUP BY
            funding_year,
            funding_type

        ORDER BY
            funding_year,
            total_funding DESC;
    """

    return execute_query(query)


# ============================================================
# LARGEST FUNDING ROUNDS
# ============================================================

def get_largest_funding_rounds(limit=20):

    query = """
        SELECT
            s.startup_name,

            i.industry_name,

            l.city,

            fr.funding_date,

            fr.funding_type,

            fr.funding_amount_usd

        FROM funding_rounds fr

        JOIN startups s
            ON fr.startup_id = s.startup_id

        JOIN industries i
            ON s.industry_id = i.industry_id

        JOIN locations l
            ON s.location_id = l.location_id

        ORDER BY fr.funding_amount_usd DESC

        LIMIT :limit;
    """

    return execute_query(
        query,
        {"limit": limit}
    )


# ============================================================
# FUNDING GROWTH
# ============================================================

def get_year_over_year_growth():

    query = """
        WITH yearly_funding AS (

            SELECT
                funding_year,

                SUM(funding_amount_usd) AS total_funding

            FROM funding_rounds

            GROUP BY funding_year
        )

        SELECT
            funding_year,

            total_funding,

            LAG(total_funding)
                OVER (ORDER BY funding_year)
                AS previous_year_funding,

            ROUND(
                (
                    (
                        total_funding
                        -
                        LAG(total_funding)
                            OVER (ORDER BY funding_year)
                    )
                    /
                    NULLIF(
                        LAG(total_funding)
                            OVER (ORDER BY funding_year),
                        0
                    )
                ) * 100,
                2
            ) AS growth_percentage

        FROM yearly_funding

        ORDER BY funding_year;
    """

    return execute_query(query)


# ============================================================
# MONTHLY FUNDING TREND
# ============================================================

def get_monthly_funding_trend():

    query = """
        SELECT
            funding_year,
            funding_month,

            COUNT(*) AS funding_rounds,

            SUM(funding_amount_usd) AS total_funding

        FROM funding_rounds

        GROUP BY
            funding_year,
            funding_month

        ORDER BY
            funding_year,
            funding_month;
    """

    return execute_query(query)