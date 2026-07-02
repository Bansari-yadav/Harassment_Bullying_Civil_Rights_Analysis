import pandas as pd
from pathlib import Path

CLEANED_DATA = Path("data/cleaned")

input_file = CLEANED_DATA / "cleaned_crime_recent.csv"
output_file = CLEANED_DATA / "crime_summary_by_ward.csv"

crime = pd.read_csv(input_file)

summary = (
    crime.groupby("ward")
    .agg(
        total_crimes=("ward", "count"),
        violent_crimes=("violent_crime", "sum"),
        property_crimes=("property_crime", "sum"),
        arrest_count=("arrest_count", "sum"),
        domestic_crimes=("domestic_crime", "sum"),
        first_year=("year", "min"),
        last_year=("year", "max"),
    )
    .reset_index()
)

summary["arrest_rate"] = summary["arrest_count"] / summary["total_crimes"]

summary.to_csv(output_file, index=False)

print("Saved:", output_file)
print(summary.head())