import os
import pytest
import pandas as pd
from datetime import datetime
import sys

scripts_path = os.path.abspath("scripts")
sys.path.insert(0, scripts_path)

from sar_engine import filter_by_email, redact_field, generate_markdown_report, log_request, ROLE_FIELDS

@pytest.fixture
def user_data():
    return pd.DataFrame([{
        "user_id": 1,
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "phone_number": "123-456-7890",
        "date_of_birth": "1990-01-01",
        "consent_given": True,
        "created_at": "2020-01-01"
    }])

@pytest.fixture
def purchase_data():
    return pd.DataFrame([{
        "user_id": 1,
        "purchase_date": "2023-01-01",
        "product_name": "Privacy Book",
        "amount": 29.99,
        "currency": "USD"
    }])

@pytest.fixture
def user_data_no_consent():
    return pd.DataFrame([{
        "user_id": 2,
        "full_name": "No Consent",
        "email": "noconsent@example.com",
        "phone_number": "000-000-0000",
        "date_of_birth": "1980-01-01",
        "consent_given": False,
        "created_at": "2019-01-01"
    }])

def test_filter_by_email(user_data):
    result = filter_by_email(user_data, "jane@example.com")
    assert not result.empty
    assert result.iloc[0]["full_name"] == "Jane Doe"

def test_redact_field_user():
    assert redact_field("123-456-7890", "phone_number", "user") == "[REDACTED]"
    assert redact_field("jane@example.com", "email", "user") == "[REDACTED]"

def test_redact_field_analyst():
    assert redact_field("123-456-7890", "phone_number", "analyst") == "[REDACTED]"
    assert redact_field("jane@example.com", "email", "analyst") == "jane@example.com"

def test_redact_field_admin():
    assert redact_field("123-456-7890", "phone_number", "admin") == "123-456-7890"

def test_generate_markdown_report(tmp_path, user_data, purchase_data):
    os.makedirs("responses", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = generate_markdown_report(user_data, purchase_data, "user", timestamp)
    assert filename is not None
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        contents = f.read()
        assert "Subject Access Report" in contents
        assert "[REDACTED]" in contents

def test_log_request():
    os.makedirs("logs", exist_ok=True)
    log_file = "logs/sar_audit_log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)
    log_request("jane@example.com", "user", 0.45)
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        log_contents = f.read()
        assert "SAR submitted for: jane@example.com" in log_contents

def test_consent_flag_blocks_processing(user_data_no_consent):
    assert user_data_no_consent.iloc[0]["consent_given"] == False

def test_email_not_found_returns_empty():
    df = pd.DataFrame([{ "email": "nobody@example.com" }])
    result = filter_by_email(df, "notfound@example.com")
    assert result.empty

def test_generate_report_no_purchases(tmp_path, user_data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = generate_markdown_report(user_data, pd.DataFrame(), "user", timestamp)
    assert filename is not None
    with open(filename, "r") as f:
        contents = f.read()
        assert "No purchases found." in contents

def test_invalid_role_redaction():
    result = redact_field("secret@example.com", "email", "intern")
    assert result == "secret@example.com"

def test_log_request_appends():
    log_file = "logs/sar_audit_log.txt"
    os.makedirs("logs", exist_ok=True)
    log_request("a@example.com", "admin", 0.10)
    log_request("b@example.com", "user", 0.20)
    with open(log_file, "r") as f:
        lines = f.readlines()
        assert any("a@example.com" in line for line in lines)
        assert any("b@example.com" in line for line in lines)

def test_consent_as_string_true():
    df = pd.DataFrame([{ "consent_given": "True" }])
    assert str(df.iloc[0]["consent_given"]).lower() == "true"

def test_special_characters_in_report(tmp_path):
    df = pd.DataFrame([{
        "user_id": 3,
        "full_name": "🚀 Zé Testé",
        "email": "ze@example.com",
        "phone_number": "+33-123-456",
        "date_of_birth": "1988-07-04",
        "consent_given": True,
        "created_at": "2022-03-01"
    }])
    purchases = pd.DataFrame()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = generate_markdown_report(df, purchases, "user", timestamp)
    with open(filename, "r") as f:
        contents = f.read()
        assert "Zé Testé" in contents
        assert "🚀" in contents

