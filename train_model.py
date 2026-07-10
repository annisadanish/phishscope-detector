"""Train and compare beginner-friendly phishing URL models."""

import os

import joblib
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


data_path = os.path.join("data", "processed_urls.csv")
model_folder = "models"
model_path = os.path.join(model_folder, "phishscope_model.joblib")

feature_names = [
    "url_length",
    "uses_https",
    "hostname_is_ip",
    "dot_count",
    "hyphen_count",
    "at_symbol_count",
    "digit_count",
    "suspicious_word_count",
]


def evaluate_model(name, model, x_test, y_test):
    """Print security-focused test results and return the phishing F1-score."""
    predictions = model.predict(x_test)
    matrix = confusion_matrix(y_test, predictions)

    print("\n" + name)
    print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("Precision:", round(precision_score(y_test, predictions), 4))
    print("Recall:", round(recall_score(y_test, predictions), 4))
    print("F1-score:", round(f1_score(y_test, predictions), 4))
    print("Confusion matrix:")
    print(matrix)
    print("Rows = actual [legitimate, phishing]")
    print("Columns = predicted [legitimate, phishing]")

    return f1_score(y_test, predictions)


if not os.path.exists(data_path):
    print("ERROR: The processed dataset could not be found.")
    print("Run prepare_data.py first.")
else:
    print("Loading processed data...")
    data = pd.read_csv(data_path)

    x = data[feature_names]

    # Original dataset: 0 = phishing and 1 = legitimate.
    # Our model target: 1 = phishing and 0 = legitimate.
    # This makes phishing the positive class in precision, recall, and F1-score.
    y = (data["label"] == 0).astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("Training rows:", len(x_train))
    print("Testing rows:", len(x_test))
    print("1 = phishing, 0 = legitimate")

    models = {
        "Dummy baseline": DummyClassifier(strategy="most_frequent"),
        "Logistic regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, random_state=42),
        ),
        "Decision tree": DecisionTreeClassifier(
            max_depth=8,
            min_samples_leaf=20,
            random_state=42,
        ),
    }

    best_name = ""
    best_model = None
    best_f1 = -1

    for name, model in models.items():
        print("\nTraining", name + "...")
        model.fit(x_train, y_train)
        model_f1 = evaluate_model(name, model, x_test, y_test)

        if name != "Dummy baseline" and model_f1 > best_f1:
            best_name = name
            best_model = model
            best_f1 = model_f1

    os.makedirs(model_folder, exist_ok=True)

    saved_package = {
        "model": best_model,
        "feature_names": feature_names,
        "model_name": best_name,
        "phishing_is_positive_class": True,
    }
    joblib.dump(saved_package, model_path)

    print("\nBEST MODEL")
    print("Model:", best_name)
    print("Phishing F1-score:", round(best_f1, 4))
    print("Saved to:", model_path)
