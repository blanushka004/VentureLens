from analytics.investor_analysis import (
    get_top_investors,
    get_investor_portfolio,
    get_investor_industry_preferences,
    get_investor_geographic_reach,
    get_investor_activity_by_year,
    get_most_diversified_investors,
    get_co_investment_pairs
)


print("\n========== INVESTOR INTELLIGENCE ==========\n")


print("TOP INVESTORS:\n")

for row in get_top_investors():
    print(row)


print("\n========== INVESTOR PORTFOLIO ==========\n")

for row in get_investor_portfolio():
    print(row)


print("\n========== INVESTOR INDUSTRY PREFERENCES ==========\n")

for row in get_investor_industry_preferences():
    print(row)


print("\n========== INVESTOR GEOGRAPHIC REACH ==========\n")

for row in get_investor_geographic_reach():
    print(row)


print("\n========== INVESTOR ACTIVITY BY YEAR ==========\n")

for row in get_investor_activity_by_year():
    print(row)


print("\n========== MOST DIVERSIFIED INVESTORS ==========\n")

for row in get_most_diversified_investors():
    print(row)


print("\n========== CO-INVESTMENT NETWORK ==========\n")

for row in get_co_investment_pairs():
    print(row)