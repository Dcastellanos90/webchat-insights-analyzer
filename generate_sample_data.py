"""Generate a realistic sample CSV of WebChat support interactions.

The data is completely fictional -- it exists so the analyzer has
something to chew on without touching any real company data.

Run:  python3 generate_sample_data.py
Makes: sample_chats.csv (200 rows)
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # same "random" data every run, so results are reproducible

AGENTS = ["Maria", "James", "Priya", "Carlos", "Aisha", "Tom", "Lucia", "David"]
CATEGORIES = [
    "Billing Question",
    "Password Reset",
    "Appointment Scheduling",
    "Claim Status",
    "Technical Issue",
    "General Inquiry",
]

OUTPUT_FILE = "sample_chats.csv"
NUM_ROWS = 200


def random_timestamp():
    """Return a random moment within the last 30 days, as a string."""
    days_ago = random.randint(0, 29)
    seconds = random.randint(0, 86399)
    moment = datetime.now() - timedelta(days=days_ago, seconds=seconds)
    return moment.strftime("%Y-%m-%d %H:%M:%S")


def main():
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "agent_name", "customer_id", "issue_category",
            "response_time_seconds", "escalated", "resolved",
        ])
        for _ in range(NUM_ROWS):
            escalated = random.random() < 0.15      # ~15% of chats get escalated
            resolved = random.random() < 0.90       # ~90% get resolved
            if escalated:
                resolved = random.random() < 0.70   # escalated chats resolve less often
            writer.writerow([
                random_timestamp(),
                random.choice(AGENTS),
                f"CUST-{random.randint(1000, 9999)}",
                random.choice(CATEGORIES),
                random.randint(20, 600),            # response time in seconds
                "yes" if escalated else "no",
                "yes" if resolved else "no",
            ])
    print(f"Wrote {NUM_ROWS} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
