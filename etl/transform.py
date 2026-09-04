import pandas as pd


REQUIRED_COLUMNS = [
    "Startup",
    "Industry",
    "SubVertical",
    "City",
    "Investors",
    "InvestmentType",
    "InvestmentAmount_USD",
    "Date"
]


def clean_text(value):
    """
    Clean text fields safely.
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "" or value.lower() in ["nan", "none", "null"]:
        return None

    return value


def transform_data(df):
    """
    Clean and transform raw startup funding data.
    """

    print("\nStarting data transformation...")

    # --------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # --------------------------------------------------

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Keep only required columns
    df = df[REQUIRED_COLUMNS].copy()

    print(f"Initial records: {len(df)}")

    # --------------------------------------------------
    # CLEAN TEXT COLUMNS
    # --------------------------------------------------

    text_columns = [
        "Startup",
        "Industry",
        "SubVertical",
        "City",
        "Investors",
        "InvestmentType"
    ]

    for column in text_columns:
        df[column] = df[column].apply(clean_text)

    # --------------------------------------------------
    # CLEAN FUNDING AMOUNT
    # --------------------------------------------------

    df["InvestmentAmount_USD"] = (
        pd.to_numeric(
            df["InvestmentAmount_USD"],
            errors="coerce"
        )
    )

    # --------------------------------------------------
    # PARSE DATE
    # --------------------------------------------------

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
        errors="coerce"
    )

    # --------------------------------------------------
    # REMOVE INVALID CORE RECORDS
    # --------------------------------------------------

    df = df.dropna(
        subset=[
            "Startup",
            "Industry",
            "City",
            "Date"
        ]
    )

    # --------------------------------------------------
    # REMOVE DUPLICATE FUNDING RECORDS
    # --------------------------------------------------

    df = df.drop_duplicates(
        subset=[
            "Startup",
            "Date",
            "InvestmentType",
            "InvestmentAmount_USD"
        ]
    )

    # --------------------------------------------------
    # EXTRACT TIME FEATURES
    # --------------------------------------------------

    df["FundingYear"] = df["Date"].dt.year
    df["FundingMonth"] = df["Date"].dt.month
    df["FundingQuarter"] = df["Date"].dt.quarter

    # --------------------------------------------------
    # RESET INDEX
    # --------------------------------------------------

    df = df.reset_index(drop=True)

    print(f"Records after cleaning: {len(df)}")

    print("\nTransformation completed successfully.")

    return df


if __name__ == "__main__":

    from etl.extract import extract_data

    raw_data = extract_data()

    processed_data = transform_data(raw_data)

    print("\nProcessed Data Preview:")
    print(processed_data.head())

    print("\nData Info:")
    print(processed_data.info())