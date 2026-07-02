import pandas as pd
from pathlib import Path

CLEANED_DATA = Path("data/cleaned")

crime_file = CLEANED_DATA / "crime_summary_by_ward.csv"
housing_file = CLEANED_DATA / "housing_by_community_area.csv"
grocery_file = CLEANED_DATA / "grocery_by_community_area.csv"

output_file = CLEANED_DATA / "final_livability_scores.csv"

crime = pd.read_csv(crime_file)
housing = pd.read_csv(housing_file)
grocery = pd.read_csv(grocery_file)

print("Crime columns:", crime.columns.tolist())
print("Housing columns:", housing.columns.tolist())
print("Grocery columns:", grocery.columns.tolist())

# TEMPORARY:
# Crime is currently by ward, while housing/grocery are likely by community area.
# So for now, we create a crime-only score file and later adjust the merge key.
final = crime.copy()

# Safety score: lower crime count = higher score
final["safety_score"] = 100 - (
    (final["total_crimes"] - final["total_crimes"].min())
    / (final["total_crimes"].max() - final["total_crimes"].min())
    * 100
)

# Violent crime score: lower violent crime count = higher score
final["violent_safety_score"] = 100 - (
    (final["violent_crimes"] - final["violent_crimes"].min())
    / (final["violent_crimes"].max() - final["violent_crimes"].min())
    * 100
)

# Final temporary score
final["final_livability_score"] = (
    final["safety_score"] * 0.7
    + final["violent_safety_score"] * 0.3
)

final = final.sort_values("final_livability_score", ascending=False)

final.to_csv(output_file, index=False)

print("Saved:", output_file)
print(final.head(10))