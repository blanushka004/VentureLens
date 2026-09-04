from sqlalchemy import text
from database.connection import engine


# ============================================================
# OLAP ANALYTICS QUERIES
# ============================================================


# ============================================================
# 1. ROLL-UP OPERATIONS
# ============================================================

def funding_rollup_by_year():

    query = text("""
        SELECT
            fr.funding_year,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM funding_rounds fr
        GROUP BY fr.funding_year
        ORDER BY fr.funding_year;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


def funding_rollup_by_city():

    query = text("""
        SELECT
            l.city,
            COUNT(DISTINCT s.startup_id) AS startup_count,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM funding_rounds fr
        JOIN startups s ON fr.startup_id = s.startup_id
        JOIN locations l ON s.location_id = l.location_id
        GROUP BY l.city
        ORDER BY total_funding DESC;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


def funding_rollup_by_industry():

    query = text("""
        SELECT
            i.industry_name,
            COUNT(DISTINCT s.startup_id) AS startup_count,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM funding_rounds fr
        JOIN startups s ON fr.startup_id = s.startup_id
        JOIN industries i ON s.industry_id = i.industry_id
        GROUP BY i.industry_name
        ORDER BY total_funding DESC;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


# ============================================================
# 2. DRILL-DOWN OPERATIONS
# ============================================================

def funding_drilldown_year_to_month():

    query = text("""
        SELECT
            fr.funding_year,
            fr.funding_month,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM funding_rounds fr
        GROUP BY
            fr.funding_year,
            fr.funding_month
        ORDER BY
            fr.funding_year,
            fr.funding_month;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


def industry_drilldown_to_startups():

    query = text("""
        SELECT
            i.industry_name,
            s.startup_name,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM startups s
        JOIN industries i ON s.industry_id = i.industry_id
        LEFT JOIN funding_rounds fr ON s.startup_id = fr.startup_id
        GROUP BY
            i.industry_name,
            s.startup_name
        ORDER BY
            i.industry_name,
            total_funding DESC NULLS LAST;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


def city_drilldown_to_industry():

    query = text("""
        SELECT
            l.city,
            i.industry_name,
            COUNT(DISTINCT s.startup_id) AS startup_count,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM startups s
        JOIN locations l ON s.location_id = l.location_id
        JOIN industries i ON s.industry_id = i.industry_id
        LEFT JOIN funding_rounds fr ON s.startup_id = fr.startup_id
        GROUP BY
            l.city,
            i.industry_name
        ORDER BY
            l.city,
            total_funding DESC NULLS LAST;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


# ============================================================
# 3. SLICE OPERATIONS
# ============================================================

def funding_slice_by_industry(industry_name):

    query = text("""
        SELECT
            s.startup_name,
            fr.funding_year,
            fr.funding_type,
            fr.funding_amount_usd
        FROM funding_rounds fr
        JOIN startups s ON fr.startup_id = s.startup_id
        JOIN industries i ON s.industry_id = i.industry_id
        WHERE i.industry_name = :industry_name
        ORDER BY
            fr.funding_year,
            fr.funding_amount_usd DESC;
    """)

    with engine.connect() as conn:
        result = conn.execute(
            query,
            {"industry_name": industry_name}
        )
        return [dict(row._mapping) for row in result]


def funding_slice_by_city(city):

    query = text("""
        SELECT
            s.startup_name,
            i.industry_name,
            fr.funding_year,
            fr.funding_type,
            fr.funding_amount_usd
        FROM funding_rounds fr
        JOIN startups s ON fr.startup_id = s.startup_id
        JOIN locations l ON s.location_id = l.location_id
        JOIN industries i ON s.industry_id = i.industry_id
        WHERE l.city = :city
        ORDER BY
            fr.funding_year,
            fr.funding_amount_usd DESC;
    """)

    with engine.connect() as conn:
        result = conn.execute(
            query,
            {"city": city}
        )
        return [dict(row._mapping) for row in result]


def funding_slice_by_year(year):

    query = text("""
        SELECT
            fr.funding_type,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM funding_rounds fr
        WHERE fr.funding_year = :year
        GROUP BY fr.funding_type
        ORDER BY total_funding DESC;
    """)

    with engine.connect() as conn:
        result = conn.execute(
            query,
            {"year": year}
        )
        return [dict(row._mapping) for row in result]


# ============================================================
# 4. DICE OPERATION
# ============================================================

def funding_dice(industries, cities, start_year, end_year):

    query = text("""
        SELECT
            i.industry_name,
            l.city,
            fr.funding_year,
            fr.funding_type,
            COUNT(fr.round_id) AS funding_rounds,
            SUM(fr.funding_amount_usd) AS total_funding
        FROM funding_rounds fr
        JOIN startups s ON fr.startup_id = s.startup_id
        JOIN industries i ON s.industry_id = i.industry_id
        JOIN locations l ON s.location_id = l.location_id
        WHERE
            i.industry_name = ANY(:industries)
            AND l.city = ANY(:cities)
            AND fr.funding_year BETWEEN :start_year AND :end_year
        GROUP BY
            i.industry_name,
            l.city,
            fr.funding_year,
            fr.funding_type
        ORDER BY
            fr.funding_year,
            total_funding DESC;
    """)

    with engine.connect() as conn:
        result = conn.execute(
            query,
            {
                "industries": industries,
                "cities": cities,
                "start_year": start_year,
                "end_year": end_year
            }
        )

        return [dict(row._mapping) for row in result]


# ============================================================
# 5. PIVOT OPERATIONS
# ============================================================

def funding_pivot_city_industry():

    query = text("""
        SELECT
            l.city,

            SUM(
                CASE WHEN i.industry_name = 'FinTech'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS fintech_funding,

            SUM(
                CASE WHEN i.industry_name = 'HealthTech'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS healthtech_funding,

            SUM(
                CASE WHEN i.industry_name = 'EdTech'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS edtech_funding,

            SUM(
                CASE WHEN i.industry_name = 'E-commerce'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS ecommerce_funding,

            SUM(
                CASE WHEN i.industry_name = 'SaaS'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS saas_funding

        FROM funding_rounds fr
        JOIN startups s ON fr.startup_id = s.startup_id
        JOIN locations l ON s.location_id = l.location_id
        JOIN industries i ON s.industry_id = i.industry_id

        GROUP BY l.city
        ORDER BY l.city;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]


def funding_pivot_year_stage():

    query = text("""
        SELECT
            fr.funding_year,

            SUM(
                CASE WHEN fr.funding_type = 'Seed'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS seed_funding,

            SUM(
                CASE WHEN fr.funding_type = 'Series A'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS series_a_funding,

            SUM(
                CASE WHEN fr.funding_type = 'Series B'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS series_b_funding,

            SUM(
                CASE WHEN fr.funding_type = 'Series C'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS series_c_funding,

            SUM(
                CASE WHEN fr.funding_type = 'Angel'
                THEN fr.funding_amount_usd ELSE 0 END
            ) AS angel_funding

        FROM funding_rounds fr

        GROUP BY fr.funding_year
        ORDER BY fr.funding_year;
    """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]