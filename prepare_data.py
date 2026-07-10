"""Create a clean, URL-text-only dataset for PhishScope."""

import os

import pandas as pd

from url_features import extract_features


input_path = os.path.join("data", "PhiUSIIL_Phishing_URL_Dataset.csv")
output_path = os.path.join("data", "processed_urls.csv")


def convert_url_to_row(url, label):
    """Convert one URL into numeric features that a model can use."""
    features = extract_features(url)

    return {
        "url_length": features["url_length"],
        "uses_https": int(features["uses_https"]),
        "hostname_is_ip": int(features["hostname_is_ip"]),
        "dot_count": features["dot_count"],
        "hyphen_count": features["hyphen_count"],
        "at_symbol_count": features["at_symbol_count"],
        "digit_count": features["digit_count"],
        "suspicious_word_count": len(features["suspicious_words"]),
        "label": label,
    }


if not os.path.exists(input_path):
    print("ERROR: The original dataset could not be found.")
    print("Expected location:", input_path)
else:
    print("Reading the URL and label columns...")
    original_data = pd.read_csv(input_path, usecols=["URL", "label"])

    original_rows = len(original_data)

    # Find URLs that have been assigned both labels.
    label_counts = original_data.groupby("URL")["label"].nunique()
    conflicting_urls = label_counts[label_counts > 1].index

    # Ambiguous examples are removed instead of guessing which label is right.
    clean_data = original_data[~original_data["URL"].isin(conflicting_urls)]
    clean_data = clean_data.drop_duplicates(subset=["URL"]).reset_index(drop=True)

    print("Creating safe URL-text features. Please wait...")
    processed_rows = []

    for row_number, row in clean_data.iterrows():
        processed_rows.append(convert_url_to_row(row["URL"], row["label"]))

        if (row_number + 1) % 50000 == 0:
            print("Processed", row_number + 1, "URLs")

    processed_data = pd.DataFrame(processed_rows)
    processed_data.to_csv(output_path, index=False)

    print("\nPREPROCESSING SUMMARY")
    print("Original rows:", original_rows)
    print("Conflicting URLs removed:", len(conflicting_urls))
    print("Final unique rows:", len(processed_data))
    print("Output file:", output_path)

    print("\nFINAL CLASS DISTRIBUTION")
    print(processed_data["label"].value_counts().sort_index())

    print("\nProcessed dataset created successfully.")
