"""Safe feature extraction for PhishScope.

This module analyzes only the URL text. It never connects to the website.
"""

import ipaddress
from urllib.parse import urlparse


SUSPICIOUS_WORDS = [
    "account",
    "banking",
    "confirm",
    "login",
    "password",
    "secure",
    "signin",
    "update",
    "verify",
]


def prepare_url(url):
    """Add a scheme so urlparse can identify the hostname correctly."""
    url = url.strip()
    if "://" not in url:
        url = "http://" + url
    return url


def hostname_is_ip(hostname):
    """Return True when the hostname is an IPv4 or IPv6 address."""
    if not hostname:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False


def extract_features(url):
    """Extract simple, explainable characteristics from a URL."""
    prepared_url = prepare_url(url)
    parsed = urlparse(prepared_url)
    hostname = parsed.hostname or ""
    lower_url = prepared_url.lower()

    suspicious_words_found = []
    for word in SUSPICIOUS_WORDS:
        if word in lower_url:
            suspicious_words_found.append(word)

    return {
        "url_length": len(prepared_url),
        "hostname": hostname,
        "uses_https": parsed.scheme.lower() == "https",
        "hostname_is_ip": hostname_is_ip(hostname),
        "dot_count": hostname.count("."),
        "hyphen_count": hostname.count("-"),
        "at_symbol_count": prepared_url.count("@"),
        "digit_count": sum(character.isdigit() for character in prepared_url),
        "suspicious_words": suspicious_words_found,
    }


def calculate_risk(features):
    """Calculate a transparent risk score and return its explanations."""
    score = 0
    reasons = []

    if features["hostname_is_ip"]:
        score += 30
        reasons.append("The hostname is an IP address instead of a domain name.")

    if features["url_length"] > 75:
        score += 20
        reasons.append("The URL is unusually long.")

    if features["dot_count"] >= 4:
        score += 15
        reasons.append("The hostname contains many dots or possible subdomains.")

    if features["at_symbol_count"] > 0:
        score += 20
        reasons.append("The URL contains an @ symbol, which can hide its destination.")

    if features["hyphen_count"] >= 2:
        score += 10
        reasons.append("The hostname contains multiple hyphens.")

    if features["digit_count"] >= 6:
        score += 10
        reasons.append("The URL contains many digits.")

    if features["suspicious_words"]:
        score += min(20, len(features["suspicious_words"]) * 5)
        words = ", ".join(features["suspicious_words"])
        reasons.append("Potentially misleading words were found: " + words + ".")

    if not features["uses_https"]:
        score += 5
        reasons.append("The URL does not use HTTPS. This alone does not prove phishing.")

    score = min(score, 100)

    if score >= 60:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    if not reasons:
        reasons.append("No indicators used by this prototype were detected.")

    return score, level, reasons
