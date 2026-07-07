#!/usr/bin/env python3
"""Render the BI with Neema channel analytics report as a standalone HTML file.

PORTFOLIO / PUBLIC VERSION
---------------------------
This script only ever runs against --sample data in this repo. Real exported
CSVs and the real ingest pipeline (ingest.py) are intentionally NOT included
here, since they contain private analytics (impressions, CTR, retention,
traffic sources) that aren't meant to be public. Video titles and public view
counts below are real and already public on the channel; every other number
(CTR, retention, watch time, impressions) is synthetic and clearly labeled as
such in the rendered report's banner.

Usage:
    python3 report.py --sample          # render with realistic fake data
    python3 report.py -o out.html --sample
"""
import argparse
import html
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
LOW_IMPRESSIONS = 1000  # below this, CTR/retention stats are flagged low-confidence

# ---------------------------------------------------------------------------
# Sample data — titles and public view counts are real; impressions, CTR,
# retention, and watch time are plausible synthetic values for demo purposes.
# ---------------------------------------------------------------------------

def build_sample_data():
    rng = random.Random(42)
    today = date(2026, 7, 5)

    relaunch = [
        ("I Built My Portfolio in Public During a Layoff - It Got Me 2 Job Offers", 4, 57, "long"),
        ("Why Your Power BI Numbers Don't Match (Filter Context vs Row Context Explained)", 11, 31, "long"),
        ("I quit my job and moved to Canada with no offer, here's what nobody tells you", 15, 378, "long"),
        ("Power BI vs Tableau 2026 - which one actually gets you hired in Canada?", 22, 104, "long"),
        ("I Failed a Live Power BI Interview. Then I Passed PL-300 in 6 Days. Here's Everything.", 32, 209, "long"),
    ]
    archive = [
        ("From Data Scientist to AI Product Manager | Career Transition, Skills & Lessons", 155, 112, "long"),
        ("I Took a Break… and Here's What It Taught Me (Data Diaries Comeback)", 185, 53, "long"),
        ("How to Succeed in Data Science: Career Tips, Layoffs & Future Trends", 400, 222, "long"),
        ("How to Kick Start your AI Career in 2025 ft. Ananya Gosh Chowdhury", 420, 113, "long"),
        ("How to land data job - highlight", 430, 45, "short"),
        ("How to Land a Data Analyst Job in 2025 | Your Step-by-Step Guide", 440, 50, "long"),
        ("How to be successful as an international student and a newcomer!", 460, 99, "long"),
        ("My 1st Anniversary in Canada — Top 3 life lessons", 480, 83, "short"),
        ("How to restart my job search in #canada #dataanalyst #career", 500, 89, "short"),
        ("How to transition into AI Industry successfully #ai #careeradvice", 510, 170, "short"),
        ("Gaining hands-on experience goes a long way! #data", 520, 18, "short"),
        ("How To Find Your Perfect Career ft. Clarisa #data", 540, 51, "short"),
        ("3 tips to get settled in Canada FASTER! #canada", 740, 69, "short"),
        ("How to Transition to Data Career 101 ft. Thais Cooke", 760, 123, "long"),
        ("From Non Tech to Tech Career - ft. Princilla Abena Koranteng", 790, 101, "long"),
        ("Canada PR application made simple (Watch Now)", 800, 47, "long"),
        ("Will these courses get you a job? (Must Watch) #datascience", 810, 141, "short"),
        ("Navigating PR: How I Received 3 Invitations to Apply in Canada!", 820, 1030, "long"),
        ("Settling In: My First Weeks as an Immigrant Abroad", 830, 266, "long"),
        ("The Truth About Data Scientist Salaries: India vs. USA (2023)", 900, 139, "long"),
        ("The 2 Portfolio Projects you ONLY need (Watch Now)", 920, 98, "long"),
        ("How to Make a Winning Resume (2023)", 940, 46, "long"),
    ]

    traffic_kinds = ["Suggested", "Search", "Browse", "External", "Channel pages", "Other"]

    def retention_curve(quality):
        pts, level = [], 1.0
        for i in range(41):
            x = i / 40
            if x < 0.05:
                level = 1.0 - (1.0 - quality * 0.85) * (x / 0.05) * 0.35
            else:
                level -= (0.012 + (1 - quality) * 0.014) * (1 + rng.uniform(-0.4, 0.4))
            level = max(level, 0.04)
            pts.append(round(level, 4))
        return pts

    def make_video(title, days_ago, views, vtype, era):
        pub = today - timedelta(days=days_ago)
        quality = rng.uniform(0.35, 0.75)
        ctr = round(rng.uniform(0.018, 0.062), 4)
        ext_share = rng.uniform(0.05, 0.45)
        impressions = int(views * (1 - ext_share) / ctr)
        avg_pct = round(quality * rng.uniform(0.55, 0.8), 3) if vtype == "long" else round(rng.uniform(0.55, 0.95), 3)
        dur = rng.randint(420, 780) if vtype == "long" else rng.randint(25, 58)
        avg_dur = int(dur * avg_pct)
        weights = [rng.random() ** 2 for _ in traffic_kinds]
        if ext_share > 0.3:
            weights[3] += 1.5
        total_w = sum(weights)
        traffic = {k: int(views * w / total_w) for k, w in zip(traffic_kinds, weights)}
        v = {
            "id": f"vid{rng.randint(10000, 99999)}",
            "title": title,
            "published": pub.isoformat(),
            "type": vtype,
            "era": era,
            "duration_s": dur,
            "views": views,
            "impressions": impressions,
            "ctr": ctr,
            "avg_pct_viewed": avg_pct,
            "avg_view_duration_s": avg_dur,
            "watch_hours": round(views * avg_dur / 3600, 1),
            "subs_gained": max(0, int(views * rng.uniform(0.004, 0.03))),
            "likes": int(views * rng.uniform(0.02, 0.08)),
            "comments": int(views * rng.uniform(0.002, 0.02)),
            "traffic": traffic,
        }
        if era == "relaunch" and vtype == "long":
            v["retention"] = retention_curve(quality)
        return v

    videos = [make_video(t, d, vw, ty, "relaunch") for t, d, vw, ty in relaunch]
    videos += [make_video(t, d, vw, ty, "archive") for t, d, vw, ty in archive]

    daily = []
    for i in range(90):
        d = today - timedelta(days=89 - i)
        base = 8 + (20 if i > 55 else 0)
        spike = 60 if i in (68, 75, 86) else 0
        daily.append({"date": d.isoformat(),
                      "views": int(base + spike + rng.uniform(0, 14)),
                      "watch_hours": round((base + spike) * rng.uniform(0.05, 0.12), 2),
                      "subs": rng.choice([0, 0, 0, 1, 1, 2])})

    return {
        "generated_at": datetime(2026, 7, 5, 19, 40).isoformat(),
        "data_through": (today - timedelta(days=3)).isoformat(),
        "sample": True,
        "channel": {"title": "BI with Neema", "handle": "@mvneema",
                    "subscribers": 388, "video_count": 158},
        "daily": daily,
        "videos": videos,
    }


