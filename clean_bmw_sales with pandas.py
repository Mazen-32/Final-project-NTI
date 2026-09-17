"""
BMW Sales Data Cleaning Script
Cleans raw BMW sales data for Power BI dashboarding.
"""
import pandas as pd

INPUT_PATH = "/mnt/user-data/uploads/BMW_Sales_Data.csv"
OUTPUT_PATH = "/mnt/user-data/outputs/BMW_Sales_Data_Clean.csv"

def clean_bmw_sales(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    rows_before = len(df)

    # 1. Drop fully empty rows
    df = df.dropna(how="all")

    # 2. Drop rows missing any critical field (date, revenue, qty, model)
    critical_cols = ["Date", "Model", "Revenue", "Quantity Sold", "Region", "Country", "Channel"]
    df = df.dropna(subset=critical_cols)

    # 3. Parse Date properly (source format is DD/MM/YYYY)
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")
    df = df.dropna(subset=["Date"])  # drop any dates that failed to parse

    # 4. Fix dtypes
    df["Year"] = df["Date"].dt.year.astype(int)          # derive Year from Date (safer than trusting the column)
    df["Quantity Sold"] = df["Quantity Sold"].astype(int)
    df["Revenue"] = df["Revenue"].astype(float).round(2)

    # 5. Add a helpful derived column for Power BI (avg price per unit)
    df["Revenue Per Unit"] = (df["Revenue"] / df["Quantity Sold"]).round(2)

    # 6. Clean text columns: strip whitespace, standardize casing
    text_cols = ["Model", "Region", "Country", "Channel"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # 7. Drop exact duplicate rows
    df = df.drop_duplicates()

    # 8. Sort chronologically and reset index
    df = df.sort_values("Date").reset_index(drop=True)

    # 9. Reorder columns nicely
    df = df[["Date", "Year", "Model", "Region", "Country", "Channel",
             "Quantity Sold", "Revenue", "Revenue Per Unit"]]

    print(f"Rows before cleaning: {rows_before}")
    print(f"Rows after cleaning:  {len(df)}")
    print(f"Rows removed:         {rows_before - len(df)}")
    return df

if __name__ == "__main__":
    clean_df = clean_bmw_sales(INPUT_PATH)
    clean_df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved cleaned file to: {OUTPUT_PATH}")
    print("\nPreview:")
    print(clean_df.head())
    print("\nDtypes:")
    print(clean_df.dtypes)
