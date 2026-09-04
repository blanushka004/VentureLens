from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "indian_startup_funding.csv"


def extract_data():
    """
    Extract raw startup funding data from CSV.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    print(f"Reading dataset from: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print(f"Records extracted: {len(df)}")
    print(f"Columns found: {list(df.columns)}")

    return df


if __name__ == "__main__":
    dataframe = extract_data()

    print("\nFirst 5 records:")
    print(dataframe.head())