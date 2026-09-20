# PhishScope

**A machine learning toolkit for detecting phishing URLs using explainable
URL-text features.**

PhishScope extracts lexical and structural features from URLs, trains and
compares several classifiers, and produces a transparent risk score with
human-readable explanations.

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Made by](https://img.shields.io/badge/Made%20by-@annisadanish-cyan?style=for-the-badge)](https://github.com/annisadanish)

---

## Overview

Phishing attacks remain one of the most common vectors for credential theft
and malware delivery. PhishScope explores whether **URL text alone** — without
visiting the page — is enough to distinguish phishing URLs from legitimate ones.

The project covers a full pipeline:

1. Clean a labeled URL dataset (remove conflicts and duplicates)
2. Extract lexical, structural, and keyword-based features
3. Train and compare classifiers with a phishing-positive class
4. Save the best model and expose predictions through a web app
5. Produce a transparent risk score with explanations

> **Safety note:** The feature extractor only analyzes the URL string. It never
> connects to the target website.

---

## Project Structure

    phishscope-detector/
    ├── app.py                       # Web interface for URL risk checking
    ├── url_features.py              # Feature extraction + risk scoring
    ├── prepare_data.py              # Dataset cleaning and feature generation
    ├── inspect_data.py              # Quick EDA on the raw dataset
    ├── train_model.py               # Train and compare classifiers
    ├── create_evaluation_report.py  # Generate evaluation report
    ├── PROJECT_REPORT.md            # Full project write-up
    ├── README.md
    ├── requirements.txt
    └── .gitignore

---

## Dataset

**Source:** PhiUSIIL Phishing URL Dataset

- Input file expected at `data/PhiUSIIL_Phishing_URL_Dataset.csv`
- Contains `URL` and `label` columns

**Preprocessing (`prepare_data.py`):**

- Removes URLs that appear with **conflicting labels**
- Removes duplicates by URL
- Extracts numeric features from the URL text
- Writes cleaned output to `data/processed_urls.csv`

> Raw data files are not committed. Place the dataset in `data/` before running.

---

## Feature Engineering

Features are extracted by `url_features.py` — all from the URL text only.

| Feature | Description |
|---|---|
| `url_length` | Length of the full URL |
| `uses_https` | 1 if scheme is HTTPS, else 0 |
| `hostname_is_ip` | 1 if hostname is an IPv4/IPv6 address |
| `dot_count` | Number of dots in the hostname |
| `hyphen_count` | Number of hyphens in the hostname |
| `at_symbol_count` | Count of `@` in the URL (can hide the true host) |
| `digit_count` | Number of digits in the URL |
| `suspicious_word_count` | Matches from a keyword list |

**Suspicious keywords:**
`account`, `banking`, `confirm`, `login`, `password`, `secure`, `signin`,
`update`, `verify`

---

## Risk Score

In addition to the ML model, `calculate_risk()` in `url_features.py` returns a
transparent 0–100 score with explanations:

| Indicator | Points |
|---|---|
| Hostname is an IP address | +30 |
| URL length > 75 | +20 |
| `@` symbol present | +20 |
| 4+ dots in hostname | +15 |
| 2+ hyphens in hostname | +10 |
| 6+ digits in URL | +10 |
| Suspicious keywords | up to +20 |
| No HTTPS | +5 |

**Levels:** `High` ≥ 60 · `Medium` ≥ 30 · `Low` < 30

---

## Model Training

`train_model.py` compares three classifiers using an 80/20 stratified split:

1. **Dummy baseline** (most frequent class) — sanity check
2. **Logistic Regression** with `StandardScaler`
3. **Decision Tree** (`max_depth=8`, `min_samples_leaf=20`)

**Target encoding:**

- Original dataset: `0 = phishing`, `1 = legitimate`
- Model target: `1 = phishing`, `0 = legitimate`

This makes **phishing the positive class**, so precision/recall/F1 directly
reflect detection performance.

**Metrics:** accuracy, precision, recall, F1-score, confusion matrix.

The best non-dummy model is saved to:

    models/phishscope_model.joblib

along with the feature names and model metadata.

---

## Installation

    git clone git@github.com:annisadanish/phishscope-detector.git
    cd phishscope-detector
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

---

## Usage

### 1. Prepare the dataset

Place `PhiUSIIL_Phishing_URL_Dataset.csv` in `data/`, then:

    python prepare_data.py

### 2. Inspect the data (optional)

    python inspect_data.py

### 3. Train the model

    python train_model.py

### 4. Generate the evaluation report

    python create_evaluation_report.py

### 5. Run the web app

    python app.py

Then open the local URL shown in the terminal.

---

## Ethical Use

This project is intended for:

- Educational purposes
- Defensive security research
- Personal or organizational phishing detection

Do **not** use this tool to generate, distribute, or promote phishing URLs.
Do **not** scan URLs you do not have permission to analyze.

---

## Roadmap

- [ ] Add WHOIS-based and TLS-certificate features
- [ ] Compare gradient boosting models (XGBoost / LightGBM)
- [ ] SHAP-based feature importance
- [ ] Package as a CLI tool
- [ ] Deploy as a public API
- [ ] Add unit tests for feature extraction

---

## License

MIT — see [LICENSE](LICENSE).

## Author

**Annisa Danish** — [github.com/annisadanish](https://github.com/annisadanish)
