# PhishScope: Explainable Phishing URL Risk Analysis

## 1. Project summary

PhishScope is a beginner-friendly cybersecurity application that estimates the
risk of a URL without opening the website. It combines a machine-learning model
with transparent security rules and reports uncertainty when the two methods
disagree.

## 2. Research question

Can a lightweight and explainable system identify potentially malicious URLs
using only characteristics extracted safely from the URL text?

## 3. Dataset

The project uses the PhiUSIIL Phishing URL Dataset from the UCI Machine Learning
Repository. The original dataset contains 235,795 records: 100,945 phishing URLs
and 134,850 legitimate URLs. In the source data, label 0 means phishing and label
1 means legitimate.

Source: [UCI PhiUSIIL dataset](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset)

## 4. Data preparation

The original data contained no missing values and 425 duplicate URLs. No URL had
conflicting labels. Duplicate records were removed, leaving 235,370 unique URLs.

Only URL-text features were used. This prevents a mismatch between training and
deployment because the application does not visit a submitted website to inspect
its HTML content.

The eight model features are:

1. URL length
2. HTTPS usage
3. IP address used as the hostname
4. Number of dots
5. Number of hyphens
6. Number of @ symbols
7. Number of digits
8. Number of suspicious words

## 5. Experimental design

The clean dataset was divided into 80% training data and 20% testing data. The
split was stratified so both portions retained approximately the same phishing
and legitimate class distribution. A fixed random state of 42 made the
experiment reproducible.

Three models were compared:

- A dummy majority-class baseline
- Logistic regression with standardized features
- A decision tree limited to depth 8 with at least 20 training examples per leaf

Phishing was converted to positive class 1 for evaluation. This makes precision,
recall, and F1-score describe phishing detection rather than legitimate-URL
detection.

## 6. Results

| Model | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Dummy baseline | 57.29% | 0.00% | 0.00% | 0.00% |
| Logistic regression | 94.47% | 97.22% | 89.61% | 93.26% |
| Decision tree | 96.33% | 97.74% | 93.57% | 95.61% |

The dummy model demonstrates why accuracy alone is inadequate: it obtained
57.29% accuracy by always predicting the majority class but detected no phishing
URLs. The decision tree achieved the highest phishing F1-score and was therefore
selected for the application.

On 47,074 test records, the decision tree:

- correctly classified 26,535 legitimate URLs;
- falsely flagged 435 legitimate URLs;
- missed 1,293 phishing URLs; and
- correctly detected 18,811 phishing URLs.

## 7. Explainability and application design

The interface presents the model estimate beside a separate rule-based score.
It uses three combined outcomes:

- **Potential phishing:** both methods identify risk.
- **Likely legitimate:** both methods identify low risk.
- **Uncertain:** the methods disagree and independent verification is advised.

This design does not claim that a model estimate is proof of maliciousness.

## 8. Sanity testing and discovered limitation

Additional examples outside the train-test evaluation exposed a false positive.
The model gave `https://example.com/about` a 100% phishing estimate while the
transparent rules found no risk indicators. The application now reports this
disagreement as uncertain.

Feature importance showed that HTTPS usage and digit count dominated the
decision tree. This may reflect patterns in the dataset rather than permanent
properties of phishing. HTTPS encrypts communication but does not establish
that the operator of a website is trustworthy. Research has documented phishing
websites using valid TLS certificates, so HTTPS must not be interpreted as a
safety guarantee.

Supporting research: [USENIX study of certificates used by phishing websites](https://www.usenix.org/system/files/soups2019-drury.pdf)

## 9. Ethical and safety controls

- The application analyzes URL text without opening the destination.
- Testing uses reserved example domains and private IP addresses.
- The application does not exploit, scan, download, or interact with websites.
- Results are presented as educational estimates rather than confirmed verdicts.

## 10. Future improvements

1. Evaluate with a time-separated or external dataset to measure generalization.
2. Calibrate model estimates to reduce decision-tree overconfidence.
3. Add safe lexical features such as path length, query count, and character
   entropy.
4. Test domain-grouped splitting to reduce similarity leakage between training
   and testing data.
5. Study brand-domain mismatches and typosquatting without visiting websites.

## 11. Conclusion

PhishScope shows that lightweight URL-text features can support phishing risk
analysis while remaining safe and explainable. The decision tree substantially
outperformed the baseline and logistic regression on the held-out data. However,
the external sanity check revealed that high test performance does not guarantee
reliable behavior for every new domain. The hybrid uncertainty state is therefore
an essential part of the system rather than a cosmetic interface feature.
