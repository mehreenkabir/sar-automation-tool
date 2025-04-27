# Privacy Risk Dashboard

Scans CSV files for privacy risks like exposed personal data and expired records. Calculates a risk score and generates a full report in Markdown and JSON formats.

## Features
- Detects high-risk fields like email, IP address, DOB
- Flags old records that violate retention rules
- Calculates total risk score
- Creates Markdown and JSON reports
- Run from the command line

## How to Run

1. Install required libraries:

   ```bash
   pip install -r requirements.txt
2. Scan a CSV file:


   ```bash
   python scripts/scanner.py --file data/sample_data.csv

3. Find your reports inside the reports/ folder.

License
MIT License © Mehreen Kabir


