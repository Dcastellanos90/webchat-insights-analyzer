"""WebChat Insights Analyzer.

Reads a CSV of customer chat interactions and prints summary analytics:
total chats, average response time, escalation rate, resolution rate,
chats per agent, and the most common issue categories.

Expected CSV columns:
    timestamp, agent_name, customer_id, issue_category,
    response_time_seconds, escalated, resolved

Usage:
    python3 analyzer.py --file sample_chats.csv
"""

import argparse
import csv
import sys
from collections import Counter


def load_chats(path):
    """Read the CSV and return a list of dicts, one per chat.

    Numbers are converted to floats and the yes/no columns to booleans
    so the math below stays simple.
    """
    chats = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["response_time_seconds"] = float(row["response_time_seconds"])
            except (ValueError, KeyError):
                row["response_time_seconds"] = 0.0
            row["escalated"] = row.get("escalated", "").strip().lower() == "yes"
            row["resolved"] = row.get("resolved", "").strip().lower() == "yes"
            chats.append(row)
    return chats


def summarize(chats):
    """Compute the headline numbers. Returns a dict of results."""
    total = len(chats)
    if total == 0:
        return None

    avg_response = sum(c["response_time_seconds"] for c in chats) / total
    escalated = sum(1 for c in chats if c["escalated"])
    resolved = sum(1 for c in chats if c["resolved"])

    # Counter is a dict subclass that counts how often each value appears.
    per_agent = Counter(c["agent_name"] for c in chats)
    per_category = Counter(c["issue_category"] for c in chats)

    return {
        "total": total,
        "avg_response": avg_response,
        "escalation_rate": escalated / total * 100,
        "resolution_rate": resolved / total * 100,
        "per_agent": per_agent,
        "per_category": per_category,
    }


def print_report(summary):
    """Print the results as a readable plain-text report."""
    print("=" * 50)
    print("WebChat Insights Report")
    print("=" * 50)
    print(f"Total chats:            {summary['total']}")
    print(f"Avg response time:      {summary['avg_response']:.1f} seconds")
    print(f"Escalation rate:        {summary['escalation_rate']:.1f}%")
    print(f"Resolution rate:        {summary['resolution_rate']:.1f}%")
    print()
    print("Chats per agent:")
    for agent, count in summary["per_agent"].most_common():
        print(f"  {agent:<12} {count}")
    print()
    print("Most common issue categories:")
    for category, count in summary["per_category"].most_common():
        print(f"  {category:<24} {count}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze WebChat support chat data from a CSV file."
    )
    parser.add_argument("--file", required=True, help="Path to the chats CSV file")
    args = parser.parse_args()

    try:
        chats = load_chats(args.file)
    except FileNotFoundError:
        print(f"Error: could not find file '{args.file}'", file=sys.stderr)
        sys.exit(1)

    if not chats:
        print("No chat rows found in the file.")
        sys.exit(0)

    print_report(summarize(chats))


if __name__ == "__main__":
    main()
