"""Inspect the PhiUSIIL dataset without opening any listed websites."""

import os

import pandas as pd


file_path = os.path.join("data", "PhiUSIIL_Phishing_URL_Dataset.csv")

if not os.path.exists(file_path):
    print("ERROR: The dataset could not be found.")
    print("Expected location:", file_path)
else:
    print("Loading the dataset. Please wait...")
    data = pd.read_csv(file_path)

    print("\n1. DATASET SIZE")
    print("Rows:", data.shape[0])
    print("Columns:", data.shape[1])

    print("\n2. COLUMN NAMES")
    print(data.columns.tolist())

    print("\n3. FIRST FIVE URLS")
    print(data[["URL", "label"]].head())

    print("\n4. MISSING VALUES")
    print("Total missing values:", data.isnull().sum().sum())

    print("\n5. DUPLICATE URLS")
    print("Duplicate URLs:", data["URL"].duplicated().sum())

    print("\n6. CLASS DISTRIBUTION")
    print(data["label"].value_counts().sort_index())
    print("0 = phishing")
    print("1 = legitimate")

    print("\nInspection complete. The dataset was not changed.")
