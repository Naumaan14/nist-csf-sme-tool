# NIST CSF 2.0 Risk Assessment Tool
## CO7047 Research Project | MSc Cybersecurity | University of Chester
**Author:** Nauman Salimbhai Shaikh | Student No. 2527627  
**Supervisor:** Dr Bismark Asare

---

## Overview
A free, web-based cybersecurity risk assessment tool for Small and Medium-sized
Enterprises (SMEs), grounded in the NIST Cybersecurity Framework 2.0.

The tool guides non-technical users through 30 questions across all six NIST CSF
functions (Govern, Identify, Protect, Detect, Respond, Recover) and produces:
- A weighted risk score per function (1–25 scale)
- An overall weighted risk score and level (High / Medium / Low)
- A maturity level per function (Partial → Adaptive, aligned to NIST CSF 2.0 Tiers)
- Three prioritised recommendations per function
- An Excel export compatible with Power BI (3 sheets: Summary, Detail, Raw Data)

---

## System Flow
```
User Inputs (30 Likert-scale responses)
        ↓
NIST CSF 2.0 Control Mapping (engine.py)
        ↓
Risk Formula: Likelihood × Impact
        ↓
Apply Function Weights (GV:20%, ID:20%, PR:25%, DE:15%, RS:10%, RC:10%)
        ↓
Calculate Scores (per function + overall weighted)
        ↓
Generate Risk Level + Maturity Tier
        ↓
Provide Prioritised Recommendations
        ↓
(Optional) Export to Excel / Power BI
```

---

## Installation

### Requirements
- Python 3.9 or higher
- pip

### Install dependencies
```bash
pip install flask openpyxl
```

---

## Running the Tool

### Web application (recommended)
```bash
cd nist_tool
python app.py
```
Then open your browser at: **http://localhost:5050**

### Command-line / scripting use
```python
from engine import calculate_results
from export import generate_excel

responses = {
    'Govern':   [3, 2, 1, 3, 2],
    'Identify': [2, 1, 2, 1, 3],
    'Protect':  [4, 2, 3, 2, 3],
    'Detect':   [2, 2, 1, 2, 2],
    'Respond':  [1, 1, 2, 2, 3],
    'Recover':  [2, 3, 1, 2, 2],
}

results = calculate_results(responses)
print(results['overall_score'], results['overall_level'])

# Export to Excel
xlsx_bytes = generate_excel(results, 'My Organisation')
with open('report.xlsx', 'wb') as f:
    f.write(xlsx_bytes)
```

---

## File Structure
```
nist_tool/
├── app.py          # Flask web application (routes + session handling)
├── engine.py       # Core risk engine (questions, scoring, recommendations)
├── export.py       # Excel / Power BI export module
├── templates/
│   ├── index.html  # Landing page
│   ├── assess.html # Assessment questionnaire (stepped, one function per page)
│   └── results.html# Results dashboard with charts and recommendations
└── README.md       # This file
```

---

## Risk Scoring Formula
```
avg_score    = mean of 5 responses for a function (1–5 scale)
likelihood   = (5 - avg_score) + 1   [inverted: lower score = higher likelihood]
impact       = predefined per function (derived from DCMS 2023 breach data)
risk_score   = likelihood × impact    [1–25 scale]
weighted     = risk_score × function_weight
overall      = sum of all weighted scores
```

### Risk Level Thresholds (NIST SP 800-30)
| Score Range | Risk Level |
|-------------|-----------|
| > 15        | High      |
| 8 – 15      | Medium    |
| < 8         | Low       |

### Maturity Levels (NIST CSF 2.0 Implementation Tiers)
| Avg Score | Maturity Level              |
|-----------|-----------------------------|
| 1.0 – 2.0 | Level 1 — Partial           |
| 2.1 – 3.0 | Level 2 — Risk-Informed     |
| 3.1 – 4.0 | Level 3 — Repeatable        |
| 4.1 – 5.0 | Level 4 — Adaptive          |

---

## References
- NIST. (2024). Cybersecurity Framework 2.0. https://doi.org/10.6028/NIST.CSWP.29
- NIST. (2012). NIST SP 800-30 Rev. 1. https://doi.org/10.6028/NIST.SP.800-30r1
- Paulsen & Toth. (2016). NISTIR 7621 Rev. 1. https://doi.org/10.6028/NIST.IR.7621r1
- DCMS. (2023). Cyber Security Breaches Survey 2023.
