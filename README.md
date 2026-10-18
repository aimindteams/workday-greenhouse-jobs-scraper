# Workday, Greenhouse & Lever Jobs Scraper (Python)

Pull every open job straight from company career sites, in one consistent format: **Greenhouse, Lever, Ashby, Workday, Workable, SmartRecruiters, Recruitee, Personio and BambooHR**. Give it careers page URLs, company websites or just company names; it finds the job board, applies your filters and returns title, department, location, remote status, salary (when published) and the apply link.

This repo is a small, free Python client for the [Career Site Jobs Scraper](https://apify.com/aimindteams/career-site-jobs-scraper) on Apify. The Actor reads each company's official job board API in the cloud; this script runs it on your list and saves a CSV.

## Why career sites instead of LinkedIn or Indeed?

- **Complete and current:** the company's own board is the source every job site copies from, so nothing is missing or stale
- **No login, no blocking:** these are the public job board APIs the career pages themselves use
- **Structured salary and remote data** where the company publishes it
- **One schema for nine hiring systems**, so you can compare companies side by side

## Quick start (no code)

Open the [Actor on the Apify Store](https://apify.com/aimindteams/career-site-jobs-scraper), list your companies and press **Start**. Download the results as CSV, Excel or JSON.

## Quick start (Python)

```bash
git clone https://github.com/aimindteams/workday-greenhouse-jobs-scraper
cd workday-greenhouse-jobs-scraper
pip install -r requirements.txt
export APIFY_TOKEN=your_token   # free account: https://console.apify.com/settings/integrations

# Engineering jobs at three companies, by URL, website and name
python track_jobs.py "https://boards.greenhouse.io/stripe" palantir.com Ramp --keywords engineer --csv jobs.csv

# Remote data jobs posted this week across a list of companies
python track_jobs.py --file companies.example.txt --keywords data analyst scientist --remote-only --days 7

# Daily tracking: only jobs you have not seen in earlier runs
python track_jobs.py --file companies.example.txt --only-new
```

On Windows PowerShell use `$env:APIFY_TOKEN="your_token"`.

## What the CSV looks like

Illustrative example (invented company):

| company | ats | title | department | location | workplace_type | posted_at | salary |
|---|---|---|---|---|---|---|---|
| Acme Robotics | Greenhouse | Senior Software Engineer, Perception | Engineering | Boston, MA | hybrid | 2026-10-14 | $160K - $210K |
| Acme Robotics | Greenhouse | Data Analyst | Operations | Remote (US) | remote | 2026-10-12 | |

## Use cases

- **Job seekers:** watch your target companies and see new roles the day they are posted
- **Sales and recruiting teams:** hiring is a buying signal; track which companies are growing which teams
- **Job boards and newsletters:** fill a niche board from the source instead of copying other boards
- **Market research:** compare headcount growth, remote share and salary bands across competitors

## Use it from AI agents (MCP)

```
https://mcp.apify.com?tools=aimindteams/career-site-jobs-scraper
```

## Pricing

Pay per job delivered; filters lower the cost because filtered-out jobs are free. With `--only-new` you never pay twice for the same job. Current prices are on the [Pricing tab](https://apify.com/aimindteams/career-site-jobs-scraper/pricing). `--max-cost` (default $1) caps any single run.

## FAQ

**Which URLs work?** boards.greenhouse.io/acme, jobs.lever.co/acme, jobs.ashbyhq.com/acme, acme.wd5.myworkdayjobs.com/External, apply.workable.com/acme, jobs.smartrecruiters.com/Acme, acme.recruitee.com, acme.jobs.personio.de and acme.bamboohr.com/careers, plus shorthands like `greenhouse:acme`.

**What if I only know the company name?** The Actor checks the company's website and the major hiring systems and reports which board it matched, so you can confirm it.

## License

The code in this repo is MIT licensed. The Actor itself is a hosted service on Apify.
