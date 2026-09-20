# PhishScope

**A machine learning toolkit for detecting phishing URLs.**

PhishScope extracts lexical and structural features from URLs, trains a
classifier, and exposes a simple web interface for real-time phishing
detection.

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Made by](https://img.shields.io/badge/Made%20by-@annisadanish-cyan?style=for-the-badge)](https://github.com/annisadanish)

---

## Overview

Phishing attacks remain one of the most common vectors for credential theft
and malware delivery. PhishScope explores whether **URL-level features alone**
(without page content) are enough to distinguish phishing URLs from legitimate
ones.

The project covers the full pipeline:

1. Prepare and clean a labeled URL dataset
2. Extract lexical, structural, and statistical URL features
3. Train and evaluate a classifier
4. Serve predictions through a lightweight web app

---

## Project Structure

    PhishScope/
    ├── app.py                       # Web interface (predict from input URL)
    ├── url_features.py              # Feature extraction from URLs
    ├── prepare_data.py              # Dataset cleaning and splitting
    ├── inspect_data.py              # Quick EDA on the dataset
    ├── train_model.py               # Model training + evaluation
    ├── create_evaluation_report.py  # Generate evaluation report
    ├── PROJECT_REPORT.md            # Detailed project write-up
    ├── README.md
    ├── requirements.txt
    └── .gitignore

---

## Features

| Category | Examples |
|---|---|
| **Lexical** | URL length, number of dots, hyphens, digits, special chars |
| **Structural** | Presence of IP address, `@` symbol, subdomain depth |
| **Security** | Use of HTTPS, presence of suspicious TLDs |
| **Token-based** | Count of suspicious keywords (`login`, `verify`, `secure`, etc.) |

---

## Installation

    git clone git@github.com:annisadanish/PhishScope.git
    cd PhishScope
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

---

## Usage

### 1. Prepare the dataset

    python prepare_data.py

### 2. Inspect the data (optional)

    python inspect_data.py

### 3. Train the model

    python train_model.py

### 4. Generate the evaluation report

    python create_evaluation_report.py

### 5. Run the web app

    python app.py

Then open the local URL shown in the terminal (usually `http://127.0.0.1:5000`).

---

## Model

- **Algorithm:** (see `train_model.py`)
- **Features:** extracted by `url_features.py`
- **Evaluation:** accuracy, precision, recall, F1, confusion matrix

See `PROJECT_REPORT.md` for the full methodology, dataset description, and
results.

---

## Dataset

The dataset consists of labeled URLs (phishing / legitimate). Preprocessing
and cleaning steps are handled in `prepare_data.py`.

> Raw datasets are not committed to this repository. Use `prepare_data.py`
> to reproduce the training set locally.

---

## Ethical Use

This project is intended for:

- **Educational purposes**
- **Defensive security research**
- **Personal or organizational phishing detection**

Do **not** use this tool to generate, distribute, or promote phishing URLs.

---

## Roadmap

- [ ] Add more features (WHOIS age, TLS cert info)
- [ ] Compare multiple models (Logistic Regression, Random Forest, XGBoost)
- [ ] Add SHAP-based feature importance
- [ ] Package as a CLI tool
- [ ] Deploy as a public API

---

## License

MIT — see [LICENSE](LICENSE).

## Author

**Annisa Danish** — [github.com/annisadanish](https://github.com/annisadanish)
