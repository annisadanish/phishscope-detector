import os

import joblib
import pandas as pd
import streamlit as st

from url_features import calculate_risk, extract_features


st.set_page_config(page_title="PhishScope", page_icon="🔎")


@st.cache_resource
def load_saved_model():
    model_path = os.path.join("models", "phishscope_model.joblib")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


def make_model_input(features, feature_names):
    """Convert extracted URL characteristics into one model input row."""
    row = {
        "url_length": features["url_length"],
        "uses_https": int(features["uses_https"]),
        "hostname_is_ip": int(features["hostname_is_ip"]),
        "dot_count": features["dot_count"],
        "hyphen_count": features["hyphen_count"],
        "at_symbol_count": features["at_symbol_count"],
        "digit_count": features["digit_count"],
        "suspicious_word_count": len(features["suspicious_words"]),
    }
    return pd.DataFrame([row], columns=feature_names)

st.title("PhishScope")
st.write("An explainable phishing-link risk analyzer for cybersecurity education.")
st.info("This tool analyzes the URL text only. It does not open the website.")

saved_package = load_saved_model()

url = st.text_input("Paste a URL", placeholder="https://example.com/login")

if st.button("Analyze URL"):
    if not url.strip():
        st.warning("Please enter a URL first.")
    else:
        features = extract_features(url)
        rule_score, rule_level, reasons = calculate_risk(features)

        st.subheader("Result")

        if saved_package is not None:
            model_input = make_model_input(
                features,
                saved_package["feature_names"],
            )
            model = saved_package["model"]
            prediction = model.predict(model_input)[0]
            probability = model.predict_proba(model_input)[0][1]

            first_column, second_column = st.columns(2)
            first_column.metric(
                "ML phishing estimate",
                str(round(probability * 100, 1)) + "%",
            )
            second_column.metric("Rule-based score", str(rule_score) + "/100")

            model_says_phishing = prediction == 1
            rules_say_suspicious = rule_score >= 30

            if model_says_phishing and rules_say_suspicious:
                st.error("Combined assessment: Potential phishing")
            elif not model_says_phishing and not rules_say_suspicious:
                st.success("Combined assessment: Likely legitimate")
            else:
                st.warning(
                    "Combined assessment: Uncertain — the model and transparent "
                    "rules disagree. Verify the link independently."
                )

            st.caption("Model used: " + saved_package["model_name"])
        else:
            st.warning("Trained model not found. Showing rule-based analysis only.")
            st.metric("Rule-based score", str(rule_score) + "/100")

            if rule_level == "High":
                st.error("Rule-based risk level: High")
            elif rule_level == "Medium":
                st.warning("Rule-based risk level: Medium")
            else:
                st.success("Rule-based risk level: Low")

        st.subheader("Transparent rule indicators")
        for reason in reasons:
            st.write("- " + reason)

        st.subheader("Extracted features")
        st.json(features)

        st.caption(
            "The ML estimate and rule score are educational estimates, not proof "
            "that a website is safe or malicious. Verify uncertain links through "
            "the official website."
        )
