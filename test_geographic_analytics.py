from analytics.geographic_analysis import (
    get_geographic_overview,
    get_city_ecosystem,
    get_top_cities_by_startups,
    get_top_cities_by_funding,
    get_city_industry_distribution,
    get_city_leading_industries,
    get_city_funding_growth,
    get_city_funding_concentration,
    get_city_average_funding,
    get_city_investment_activity
)


print("\n========== GEOGRAPHIC OVERVIEW ==========\n")
print(get_geographic_overview())


print("\n========== CITY ECOSYSTEM ==========\n")
for row in get_city_ecosystem():
    print(row)


print("\n========== TOP CITIES BY STARTUPS ==========\n")
for row in get_top_cities_by_startups():
    print(row)


print("\n========== TOP CITIES BY FUNDING ==========\n")
for row in get_top_cities_by_funding():
    print(row)


print("\n========== CITY INDUSTRY DISTRIBUTION ==========\n")
for row in get_city_industry_distribution():
    print(row)


print("\n========== LEADING INDUSTRIES BY CITY ==========\n")
for row in get_city_leading_industries():
    print(row)


print("\n========== CITY FUNDING GROWTH ==========\n")
for row in get_city_funding_growth():
    print(row)


print("\n========== CITY FUNDING CONCENTRATION ==========\n")
for row in get_city_funding_concentration():
    print(row)


print("\n========== AVERAGE FUNDING PER STARTUP ==========\n")
for row in get_city_average_funding():
    print(row)


print("\n========== CITY INVESTMENT ACTIVITY ==========\n")
for row in get_city_investment_activity():
    print(row)