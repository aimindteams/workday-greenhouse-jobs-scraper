"""Pull open jobs straight from company career sites (Greenhouse, Lever, Ashby, Workday and more).

Runs the "Career Site Jobs Scraper" Actor on Apify and saves one CSV row per job.

    export APIFY_TOKEN=...   # free account: https://console.apify.com/settings/integrations
    python track_jobs.py stripe.com "https://jobs.lever.co/palantir" Ramp --keywords engineer --csv jobs.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path

from apify_client import ApifyClient

ACTOR_ID = "aimindteams/career-site-jobs-scraper"

COLUMNS = [
    "company", "ats", "title", "department", "team", "location", "workplace_type", "is_remote",
    "employment_type", "posted_at", "salary", "job_url", "apply_url",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scrape open jobs from company career sites.")
    p.add_argument("companies", nargs="*", help="Careers URLs, company websites or company names")
    p.add_argument("--file", help="Text file with one company per line")
    p.add_argument("--keywords", nargs="*", default=[], help="Keep jobs whose title contains any of these")
    p.add_argument("--locations", nargs="*", default=[], help="Keep jobs whose location contains any of these")
    p.add_argument("--departments", nargs="*", default=[], help="Keep jobs in these departments or teams")
    p.add_argument("--remote-only", action="store_true", help="Fully remote jobs only")
    p.add_argument("--days", type=int, default=0, help="Posted in the last N days (0 = all open jobs)")
    p.add_argument("--max-per-company", type=int, default=100, help="Jobs per company after filters (default 100)")
    p.add_argument("--descriptions", action="store_true", help="Include full job descriptions (bigger output)")
    p.add_argument("--only-new", action="store_true", help="Only jobs not returned by your earlier runs")
    p.add_argument("--csv", default="jobs.csv", help="CSV output path (default jobs.csv)")
    p.add_argument("--json", help="Also save the full results as JSON")
    p.add_argument("--max-cost", type=float, default=1.0, help="Stop the run before it costs more than this (USD)")
    return p.parse_args()


def row(job: dict) -> dict:
    salary = job.get("salary") or {}
    return {
        "company": job.get("company"),
        "ats": job.get("ats"),
        "title": job.get("title"),
        "department": job.get("department"),
        "team": job.get("team"),
        "location": job.get("location"),
        "workplace_type": job.get("workplace_type"),
        "is_remote": job.get("is_remote"),
        "employment_type": job.get("employment_type"),
        "posted_at": (job.get("posted_at") or "")[:10],
        "salary": salary.get("text"),
        "job_url": job.get("job_url"),
        "apply_url": job.get("apply_url"),
    }


def main() -> int:
    args = parse_args()
    companies = list(args.companies)
    if args.file:
        companies += [line.strip() for line in Path(args.file).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not companies:
        sys.exit("Name at least one company, for example: python track_jobs.py stripe.com")
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first. Get one free at https://console.apify.com/settings/integrations")

    run_input = {
        "companies": companies,
        "keywords": args.keywords,
        "locations": args.locations,
        "departments": args.departments,
        "remoteOnly": args.remote_only,
        "postedWithinDays": args.days,
        "maxJobsPerCompany": args.max_per_company,
        "includeDescription": args.descriptions,
        "onlyNewJobs": args.only_new,
    }
    client = ApifyClient(token)
    print(f"Checking {len(companies)} career sites with {ACTOR_ID} ...")
    run = client.actor(ACTOR_ID).call(run_input=run_input, max_total_charge_usd=args.max_cost)
    if not run or run.get("status") != "SUCCEEDED":
        sys.exit(f"Run did not finish: {run and run.get('status')}")

    jobs = [i for i in client.dataset(run["defaultDatasetId"]).iterate_items(clean=True) if i.get("job_id")]
    jobs.sort(key=lambda j: j.get("posted_at") or "", reverse=True)
    with open(args.csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(row(j) for j in jobs)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(jobs, handle, indent=2)

    print(f"Saved {len(jobs)} jobs to {args.csv}")
    for company, count in Counter(j.get("company") for j in jobs).most_common():
        print(f"  {count:>5}  {company}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
