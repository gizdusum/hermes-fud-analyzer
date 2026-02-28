---
name: fud-analyzer
description: Measure how much a Twitter/X account FUDs crypto projects. Feed it a handle, get a FUD percentage score with verdict. Zero dependencies — pure Python stdlib.
version: 1.1.0
author: Deniz Alagoz
license: MIT
metadata:
  hermes:
    tags: [Crypto, Twitter, Sentiment, Social, Analysis]
    related_skills: []
---

# FUD Analyzer

Measures what percentage of a Twitter/X account's public activity is FUD
(Fear, Uncertainty, Doubt) vs shilling toward crypto projects.

Scrapes search engine snippets — no Twitter API key, no pip install, no signup.

## When to Use

Load this skill when the user asks things like:
- "How much does @handle FUD crypto?"
- "Is @handle a FUDder?"
- "Analyze crypto sentiment for @someone on Twitter"
- "Check if this person is bullish or bearish on crypto"

## Quick Reference

  Run from terminal:
    python3 scripts/fud_analyzer.py elonmusk

  Use as a Python module:
    from scripts.fud_analyzer import analyze_fud
    result = analyze_fud("elonmusk")
    print(result["verdict"])

## Procedure

1. Locate the script:
   The script is at: <skill_dir>/scripts/fud_analyzer.py

   If the skill was installed via `hermes skills install`, the path will be
   something like: ~/.hermes/skills/crypto/fud-analyzer/scripts/fud_analyzer.py

2. Run it via terminal tool:

     python3 ~/.hermes/skills/crypto/fud-analyzer/scripts/fud_analyzer.py <handle>

   Or use execute_code to call analyze_fud() programmatically:

     import sys
     sys.path.insert(0, "/path/to/skill/scripts")
     from fud_analyzer import analyze_fud
     result = analyze_fud("handle")

3. Parse and present the result. Key fields:

   - username        -> @handle
   - posts_analyzed  -> how many snippets were found
   - fud_score       -> FUD percentage (0-100)
   - shill_score     -> shill percentage (0-100)
   - verdict         -> human-readable label
   - top_fud_evidence -> list of snippets that scored FUD points
   - top_shill_evidence -> list of snippets that scored shill points
   - error           -> present only if no posts found

4. Present to the user:
   Show username, fud_score%, shill_score%, verdict.
   Optionally show top_fud_evidence snippets for transparency.

## Verdict Scale

  Score   | Label
  --------|---------------------------------------------------
  80%+    | MAXIMUM FUD SPREADER
  60-80%  | HEAVY FUDDER
  40-60%  | MODERATE FUDDER
  20-40%  | MILD FUD
  10-20%  | LOW FUD
  0-10%   | NO FUD DETECTED

## Pitfalls

- Account must be public and indexed by search engines.
- Results depend on what search engines surface, not the actual Twitter timeline.
- Very new or small accounts may return no results — try again or inform the user.
- Search engines sometimes rate-limit. If "Could not find posts" is returned,
  wait a minute and retry.
- The tool scrapes DuckDuckGo first, falls back to Google then Bing.
  If all three fail, return the error message from the result dict.

## Verification

After running, confirm:
- posts_analyzed > 0
- fud_score + shill_score = 100 (or both = 0 if no keywords matched)
- verdict string is populated