def esc(s):
    return html.escape(str(s), quote=True)


def compact(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 10_000:
        return f"{n / 1000:.0f}K"
    if n >= 1_000:
        return f"{n / 1000:.1f}K"
    return f"{n:,}"


def pct(x, digits=1):
    return f"{x * 100:.{digits}f}%"


def render_body(data):
    """Minimal placeholder renderer for the portfolio repo.

    The full charting renderer (SVG retention curves, packaging-vs-content
    scatter, sortable tables, tooltips) lives in the private working copy of
    this project. This public version renders a simple summary table so the
    repo is runnable end-to-end without pulling in the entire dataviz layer.
    """
    ch = data["channel"]
    rows = ""
    for v in sorted(data["videos"], key=lambda x: -x["views"]):
        rows += (
            f"<tr><td>{esc(v['title'])}</td><td>{esc(v['published'])}</td>"
            f"<td style='text-align:right'>{v['views']:,}</td>"
            f"<td style='text-align:right'>{pct(v['ctr'])}</td>"
            f"<td style='text-align:right'>{pct(v['avg_pct_viewed'], 0)}</td></tr>"
        )
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>{esc(ch['title'])} — sample report</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:900px;margin:32px auto;padding:0 16px}}
.banner{{background:#fdf3dd;color:#7a5800;border-radius:8px;padding:10px 14px;font-size:13px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{padding:8px 10px;border-bottom:1px solid #e1e0d9;text-align:left}}
th{{font-size:12px;color:#666}}
</style></head><body>
<h1>{esc(ch['title'])} ({esc(ch['handle'])})</h1>
<div class="banner">Sample data — titles and view counts are real public data;
CTR, retention, and impressions are synthetic, for demonstration only.</div>
<table><thead><tr><th>Title</th><th>Published</th><th>Views</th><th>CTR</th><th>Avg % viewed</th></tr></thead>
<tbody>{rows}</tbody></table>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true", help="render with simulated data")
    ap.add_argument("-o", "--out", type=Path, default=HERE / "report_sample.html")
    args = ap.parse_args()

    data = build_sample_data()
    args.out.write_text(render_body(data))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
