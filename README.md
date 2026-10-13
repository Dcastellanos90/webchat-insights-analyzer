# WebChat Insights Analyzer

A command-line tool that reads a CSV of customer chat interactions and prints
summary analytics: total chats, average response time, escalation rate,
resolution rate, chats per agent, and the most common issue categories.

## Why I built this

At work I train representatives on WebChat and analyze chat interactions to
find patterns (like what drives escalations). I wanted to recreate that kind
of analysis in code, so I built this analyzer in Python. The sample data is
100% fictional -- no real company data is used anywhere.

## How to run it

Python 3 only, no extra packages needed (uses the standard library:
`csv`, `argparse`, `collections`, `datetime`, `random`).

```bash
# 1. Create the sample data (200 fictional chat rows)
python3 generate_sample_data.py

# 2. Run the analyzer on it
python3 analyzer.py --file sample_chats.csv
```

## Example output

```
==================================================
WebChat Insights Report
==================================================
Total chats:            200
Avg response time:      295.2 seconds
Escalation rate:        14.0%
Resolution rate:        88.5%

Chats per agent:
  Priya        34
  Lucia        30
  David        27
  James        25
  Tom          25
  Aisha        23
  Carlos       20
  Maria        16

Most common issue categories:
  Billing Question         41
  Password Reset           35
  Claim Status             34
  Technical Issue          33
  General Inquiry          30
  Appointment Scheduling   27
==================================================
```

You can also point it at your own CSV, as long as it has these columns:
`timestamp, agent_name, customer_id, issue_category, response_time_seconds, escalated, resolved`

## What I learned

- Reading and parsing CSV files with Python's `csv` module (`DictReader`
  turns each row into a dictionary keyed by column name).
- Counting and grouping data with `collections.Counter`.
- Building a real command-line interface with `argparse` (the `--file` flag).
- Defensive coding: handling a missing file and bad number values instead of
  crashing.
- Keeping functions small and single-purpose (`load_chats`, `summarize`,
  `print_report`) so each piece is easy to test and explain.
