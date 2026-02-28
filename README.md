# hermes-fud-analyzer

A Hermes Agent skill that measures how much a Twitter/X account FUDs crypto projects.

Feed it a handle, get a FUD score. Simple as that.

> "How much does @cryptoskeptic FUD projects?"
> Hermes: @cryptoskeptic has a FUD score of 72.3% — HEAVY FUDDER

---

## Install

This is a Hermes Agent hub skill. Install it with:

    hermes skills install https://github.com/gizdusum/hermes-fud-analyzer

Then ask Hermes:

    How much does @elonmusk FUD crypto?

---

## What It Does

Measures what percentage of someone's Twitter/X activity is FUD
(Fear, Uncertainty, Doubt) toward crypto projects vs shilling.

- Scrapes DuckDuckGo / Google / Bing for recent public posts from the handle
- Scores snippets against two weighted keyword banks:
  - FUD: scam, rug, dump, dead, worthless, hack... (40+ terms)
  - Shill: moon, bullish, gem, 100x, wagmi... (25+ terms)
- Returns a FUD % score and a verdict label

## Verdict Scale

  Score   | Label
  --------|----------------------------------------------
  80%+    | MAXIMUM FUD SPREADER — certified chaos agent
  60-80%  | HEAVY FUDDER — really hates crypto projects
  40-60%  | MODERATE FUDDER — skeptical but not unhinged
  20-40%  | MILD FUD — occasional negativity, mostly chill
  10-20%  | LOW FUD — pretty balanced actually
  0-10%   | NO FUD DETECTED — either a shill or just vibing

## Zero Dependencies

Pure Python stdlib. No pip install. No API keys. No signup.

    python3 scripts/fud_analyzer.py elonmusk

## Skill Structure

    hermes-fud-analyzer/
    ├── SKILL.md              # Hermes skill definition
    ├── scripts/
    │   └── fud_analyzer.py   # Core analyzer (pure Python stdlib)
    └── README.md

---

FOR ENTERTAINMENT ONLY. Not financial advice. Not even real advice. Just vibes.
