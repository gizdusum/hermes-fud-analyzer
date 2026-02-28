
```
   ╔═╗╦ ╦╔╦╗
   ╠╣ ║ ║ ║║
   ╚  ╚═╝═╩╝
   ╔═╗╔╗╔╔═╗╦  ╦ ╦╔═╗╔═╗╦═╗
   ╠═╣║║║╠═╣║  ╚╦╝╔═╝║╣ ╠╦╝
   ╩ ╩╝╚╝╩ ╩╩═╝ ╩ ╚═╝╚═╝╩╚═
```

<div align="center">

# 🕵️ FUD Analyzer

### *How much does someone FUD crypto projects on Twitter/X?*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Nous Research](https://img.shields.io/badge/Nous-Research-ff6b35?style=for-the-badge)](https://nousresearch.com)

---

*Feed it a Twitter handle, it finds their posts, runs keyword sentiment analysis, and tells you if they're a FUD spreader or a shill. Simple as that.*

</div>

---

## 🤔 What Is FUD?

**FUD** = Fear, Uncertainty, Doubt. It's when someone spreads negativity about crypto projects — calling things scams, predicting crashes, screaming "rug pull" at everything.

This tool measures exactly how much someone does that.

---

## ⚡ Quick Start

```bash
# No install needed — just run it
python fud_analyzer.py elonmusk
```

Output:
```
🔍 Analyzing @elonmusk for FUD...

  Username:        @elonmusk
  Tweets analyzed: 24
  FUD Score:       23.5%
  Shill Score:     76.5%
  Verdict:         😐 MILD FUD — occasional negativity, mostly chill

  📛 Most FUD-like snippets:
    [6pts] "this project is dead, sold everything..."
```

---

## 🎯 How It Works

1. **Scrapes** recent posts via DuckDuckGo web search (no API key needed)
2. **Scores** each post against two keyword banks:
   - 🔴 **FUD keywords** — scam, rug, dump, dead, worthless, hack... (40+ terms)
   - 🟢 **Shill keywords** — moon, bullish, gem, 100x, wagmi, LFG... (25+ terms)
3. **Calculates** FUD vs Shill percentage
4. **Returns** a verdict with the spiciest tweets

---

## 📊 Verdict Scale

| Score | Label |
|-------|-------|
| 80%+  | 🚨 MAXIMUM FUD SPREADER — certified chaos agent |
| 60-80% | 😈 HEAVY FUDDER — really hates crypto projects |
| 40-60% | 🌧️ MODERATE FUDDER — skeptical but not unhinged |
| 20-40% | 😐 MILD FUD — occasional negativity, mostly chill |
| 10-20% | 😇 LOW FUD — pretty balanced actually |
| 0-10% | 🤝 NO FUD — either a shill or just vibing |

---

## 🔧 As a Hermes Agent Tool

```bash
hermes-agent --mcp fud=fud-analyzer
```

Then just ask:
```
You: "How much does @cryptoskeptic FUD projects?"
Hermes: 😈 @cryptoskeptic has a FUD score of 72.3%...
```

---

## 🛠️ Zero Dependencies

Pure Python stdlib. No pip install. No API keys. No signup. Just works.

---

## 👤 Author

**Deniz Alagoz**

[![GitHub](https://img.shields.io/badge/@gizdusum-181717?style=flat-square&logo=github)](https://github.com/gizdusum)
[![Discord](https://img.shields.io/badge/gizdusum-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.com)
[![X/Twitter](https://img.shields.io/badge/@gizdusumandnode-000000?style=flat-square&logo=x)](https://x.com/gizdusumandnode)

---

<div align="center">

*stop the fud. or at least measure it.* 🕵️

</div>
