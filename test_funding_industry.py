from analytics.funding_analysis import (
    get_funding_summary,
    get_yearly_funding_trend,
    get_quarterly_funding_trend,
    get_funding_distribution_by_type,
    get_largest_funding_rounds,
    get_year_over_year_growth,
    get_monthly_funding_trend
)

from analytics.industry_analysis import (
    get_industry_overview,
    get_top_industries_by_funding,
    get_industry_growth,
    get_industry_market_share
)


print("\n========== FUNDING SUMMARY ==========\n")
print(get_funding_summary())


print("\n========== YEARLY FUNDING ==========\n")
for row in get_yearly_funding_trend():
    print(row)


print("\n========== QUARTERLY FUNDING ==========\n")
for row in get_quarterly_funding_trend():
    print(row)


print("\n========== FUNDING DISTRIBUTION ==========\n")
for row in get_funding_distribution_by_type():
    print(row)


print("\n========== LARGEST FUNDING ROUNDS ==========\n")
for row in get_largest_funding_rounds(10):
    print(row)


print("\n========== YEAR OVER YEAR GROWTH ==========\n")
for row in get_year_over_year_growth():
    print(row)


print("\n========== INDUSTRY OVERVIEW ==========\n")
for row in get_industry_overview():
    print(row)


print("\n========== INDUSTRY MARKET SHARE ==========\n")
for row in get_industry_market_share():
    print(row)