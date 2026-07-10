# PhishScope
A phishing URL risk analyzer with machine learning and transparent security rules.
# PhishScope

PhishScope is a beginner-friendly phishing URL risk analyzer built with Python, Streamlit, and machine learning. It examines the text of a URL without opening the website, making the analysis safer for educational use.

The project combines:

- a decision-tree machine-learning model;
- transparent URL security rules;
- an uncertainty warning when the two methods disagree.

## How it works

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

- an ML phishing estimate;
- a rule-based risk score;
- transparent risk indicators;
- a combined assessment.

PhishScope never visits or downloads content from the submitted website.

## Model results

The models were trained and tested using 235,370 unique URLs after duplicate removal.

| Model | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Dummy baseline | 57.29% | 0.00% | 0.00% | 0.00% |
| Logistic regression | 94.47% | 97.22% | 89.61% | 93.26% |
| Decision tree | **96.33%** | **97.74%** | **93.57%** | **95.61%** |

The decision tree was selected because it achieved the highest phishing F1-score.

![Model comparison](reports/model_comparison.png)

![Confusion matrix](reports/confusion_matrix.png)

## Important limitation

During additional testing, the model incorrectly gave `https://example.com/about` a high phishing estimate. The rule-based system found no suspicious indicators.

Instead of hiding this failure, PhishScope reports:

> **Uncertain — the model and transparent rules disagree.**

This demonstrates that high test accuracy does not guarantee reliable predictions for every new URL. HTTPS is also not proof that a website is trustworthy because phishing websites can use valid TLS certificates.

## Run the project

Install the required packages:

```bash
pip install -r requirements.txt
