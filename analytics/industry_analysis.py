from analytics.overview import execute_query


# ============================================================
# INDUSTRY OVERVIEW
# ============================================================

def get_industry_overview():

    query = """
        SELECT
            i.industry_name,

            COUNT(DISTINCT s.startup_id)
                AS startup_count,

            COUNT(fr.round_id)
                AS funding_rounds,

            SUM(fr.funding_amount_usd)
                AS total_funding,

            AVG(fr.funding_amount_usd)
                AS average_funding

        FROM industries i

        LEFT JOIN startups s
            ON i.industry_id = s.industry_id

        LEFT JOIN funding_rounds fr
            ON s.startup_id = fr.startup_id

        GROUP BY i.industry_name

        ORDER BY total_funding DESC NULLS LAST;
    """

    return execute_query(query)


# ============================================================
# INDUSTRY FUNDING TREND
# ============================================================

def get_industry_funding_trend():

    query = """
        SELECT
            fr.funding_year,

            i.industry_name,

            SUM(fr.funding_amount_usd)
                AS total_funding,

            COUNT(fr.round_id)
                AS funding_rounds

        FROM funding_rounds fr

        JOIN startups s
            ON fr.startup_id = s.startup_id

        JOIN industries i
            ON s.industry_id = i.industry_id

        GROUP BY
            fr.funding_year,
            i.industry_name

        ORDER BY
            fr.funding_year,
            total_funding DESC;
    """

    return execute_query(query)


# ============================================================
# TOP INDUSTRIES BY FUNDING
# ============================================================

def get_top_industries_by_funding(limit=10):

    query = """
        SELECT
            i.industry_name,

            SUM(fr.funding_amount_usd)
                AS total_funding,

            COUNT(fr.round_id)
                AS funding_rounds,

            COUNT(DISTINCT s.startup_id)
                AS startups

        FROM industries i

        JOIN startups s
            ON i.industry_id = s.industry_id

        JOIN funding_rounds fr
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
# INDUSTRY GROWTH
# ============================================================

def get_industry_growth():

    query = """
        WITH industry_yearly AS (

            SELECT
                i.industry_name,
                fr.funding_year,

                SUM(fr.funding_amount_usd)
                    AS total_funding

            FROM funding_rounds fr

            JOIN startups s
                ON fr.startup_id = s.startup_id

            JOIN industries i
                ON s.industry_id = i.industry_id

            GROUP BY
                i.industry_name,
                fr.funding_year
        )

        SELECT
            industry_name,
            funding_year,
            total_funding,

            LAG(total_funding)
                OVER (
                    PARTITION BY industry_name
                    ORDER BY funding_year
                )
                AS previous_year_funding,

            ROUND(
                (
                    (
                        total_funding
                        -
                        LAG(total_funding)
                            OVER (
                                PARTITION BY industry_name
                                ORDER BY funding_year
                            )
                    )
                    /
                    NULLIF(
                        LAG(total_funding)
                            OVER (
                                PARTITION BY industry_name
                                ORDER BY funding_year
                            ),
                        0
                    )
                ) * 100,
                2
            )
            AS growth_percentage

        FROM industry_yearly

        ORDER BY
            industry_name,
            funding_year;
    """

    return execute_query(query)


# ============================================================
# INDUSTRY MARKET SHARE
# ============================================================

def get_industry_market_share():

    query = """
        WITH industry_funding AS (

            SELECT
                i.industry_name,

                SUM(fr.funding_amount_usd)
                    AS total_funding

            FROM industries i

            JOIN startups s
                ON i.industry_id = s.industry_id

            JOIN funding_rounds fr
                ON s.startup_id = fr.startup_id

            GROUP BY i.industry_name
        )

        SELECT
            industry_name,

            total_funding,

            ROUND(
                (
                    total_funding
                    /
                    SUM(total_funding) OVER ()
                ) * 100,
                2
            )
            AS market_share_percentage

        FROM industry_funding

        ORDER BY total_funding DESC;
    """

    return execute_query(query)