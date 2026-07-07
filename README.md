# Agentic YouTube Analytics Dashboard

An unknowns-first agentic workflow — built with [Claude Code](https://claude.com/claude-code)
and a custom skill (`fable-project`) — that interviews itself before building,
runs a deliberate blind-spot pass, and self-verifies its output against
ground truth, applied here to a real YouTube channel analytics dashboard.

> **Note:** this repo is a portfolio artifact demonstrating the *process*.
> Real exported analytics CSVs and the private ingest pipeline are
> intentionally excluded (see `.gitignore`) — only synthetic sample data and
> already-public video titles/view counts are included here.

## The problem this solves

Most "AI, build me a dashboard" prompts skip straight to output — and
confidently build the wrong thing when the underlying assumptions are wrong.
This project instead runs a structured, unknowns-first process:

1. **Discovery interview** — one question at a time, not a form dump
2. **Blind-spot pass** — surface constraints and unknowns before proposing
   anything
3. **Prototype with synthetic data** — get layout approval before touching
   real data
4. **Implement with a visible decision log** — see `docs/implementation-notes.md`
5. **Explain + quiz** — a post-build comprehension check before trusting the
   output

## A concrete example of it working

Before writing any code, the blind-spot pass caught that the public YouTube
Data API only exposes views/likes/comments — the metrics that actually drive
content decisions (retention, CTR, traffic sources) require either OAuth
access or a manual CSV export. That fork was surfaced and decided *before*
implementation, not discovered as a bug afterward.

Once wired to real (exported) data, the report surfaced a genuinely
actionable, non-obvious finding: the channel's technical/BI content was
already being surfaced by YouTube's algorithm at a high impression count, but
converting at a much lower CTR than personal-story content — meaning the
fix isn't "post different topics," it's "repackage the titles/thumbnails on
the technical videos already getting reach." See `docs/implementation-notes.md`
for the full decision log.

## Repo structure

```
.claude/skills/fable-project/   the actual skill: discovery → blind-spot →
                                 plan → implement → explain+quiz phases
analytics/report.py             sample-data report renderer (runnable, no
                                 credentials or private data needed)
analytics/sample-data/          pre-rendered sample output
docs/implementation-notes.md    the real decision log, deviations, verification
docs/screenshots/               discovery interview + dashboard screenshots
```

## Run it yourself

```bash
python3 analytics/report.py --sample
```

Opens/writes `analytics/report_sample.html` — a self-contained, dependency-free
HTML file using synthetic metrics and real public video titles.

## Use the skill yourself

```bash
mkdir -p .claude/skills
cp -R .claude/skills/fable-project ~/your-project/.claude/skills/fable-project
```

Then in Claude Code: `/fable-project <your rough idea>` — see
`.claude/skills/fable-project/README.md` for full install notes.

## Tech stack

- [Claude Code](https://claude.com/claude-code) + Claude Fable 5
- Python (standard library only — no pandas/numpy dependency for the renderer)
- Inline SVG for charts, vanilla JS for tooltips/sorting (no frontend framework)
- YouTube Studio CSV exports as the data source (no OAuth/Google Cloud required)

## License

MIT — see `LICENSE`.
