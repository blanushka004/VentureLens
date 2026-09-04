from sqlalchemy import text

from database.connection import engine
# ============================================================
# TOP INVESTORS
# ============================================================

def get_top_investors(limit=10):

    query = text("""
        SELECT
            i.investor_name,
            COUNT(inv.investment_id) AS investments_count,
            COUNT(DISTINCT fr.startup_id) AS startups_invested
        FROM investors i
        JOIN investments inv
            ON i.investor_id = inv.investor_id
        JOIN funding_rounds fr
            ON inv.round_id = fr.round_id
        GROUP BY i.investor_name
        ORDER BY investments_count DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})

        return [
            {
                "investor_name": row[0],
                "investments_count": row[1],
                "startups_invested": row[2]
            }
            for row in result
        ]


# ============================================================
# INVESTOR PORTFOLIO SIZE
# ============================================================

def get_investor_portfolio():

    query = text("""
        SELECT
            i.investor_name,
            COUNT(DISTINCT fr.startup_id) AS portfolio_size,
            COUNT(inv.investment_id) AS total_investments
        FROM investors i
        JOIN investments inv
            ON i.investor_id = inv.investor_id
        JOIN funding_rounds fr
            ON inv.round_id = fr.round_id
        GROUP BY i.investor_name
        ORDER BY portfolio_size DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        return [
            {
                "investor_name": row[0],
                "portfolio_size": row[1],
                "total_investments": row[2]
            }
            for row in result
        ]


# ============================================================
# INVESTOR INDUSTRY PREFERENCES
# ============================================================
def get_investor_industry_preferences(limit=10):

    query = text("""
        SELECT
            i.investor_name,
            ind.industry_name,
            COUNT(DISTINCT fr.startup_id) AS startups_count,
            COUNT(inv.investment_id) AS investments_count
        FROM investors i
        JOIN investments inv
            ON i.investor_id = inv.investor_id
        JOIN funding_rounds fr
            ON inv.round_id = fr.round_id
        JOIN startups s
            ON fr.startup_id = s.startup_id
        JOIN industries ind
            ON s.industry_id = ind.industry_id
        GROUP BY
            i.investor_name,
            ind.industry_name
        ORDER BY investments_count DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})
        return [dict(row._mapping) for row in result]
    
# ============================================================
# INVESTOR GEOGRAPHIC REACH
# ============================================================
def get_investor_geographic_reach(limit=20):

    query = text("""
        SELECT
            i.investor_name,
            l.city,
            COUNT(DISTINCT fr.startup_id) AS startups_count,
            COUNT(inv.investment_id) AS investments_count
        FROM investors i
        JOIN investments inv
            ON i.investor_id = inv.investor_id
        JOIN funding_rounds fr
            ON inv.round_id = fr.round_id
        JOIN startups s
            ON fr.startup_id = s.startup_id
        JOIN locations l
            ON s.location_id = l.location_id
        GROUP BY
            i.investor_name,
            l.city
        ORDER BY investments_count DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})

        return [
            {
                "investor_name": row[0],
                "city": row[1],
                "startups_count": row[2],
                "investments_count": row[3]
            }
            for row in result
        ]

# ============================================================
# INVESTOR ACTIVITY BY YEAR
# ============================================================

def get_investor_activity_by_year():

    query = text("""
        SELECT
            i.investor_name,
            EXTRACT(YEAR FROM fr.funding_date)::INTEGER AS funding_year,
            COUNT(inv.investment_id) AS investments_count
        FROM investors i
        JOIN investments inv
            ON i.investor_id = inv.investor_id
        JOIN funding_rounds fr
            ON inv.round_id = fr.round_id
        GROUP BY
            i.investor_name,
            EXTRACT(YEAR FROM fr.funding_date)
        ORDER BY
            funding_year,
            investments_count DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(query)

        return [
            {
                "investor_name": row[0],
                "funding_year": row[1],
                "investments_count": row[2]
            }
            for row in result
        ]


# ============================================================
# MOST DIVERSIFIED INVESTORS
# ============================================================

def get_most_diversified_investors(limit=10):

    query = text("""
        SELECT
            i.investor_name,
            COUNT(DISTINCT ind.industry_id) AS industries_invested,
            COUNT(DISTINCT fr.startup_id) AS startups_invested,
            COUNT(DISTINCT l.city) AS cities_reached
        FROM investors i
        JOIN investments inv
            ON i.investor_id = inv.investor_id
        JOIN funding_rounds fr
            ON inv.round_id = fr.round_id
        JOIN startups s
            ON fr.startup_id = s.startup_id
        JOIN industries ind
            ON s.industry_id = ind.industry_id
        JOIN locations l
            ON s.location_id = l.location_id
        GROUP BY i.investor_name
        ORDER BY industries_invested DESC,
                 startups_invested DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})

        return [
            {
                "investor_name": row[0],
                "industries_invested": row[1],
                "startups_invested": row[2],
                "cities_reached": row[3]
            }
            for row in result
        ]


# ============================================================
# CO-INVESTMENT NETWORK
# ============================================================

def get_co_investment_pairs(limit=20):

    query = text("""
        SELECT
            i1.investor_name AS investor_1,
            i2.investor_name AS investor_2,
            COUNT(DISTINCT inv1.round_id) AS shared_rounds
        FROM investments inv1
        JOIN investments inv2
            ON inv1.round_id = inv2.round_id
            AND inv1.investor_id < inv2.investor_id
        JOIN investors i1
            ON inv1.investor_id = i1.investor_id
        JOIN investors i2
            ON inv2.investor_id = i2.investor_id
        GROUP BY
            i1.investor_name,
            i2.investor_name
        ORDER BY shared_rounds DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit})

        return [
            {
                "investor_1": row[0],
                "investor_2": row[1],
                "shared_rounds": row[2]
            }
            for row in result
        ]
        