import pandas as pd
from datetime import datetime
import os
import sys
import argparse

ROLE_FIELDS = {
    "user": ["email", "phone_number"],
    "analyst": ["phone_number"],
    "admin": []
}

def load_user_data():
    try:
        return pd.read_csv("data/users.csv")
    except Exception as e:
        print(f"Error loading user data: {e}")
        sys.exit(1)

def load_purchase_data():
    try:
        return pd.read_csv("data/purchases.csv")
    except Exception as e:
        print(f"Error loading purchase data: {e}")
        sys.exit(1)

def filter_by_email(df, email):
    return df[df["email"] == email]

def log_request(email, role, duration):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] SAR submitted for: {email} with role: {role}, duration: {duration:.2f} seconds\n"
    try:
        with open("logs/sar_audit_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Error writing to audit log: {e}")

def redact_field(value, field_name, role):
    if field_name in ROLE_FIELDS.get(role, []):
        return "[REDACTED]"
    return value

def generate_markdown_report(user_row, purchases, role, timestamp):
    user = user_row.iloc[0]
    filename = f"responses/sar_report_{timestamp}.md"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Subject Access Report - {user['full_name']}\n\n")
            f.write(f"**Email:** {redact_field(user['email'], 'email', role)}\n")
            f.write(f"**Date of Birth:** {user['date_of_birth']}\n")
            f.write(f"**Phone Number:** {redact_field(user['phone_number'], 'phone_number', role)}\n")
            f.write(f"**Consent Given:** {user['consent_given']}\n")
            f.write(f"**Created At:** {user['created_at']}\n\n")
            f.write("## Purchase History\n")
            if not purchases.empty:
                for _, p in purchases.iterrows():
                    f.write(f"- {p['purchase_date']}: {p['product_name']} (${p['amount']} {p['currency']})\n")
            else:
                f.write("No purchases found.\n")
    except Exception as e:
        print(f"Error writing markdown report: {e}")
        return None
    return filename

def safe_input(prompt, fallback=None):
    try:
        return input(prompt)
    except (EOFError, OSError):
        return fallback

def main():
    parser = argparse.ArgumentParser(description="Process a Subject Access Request")
    parser.add_argument("--email", required=False, help="User's email")
    parser.add_argument("--role", required=False, help="Access role: user, analyst, admin")
    parser.add_argument("--output", choices=["md", "pdf"], default="md", help="Report output format")
    args = parser.parse_args()

    email = args.email or safe_input("Enter the user email to process SAR: ")
    role = args.role or safe_input("Enter your role (user, analyst, admin): ")

    if not email or not role:
        print("Missing input. Please specify both email and role.")
        return

    email = email.strip()
    role = role.strip().lower()

    if role not in ROLE_FIELDS:
        print("Invalid role provided.")
        return

    users = load_user_data()
    purchases = load_purchase_data()
    match = filter_by_email(users, email)

    if match.empty:
        print("No user found with that email.")
        return

    if not bool(match.iloc[0]['consent_given']):
        print("User has not given consent. SAR will not be fulfilled.")
        return

    user_id = match.iloc[0]["user_id"]
    user_purchases = purchases[purchases["user_id"] == user_id]

    start_time = datetime.now()
    timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    md_file = generate_markdown_report(match, user_purchases, role, timestamp)

    if md_file:
        if args.output == "pdf":
            print("PDF generation is currently disabled due to missing system dependencies.")
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        log_request(email, role, duration)
        print(f"Markdown report saved to: {md_file}")
    else:
        print("Failed to generate markdown report.")

if __name__ == "__main__":
    main()

