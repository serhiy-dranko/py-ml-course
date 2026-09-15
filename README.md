# Python + Snowflake + pandas — Learning Course

A structured, hands-on course covering Python fundamentals through real
Snowflake data analysis with pandas, built week by week.

## Structure

py-ml-course/
├── week-1/
│ ├── day-1/ # Python basics, environment setup
│ ├── day-2/ # Control flow & functions
│ ├── day-3/ # Core data structures (lists, dicts, sets)
│ ├── day-4/ # Files, modules, basic OOP
│ └── day-5/ # Connecting Python to Snowflake
└── week-2/
├── day-1/ # pandas fundamentals, .loc/.iloc, filtering, sorting
├── day-2/ # Missing data, merging & joining datasets
├── day-3/ # GroupBy, aggregation, NumPy basics
├── day-4/ # Exploratory Data Analysis (EDA)
└── day-5/ # Capstone: visualization + raw-vs-dbt comparison


## Setup

1. Clone the repo and create a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\Activate.ps1   # Windows
   pip install -r requirements.txt
```

2. Create a `.env` file in the project root (never committed — see `.gitignore`)
   with your own Snowflake credentials:

SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_USER=...
SNOWFLAKE_WAREHOUSE=...
SNOWFLAKE_DATABASE=...
SNOWFLAKE_SCHEMA=...
SNOWFLAKE_PRIVATE_KEY_PATH=...


3. Authentication uses **RSA key-pair auth** (not username/password) — see
   `week-1/day-5/snowflake_helpers.py` for the connection logic.

## Highlights

- `week-1/day-5/snowflake_helpers.py` — reusable Snowflake connection module
  (`get_connection()`, `run_query()`), used throughout Week 2.
- `week-2/day-2/block5_clean_and_merge.py` — reusable `clean_and_merge()`
  function combining missing-data handling and validated merges.
- `week-2/day-5/block6_final_deliverable.py` — full capstone: raw pull →
  clean/merge → aggregate → visualize → compare against dbt staging models.

## Data source

Uses Snowflake's `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` and the open-source
[Jaffle Shop](https://github.com/dbt-labs/jaffle-shop) dbt demo project data.