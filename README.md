# SAR Automation Tool

This project was designed as a complete simulation of a real-world, production-ready system for managing Subject Access Requests (SARs). It embodies the decision-making, systems thinking, and 
accountability expected from a Director of Privacy Engineering. Every function, log, and output was implemented to meet real compliance demands—not as an academic exercise, but as a job-ready 
demonstration.

This is not a proof of concept. It's a fully operational privacy automation workflow built with engineering precision and regulatory alignment at its core.

---

## Features

- **Role-Based Data Redaction** — Data access adjusts dynamically based on the requester's role (user, analyst, admin), enforcing least-privilege access control.
- **Consent Enforcement** — Requests are blocked when consent is missing, malformed, or invalid, aligning with GDPR Article 6 and similar global statutes.
- **Structured SAR Output** — Markdown reports are auto-generated for each request with clear formatting and embedded metadata.
- **Audit Logging with Timestamps** — Logs include full execution context for every request, supporting internal and external audits.
- **Edge-Case Tolerant Input Parsing** — Handles character encoding, incomplete data, and inconsistent schema with fault tolerance.
- **Verified with 13 Test Cases** — Pytest suite includes validation of role-based redaction, malformed inputs, invalid consent, and system resilience.

---

## Project Layout

```
sar-automation-tool/
├── scripts/                  # Core SAR logic
│   └── sar_engine.py
├── test_sar_engine.py        # Full test suite
├── data/                     # Sample CSV input
├── logs/                     # Action logs
├── responses/                # Generated reports
├── requirements.txt          # Dependency list
└── README.md
```

---

## Run the Tests

```bash
source venv/bin/activate
pytest test_sar_engine.py
```

Expected output:
```
collected 13 items

... all tests passing
```

---

## Using the Tool

1. Place your CSV data files (`users.csv`, `purchases.csv`) into the `data/` directory.
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Submit a SAR request using:
   ```bash
   python scripts/sar_engine.py --email user@example.com --role user
   ```
4. The tool will validate consent, redact data based on role, generate a markdown report, and log the action.

Output will appear in the `responses/` folder, and a timestamped log will be saved in `logs/`.

---

## License

MIT License © Mehreen Kabir

