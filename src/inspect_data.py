import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")

crime_file = RAW_DATA / "Crimes_-_One_year_prior_to_present_20260624.csv"
housing_file = RAW_DATA / "Affordable_Rental_Housing_Developments.csv"
population_file = RAW_DATA / "Chicago_Population_Counts (1).csv"

print("Checking files...\n")

for file in [crime_file, housing_file, population_file]:
    print(file)
    print("Exists:", file.exists())
    print()

print("Crime columns:")
crime_sample = pd.read_csv(crime_file, nrows=5)
print(crime_sample.columns.tolist())
print(crime_sample.head())

print("\nHousing columns:")
housing = pd.read_csv(housing_file)
print(housing.columns.tolist())
print(housing.head())

print("\nPopulation columns:")
population = pd.read_csv(population_file)
print(population.columns.tolist())
print(population.head())