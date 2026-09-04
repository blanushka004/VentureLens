from analytics.overview import (
    get_total_startups,
    get_total_funding,
    get_total_investors,
    get_total_funding_rounds,
    get_funding_by_year,
    get_top_industries,
    get_top_startups,
    get_top_investors,
    get_top_cities,
    get_funding_by_type
)


print("\n========== VENTURELENS ANALYTICS ==========\n")

print("TOTAL STARTUPS:")
print(get_total_startups())

print("\nTOTAL FUNDING:")
print(get_total_funding())

print("\nTOTAL INVESTORS:")
print(get_total_investors())

print("\nTOTAL FUNDING ROUNDS:")
print(get_total_funding_rounds())


print("\n========== FUNDING BY YEAR ==========\n")

for row in get_funding_by_year():
    print(row)


print("\n========== TOP INDUSTRIES ==========\n")

for row in get_top_industries():
    print(row)


print("\n========== TOP STARTUPS ==========\n")

for row in get_top_startups():
    print(row)


print("\n========== TOP INVESTORS ==========\n")

for row in get_top_investors():
    print(row)


print("\n========== TOP CITIES ==========\n")

for row in get_top_cities():
    print(row)


print("\n========== FUNDING BY TYPE ==========\n")

for row in get_funding_by_type():
    print(row)