import os
import json

def generate_markdown_report(risks, risk_summary, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "privacy_risk_report.md")

    with open(report_path, "w") as f:
        f.write(f"# Privacy Risk Assessment Report\n\n")
        f.write(f"**Total Risks Identified:** {risk_summary['total_risks']}\n\n")
        f.write(f"**Overall Risk Score:** {risk_summary['total_score']}\n")
        f.write(f"**Risk Level:** {risk_summary['risk_level']}\n\n")
        f.write("---\n\n")
        f.write("## Detailed Risks:\n")
        for risk in risks:
            f.write(f"- **Type:** {risk['type']} | **Field:** {risk['field']} | **GDPR Ref:** {risk['gdpr_reference']}\n")

    print(f"Markdown report saved to: {report_path}")

def generate_json_report(risks, risk_summary, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "privacy_risk_report.json")

    output = {
        'summary': risk_summary,
        'detailed_risks': risks
    }

    with open(report_path, "w") as f:
        json.dump(output, f, indent=4)

    print(f"JSON report saved to: {report_path}")

