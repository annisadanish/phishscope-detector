"""Create portfolio-ready evaluation files for PhishScope."""

import os

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


data_path = os.path.join("data", "processed_urls.csv")
report_folder = "reports"

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


def calculate_metrics(model, x_test, y_test):
    predictions = model.predict(x_test)
    return {
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions, zero_division=0),
        "Recall": recall_score(y_test, predictions, zero_division=0),
        "F1-score": f1_score(y_test, predictions, zero_division=0),
    }, predictions


if not os.path.exists(data_path):
    print("ERROR: Processed data not found. Run prepare_data.py first.")
else:
    os.makedirs(report_folder, exist_ok=True)

    print("Loading processed data...")
    data = pd.read_csv(data_path)
    x = data[feature_names]
    y = (data["label"] == 0).astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

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

    results = []
    decision_tree = None
    tree_predictions = None

    for model_name, model in models.items():
        print("Training", model_name + "...")
        model.fit(x_train, y_train)
        metrics, predictions = calculate_metrics(model, x_test, y_test)
        metrics["Model"] = model_name
        results.append(metrics)

        if model_name == "Decision tree":
            decision_tree = model
            tree_predictions = predictions

    results_data = pd.DataFrame(results)
    results_data = results_data[
        ["Model", "Accuracy", "Precision", "Recall", "F1-score"]
    ]
    results_data.to_csv(
        os.path.join(report_folder, "evaluation_results.csv"),
        index=False,
    )

    # Chart 1: exact comparison of the four evaluation metrics.
    chart_data = results_data.set_index("Model") * 100
    chart_data.plot(kind="bar", figsize=(10, 6))
    plt.title("PhishScope Model Comparison")
    plt.ylabel("Score (%)")
    plt.xlabel("")
    plt.ylim(0, 105)
    plt.xticks(rotation=0)
    plt.legend(loc="lower right")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(
        os.path.join(report_folder, "model_comparison.png"),
        dpi=200,
    )
    plt.close()

    # Chart 2: confusion matrix for the selected decision tree.
    matrix = confusion_matrix(y_test, tree_predictions)
    figure, axis = plt.subplots(figsize=(6, 5))
    image = axis.imshow(matrix, cmap="Blues")
    figure.colorbar(image, ax=axis)
    axis.set_title("Decision Tree Confusion Matrix")
    axis.set_xlabel("Predicted class")
    axis.set_ylabel("Actual class")
    axis.set_xticks([0, 1], ["Legitimate", "Phishing"])
    axis.set_yticks([0, 1], ["Legitimate", "Phishing"])

    for row in range(2):
        for column in range(2):
            axis.text(
                column,
                row,
                matrix[row, column],
                ha="center",
                va="center",
                color="white" if matrix[row, column] > matrix.max() / 2 else "black",
                fontsize=12,
            )

    plt.tight_layout()
    plt.savefig(
        os.path.join(report_folder, "confusion_matrix.png"),
        dpi=200,
    )
    plt.close()

    # Chart 3: which URL-text features influenced the decision tree most.
    importance_data = pd.Series(
        decision_tree.feature_importances_,
        index=feature_names,
    ).sort_values()

    importance_data.plot(kind="barh", figsize=(9, 6))
    plt.title("Decision Tree Feature Importance")
    plt.xlabel("Importance")
    plt.ylabel("")
    plt.grid(axis="x", alpha=0.25)
    plt.tight_layout()
    plt.savefig(
        os.path.join(report_folder, "feature_importance.png"),
        dpi=200,
    )
    plt.close()

    print("\nREPORT CREATED")
    print(results_data.round(4).to_string(index=False))
    print("\nFiles saved inside:", report_folder)
    print("- evaluation_results.csv")
    print("- model_comparison.png")
    print("- confusion_matrix.png")
    print("- feature_importance.png")
