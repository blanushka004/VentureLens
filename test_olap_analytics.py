from analytics import olap_queries


def print_results(title, results):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60 + "\n")

    for row in results:
        print(row)

def test_olap_analytics():

    # ============================================================
    # 1. ROLL-UP OPERATIONS
    # ============================================================

    print_results(
        "FUNDING ROLL-UP BY YEAR",
        olap_queries.funding_rollup_by_year()
    )

    print_results(
        "FUNDING ROLL-UP BY CITY",
        olap_queries.funding_rollup_by_city()
    )

    print_results(
        "FUNDING ROLL-UP BY INDUSTRY",
        olap_queries.funding_rollup_by_industry()
    )


    # ============================================================
    # 2. DRILL-DOWN OPERATIONS
    # ============================================================

    print_results(
        "FUNDING DRILL-DOWN YEAR TO MONTH",
        olap_queries.funding_drilldown_year_to_month()
    )

    print_results(
        "INDUSTRY DRILL-DOWN TO STARTUPS",
        olap_queries.industry_drilldown_to_startups()
    )

    print_results(
        "CITY DRILL-DOWN TO INDUSTRY",
        olap_queries.city_drilldown_to_industry()
    )


    # ============================================================
    # 3. SLICE OPERATIONS
    # ============================================================

    print_results(
        "SLICE: FUNDING BY INDUSTRY - FinTech",
        olap_queries.funding_slice_by_industry("FinTech")
    )

    print_results(
        "SLICE: FUNDING BY CITY - Bengaluru",
        olap_queries.funding_slice_by_city("Bengaluru")
    )

    print_results(
        "SLICE: FUNDING BY YEAR - 2024",
        olap_queries.funding_slice_by_year(2024)
    )


    # ============================================================
    # 4. DICE OPERATION
    # ============================================================

    print_results(
        "DICE: SELECTED INDUSTRIES + CITIES + YEARS",
        olap_queries.funding_dice(
            industries=["FinTech", "HealthTech"],
            cities=["Bengaluru", "Mumbai"],
            start_year=2022,
            end_year=2024
        )
    )


    # ============================================================
    # 5. PIVOT OPERATIONS
    # ============================================================

    print_results(
        "PIVOT: CITY VS INDUSTRY FUNDING",
        olap_queries.funding_pivot_city_industry()
    )

    print_results(
        "PIVOT: YEAR VS FUNDING STAGE",
        olap_queries.funding_pivot_year_stage()
    )


if __name__ == "__main__":
    test_olap_analytics()