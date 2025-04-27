import pandas as pd
import os

HIGH_RISK_FIELDS = ['full_name', 'email', 'ip_address', 'date_of_birth']
RETENTION_PERIOD_YEARS = 5

def scan_file(file_path):
    risks = []
    df = pd.read_csv(file_path)

    # Check for presence of high-risk fields
    for field in HIGH_RISK_FIELDS:
        if field in df.columns:
            risks.append({
                'type': 'High-Risk PII Detected',
                'field': field,
                'gdpr_reference': 'GDPR Article 4(1) - Personal Data Definition'
            })

    # Check for expired records
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        expired = df[df['created_at'] < pd.Timestamp.now() - pd.DateOffset(years=RETENTION_PERIOD_YEARS)]
        if not expired.empty:
            risks.append({
                'type': 'Data Retention Violation',
                'field': 'created_at',
                'gdpr_reference': 'GDPR Article 5 - Storage Limitation',
                'count': len(expired)
            })

    return risks

from risk_scorer import calculate_risk_score
from report_generator import generate_markdown_report, generate_json_report
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Privacy Risk Scanner")
    parser.add_argument('--file', required=True, help='Path to the CSV file to scan')
    args = parser.parse_args()

    file_path = args.file
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        exit(1)

    risks = scan_file(file_path)
    risk_summary = calculate_risk_score(risks)

    print("\n--- Risk Summary ---")
    print(f"Total Risks: {risk_summary['total_risks']}")
    print(f"Score: {risk_summary['total_score']}")
    print(f"Level: {risk_summary['risk_level']}\n")

    generate_markdown_report(risks, risk_summary)
    generate_json_report(risks, risk_summary)

