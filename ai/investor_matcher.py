from sqlalchemy import text
from database.connection import engine

def match_investors(industry: str, city: str|None=None, limit:int=5):
    query=text("""
        SELECT i.investor_name, COUNT(inv.investment_id) AS investments_count,
               COUNT(DISTINCT fr.startup_id) AS startups_invested,
               SUM(CASE WHEN LOWER(ind.industry_name)=LOWER(:industry) THEN 1 ELSE 0 END) AS industry_matches,
               SUM(CASE WHEN LOWER(l.city)=LOWER(:city) THEN 1 ELSE 0 END) AS city_matches
        FROM investors i
        JOIN investments inv ON i.investor_id=inv.investor_id
        JOIN funding_rounds fr ON inv.round_id=fr.round_id
        JOIN startups s ON fr.startup_id=s.startup_id
        JOIN industries ind ON s.industry_id=ind.industry_id
        JOIN locations l ON s.location_id=l.location_id
        GROUP BY i.investor_name
        ORDER BY industry_matches DESC, city_matches DESC, investments_count DESC
        LIMIT :limit
    """)
    with engine.connect() as conn:
        rows=conn.execute(query, {'industry':industry,'city':city or '', 'limit':limit})
        return [dict(r._mapping) for r in rows]
