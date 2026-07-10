# PhishScope

PhishScope is a beginner-friendly phishing URL risk analyzer built with Python, Streamlit, and machine learning. It examines the text of a URL without opening the website, making the analysis safer for educational use.

The project combines:

- A decision-tree machine-learning model
- Transparent URL security rules
- An uncertainty warning when the model and rules disagree

## Process

PhishScope extracts eight features from the submitted URL:

- URL length
- HTTPS usage
- IP-address hostname
- Number of dots
- Number of hyphens
- Number of `@` symbols
- Number of digits
- Suspicious words such as `login`, `verify`, and `account`

The application then displays:

- An ML phishing estimate
- A rule-based risk score
- Transparent risk indicators
- A combined assessment

PhishScope never visits or downloads content from the submitted website.

## Model Results

The models were trained and tested using **235,370 unique URLs** after duplicate removal.

| Model | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Dummy baseline | 57.29% | 0.00% | 0.00% | 0.00% |
| Logistic regression | 94.47% | 97.22% | 89.61% | 93.26% |
| Decision tree | **96.33%** | **97.74%** | **93.57%** | **95.61%** |

The decision tree was selected because it achieved the highest phishing F1-score.

![Model comparison](reports/model_comparison.png)

![Confusion matrix](reports/confusion_matrix.png)

![Feature importance](reports/feature_importance.png)

## Limitations

During additional testing, the model incorrectly gave `https://example.com/about` a high phishing estimate. However, the rule-based system found no suspicious indicators.

Instead of hiding this failure, PhishScope reports:

> **Uncertain — the model and transparent rules disagree.**

This demonstrates that high test accuracy does not guarantee reliable predictions for every new URL.

HTTPS is also not proof that a website is trustworthy because phishing websites can use valid TLS certificates.

## How to Run the Project

### 1. Install the required packages

```bash
pip install -r requirements.txt
```

### 2. Download the dataset

Download the PhiUSIIL dataset from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset).

Place the extracted CSV file here:

```text
data/PhiUSIIL_Phishing_URL_Dataset.csv
```

### 3. Inspect and prepare the dataset

```bash
python inspect_data.py
python prepare_data.py
```

### 4. Train the models

```bash
python train_model.py
```

### 5. Generate the evaluation charts

```bash
python create_evaluation_report.py
```

### 6. Start PhishScope

```bash
streamlit run app.py
```

Streamlit should display a local address, normally:

```text
http://localhost:8501
```

## Project Structure

```text
phishscope/
├── app.py
├── url_features.py
├── inspect_data.py
├── prepare_data.py
├── train_model.py
├── create_evaluation_report.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
├── LICENSE
├── data/
│   └── README.md
├── models/
│   └── README.md
├── reports/
│   ├── evaluation_results.csv
│   ├── model_comparison.png
│   ├── confusion_matrix.png
│   └── feature_importance.png
└── tests/
    └── test_url_features.py
```

## Main Project Files

- `app.py` — Streamlit application
- `url_features.py` — URL feature extraction and transparent rules
- `inspect_data.py` — Initial dataset-quality inspection
- `prepare_data.py` — Duplicate removal and feature preparation
- `train_model.py` — Model training and evaluation
- `create_evaluation_report.py` — Evaluation-chart generation
- `PROJECT_REPORT.md` — Complete methodology, results, and limitations
- `tests/test_url_features.py` — Automated feature tests

## Dataset and References

1. Prasad, A., and Chandra, S. (2024). *PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning*. Computers & Security, 136, 103545.  
   [Read the research paper](https://doi.org/10.1016/j.cose.2023.103545)

2. UCI Machine Learning Repository. *PhiUSIIL Phishing URL Dataset*.  
   [View the official dataset](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset)

3. Drury, V., and Meyer, U. (2019). *Taking a Look at Public Key Certificates of Phishing Websites*. Symposium on Usable Privacy and Security.  
   [Read the USENIX paper](https://www.usenix.org/system/files/soups2019-drury.pdf)

## Ethical Use

PhishScope is intended for defensive cybersecurity education.

It does not:

- Open submitted URLs
- Scan remote systems
- Download website content
- Exploit security vulnerabilities
- Confirm with certainty that a URL is malicious

Test it only with reserved example domains, private IP addresses, or data you are authorized to analyze.
