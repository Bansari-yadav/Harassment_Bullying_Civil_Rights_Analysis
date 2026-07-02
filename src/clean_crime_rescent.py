import pandas as pd
from pathlib import Path
import re

RAW_DATA = Path("data/raw")
CLEANED_DATA = Path("data/cleaned")
CLEANED_DATA.mkdir(parents=True, exist_ok=True)

input_file = RAW_DATA / "Crimes_-_One_year_prior_to_present_20260624.csv"
cleaned_file = CLEANED_DATA / "cleaned_crime_recent.csv"
summary_file = CLEANED_DATA / "recent_crime_by_ward.csv"

def normalize_column(col):
    col = col.strip().lower()
    col = re.sub(r"[^a-z0-9]+", "_", col)
    return col.strip("_")

column_map = {
    "case_number": "case_id",
    "case": "case_id",
    "case_": "case_id",

    "date": "date",
    "date_of_occurrence": "date",

    "primary_type": "primary_type",
    "primary_description": "primary_type",

    "description": "description",
    "secondary_description": "description",

    "location_description": "location_description",
    "arrest": "arrest",
    "domestic": "domestic",
    "beat": "beat",
    "ward": "ward",
    "latitude": "latitude",
    "longitude": "longitude",
}

needed_normalized_columns = set(column_map.keys())

violent_types = {
    "HOMICIDE",
    "ASSAULT",
    "BATTERY",
    "ROBBERY",
    "CRIMINAL SEXUAL ASSAULT",
}

property_types = {
    "THEFT",
    "BURGLARY",
    "MOTOR VEHICLE THEFT",
    "CRIMINAL DAMAGE",
    "ARSON",
}

chunks = []

for chunk in pd.read_csv(
    input_file,
    chunksize=100000,
    low_memory=False,
    usecols=lambda col: normalize_column(col) in needed_normalized_columns,
):
    chunk = chunk.rename(columns={
        col: column_map[normalize_column(col)]
        for col in chunk.columns
        if normalize_column(col) in column_map
    })

    chunk["date"] = pd.to_datetime(chunk["date"], errors="coerce")
    chunk["ward"] = pd.to_numeric(chunk["ward"], errors="coerce")

    chunk = chunk.dropna(subset=["date", "ward"])
    chunk["ward"] = chunk["ward"].astype(int)

    chunk["year"] = chunk["date"].dt.year
    chunk["month"] = chunk["date"].dt.month

    chunk["primary_type"] = chunk["primary_type"].astype(str).str.upper()

    chunk["violent_crime"] = chunk["primary_type"].isin(violent_types).astype(int)
    chunk["property_crime"] = chunk["primary_type"].isin(property_types).astype(int)
    chunk["arrest_count"] = chunk["arrest"].astype(str).str.lower().eq("true").astype(int)
    chunk["domestic_crime"] = chunk["domestic"].astype(str).str.lower().eq("true").astype(int)

    chunks.append(chunk)

crime = pd.concat(chunks, ignore_index=True)

if "case_id" in crime.columns:
    crime = crime.drop_duplicates(subset=["case_id"])
else:
    crime = crime.drop_duplicates()

crime.to_csv(cleaned_file, index=False)

summary = (
    crime.groupby("ward")
    .agg(
        total_recent_crimes=("ward", "count"),
        recent_violent_crimes=("violent_crime", "sum"),
        recent_property_crimes=("property_crime", "sum"),
        recent_arrest_count=("arrest_count", "sum"),
        recent_domestic_crimes=("domestic_crime", "sum"),
        first_year=("year", "min"),
        last_year=("year", "max"),
    )
    .reset_index()
)

summary.to_csv(summary_file, index=False)

print("Saved:", cleaned_file)
print("Saved:", summary_file)
print("Rows cleaned:", len(crime))
print(summary.head())