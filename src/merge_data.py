import pandas as pd
from pathlib import Path

CLEANED_DATA = Path("data/cleaned")

crime_file = CLEANED_DATA / "cleaned_crime_2015_2026_partial.csv"
housing_file = CLEANED_DATA / "housing_by_community_area.csv"
grocery_file = CLEANED_DATA / "grocery_by_community_area.csv"

output_file = CLEANED_DATA / "community_area_livability_base.csv"

crime = pd.read_csv(crime_file)
housing = pd.read_csv(housing_file)
grocery = pd.read_csv(grocery_file)

crime["community_area"] = pd.to_numeric(crime["community_area"], errors="coerce")
crime = crime.dropna(subset=["community_area"])
crime["community_area"] = crime["community_area"].astype(int)

violent_types = [
    "HOMICIDE",
    "ASSAULT",
    "BATTERY",
    "ROBBERY",
    "CRIMINAL SEXUAL ASSAULT",
    "CRIM SEXUAL ASSAULT",
]

property_types = [
    "THEFT",
    "BURGLARY",
    "MOTOR VEHICLE THEFT",
    "CRIMINAL DAMAGE",
    "ARSON",
]

crime["is_violent"] = crime["primary_type"].isin(violent_types)
crime["is_property"] = crime["primary_type"].isin(property_types)

crime_summary = (
    crime.groupby("community_area")
    .agg(
        total_crimes=("primary_type", "count"),
        violent_crimes=("is_violent", "sum"),
        property_crimes=("is_property", "sum"),
        first_year=("year", "min"),
        last_year=("year", "max"),
    )
    .reset_index()
)

base = crime_summary.merge(
    housing,
    on="community_area",
    how="left",
)

base = base.merge(
    grocery,
    on="community_area",
    how="left",
    suffixes=("_housing", "_grocery"),
)

base["affordable_property_count"] = base["affordable_property_count"].fillna(0)
base["affordable_unit_count"] = base["affordable_unit_count"].fillna(0)
base["grocery_store_count"] = base["grocery_store_count"].fillna(0)
base["total_grocery_square_feet"] = base["total_grocery_square_feet"].fillna(0)
base["avg_grocery_square_feet"] = base["avg_grocery_square_feet"].fillna(0)

base.to_csv(output_file, index=False)

print("Merged livability base saved to:", output_file)
print("Rows:", len(base))
print("Columns:", base.columns.tolist())
print(base.head())