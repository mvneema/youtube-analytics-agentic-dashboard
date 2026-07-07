# Implementation Notes — YouTube Analytics Dashboard

## Goal
Build a channel analytics dashboard for "BI with Neema" (@mvneema) that
surfaces actionable content decisions, not just vanity metrics — using an
unknowns-first agentic workflow (the `fable-project` skill) rather than a
one-shot "build me a dashboard" prompt.

## Approved Plan Summary
Discovery interview → blind-spot pass → prototype with synthetic data →
approve layout → wire real data → verify against source totals → explainer +
comprehension quiz.

## Known Knowns
- Public YouTube Data API exposes per-video views/likes/comments/subscriber
  totals for any channel, no auth required.
- Real analytics (watch time, retention, CTR, traffic sources, demographics)
  require the YouTube Analytics API, which needs OAuth as the channel owner.

## Known Unknowns (surfaced during discovery)
- Whether to invest in OAuth/Google Cloud setup vs. manual CSV exports vs.
  public-data-only.
- Whether YouTube Studio's manual CSV export contains the same depth of data
  as the OAuth-gated API (it does).

## Unknown Knowns Surfaced
- The blind-spot pass flagged, before any building, that the public API alone
  would produce a dashboard missing the metrics that actually drive content
  decisions (retention, traffic source, CTR) — this reframed the whole
  requirements conversation before a single line of code was written.

## Unknown Unknowns Discovered
- The exported CSVs came as a 90-day window without an "Average percentage
  viewed" column — the ingest pipeline had to derive `avg % viewed` from
  `watch time ÷ views` and clearly label it as an approximation.
- Shorts detection needed to be duration-first, not title-pattern-based (a
  22-minute video with "#1" in the title was initially misclassified).
- Low-sample videos (<1,000 impressions) needed a ranking floor so a single
  lucky low-volume video couldn't outrank established, statistically
  reliable ones.

## Decisions Made

| Decision | Reason | Risk | Reversible? |
|---|---|---|---|
| CSV exports instead of OAuth | Same data depth, zero Google Cloud setup overhead | Manual refresh required | Yes — can add OAuth later without changing the report layer |
| Rank videos by retention (60%) + CTR (40%), not raw views | At this channel size, views mostly reflect exposure; retention/CTR reflect whether content and packaging are working | None | Yes — weights are a config value |
| Low-sample threshold at 1,000 impressions | Prevents noisy, statistically unreliable videos from topping the ranking | Threshold is a judgment call | Yes |

## Deviations

| Original plan | Deviation | Reason | Impact |
|---|---|---|---|
| Assumed engagement columns present in export | Derived avg % viewed from watch time ÷ views | Actual CSV export lacked the column | Numbers marked as approximate in the report until re-exported with the column included |

## Files Changed
- `analytics/ingest.py` — CSV loader and normalization
- `analytics/report.py` — HTML report renderer
- `docs/implementation-notes.md` — this file

## Verification
| Check | Result | Notes |
|---|---|---|
| Totals vs. export's own "Total" row | Match | 2,448 views, 34,058 impressions, 2.69% CTR over the export window |
| Light/dark mode render | Pass | Checked via headless screenshot |
| Colorblind-safe palette | Pass | Validated categorical palette for CVD separation and contrast |

## Open Questions
- Retention curves and traffic-source bars are absent until per-video exports
  are added (see `EXPORT-GUIDE.md`).
- Subscriber count is currently passed manually as a CLI flag rather than
  read from an export.

## Follow-ups
- Re-export top 3 videos with retention/traffic-source data included.
- Consider automating the CSV → report refresh on a schedule.
