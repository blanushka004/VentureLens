from analytics.startup_analysis import (
    get_startup_overview,
    get_top_funded_startups,
    get_most_active_startups,
    get_startup_funding_history,
    get_startup_distribution_by_industry,
    get_startup_distribution_by_city,
    get_recently_funded_startups,
    get_startup_funding_momentum
)


print("\n========== STARTUP OVERVIEW ==========\n")

print(get_startup_overview())


print("\n========== TOP FUNDED STARTUPS ==========\n")

for row in get_top_funded_startups():
    print(row)


print("\n========== MOST ACTIVE STARTUPS ==========\n")

for row in get_most_active_startups():
    print(row)


print("\n========== STARTUP FUNDING HISTORY ==========\n")

# Change this name based on your actual database startup
for row in get_startup_funding_history("Paytm"):
    print(row)


print("\n========== STARTUP DISTRIBUTION BY INDUSTRY ==========\n")

for row in get_startup_distribution_by_industry():
    print(row)


print("\n========== STARTUP DISTRIBUTION BY CITY ==========\n")

for row in get_startup_distribution_by_city():
    print(row)


print("\n========== RECENTLY FUNDED STARTUPS ==========\n")

for row in get_recently_funded_startups():
    print(row)


print("\n========== STARTUP FUNDING MOMENTUM ==========\n")

for row in get_startup_funding_momentum():
    print(row)