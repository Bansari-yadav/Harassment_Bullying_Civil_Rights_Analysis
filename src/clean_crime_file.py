import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")
CLEANED_DATA = Path("data/cleaned")
CLEANED_DATA.mkdir(parents=True, exist_ok=True)

crime_file = RAW_DATA / "Crimes_-_2015_20260626.csv"
output_file = CLEANED_DATA / "cleaned_crime_2015_2026_partial.csv"

columns_to_use = [
    "Date",
    "Primary Type",
    "Description",
    "Location Description",
    "Arrest",
    "Domestic",
    "Ward",
    "Community Area",
    "Latitude",
    "Longitude",
    "Year",
]

chunks = []

for chunk in pd.read_csv(crime_file, usecols=columns_to_use, chunksize=100000):
    chunk = chunk.rename(
        columns={
            "Date": "date",
            "Primary Type": "primary_type",
            "Description": "description",
            "Location Description": "location_description",
            "Arrest": "arrest",
            "Domestic": "domestic",
            "Ward": "ward",
            "Community Area": "community_area",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Year": "year",
        }
    )

    chunk["date"] = pd.to_datetime(chunk["date"], errors="coerce")
    chunk["community_area"] = pd.to_numeric(chunk["community_area"], errors="coerce")
    chunk["ward"] = pd.to_numeric(chunk["ward"], errors="coerce")
    chunk["latitude"] = pd.to_numeric(chunk["latitude"], errors="coerce")
    chunk["longitude"] = pd.to_numeric(chunk["longitude"], errors="coerce")
    chunk["year"] = pd.to_numeric(chunk["year"], errors="coerce")

    chunk = chunk.dropna(subset=["date", "community_area", "year"])

    chunk["community_area"] = chunk["community_area"].astype(int)
    chunk["year"] = chunk["year"].astype(int)

    chunk = chunk[chunk["community_area"] != 0]

    chunk["month"] = chunk["date"].dt.month

    chunks.append(chunk)

cleaned_crime = pd.concat(chunks, ignore_index=True)

cleaned_crime.to_csv(output_file, index=False)

print("Cleaned crime file saved to:", output_file)
print("Rows:", len(cleaned_crime))
print("Columns:", cleaned_crime.columns.tolist())
print(cleaned_crime.head())