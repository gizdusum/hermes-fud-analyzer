#!/usr/bin/env python3
"""
FUD Analyzer — How much does someone FUD crypto projects on Twitter/X?

Feed it a Twitter handle, it scrapes recent posts via multiple search
engines, runs keyword sentiment analysis, and returns a FUD score.

Zero external dependencies — pure Python stdlib.
"""

import json
import re
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, List, Any

# ---------------------------------------------------------------------------
# FUD / SHILL keyword banks (weighted)
# ---------------------------------------------------------------------------

FUD_KEYWORDS = {
    # hard fud (weight 3)
    "scam": 3, "rug": 3, "rugpull": 3, "rug pull": 3, "ponzi": 3, "fraud": 3,
    "worthless": 3, "exit scam": 3, "cashgrab": 3, "cash grab": 3, "vaporware": 3,
    # medium fud (weight 2)
    "dead": 2, "dying": 2, "dump": 2, "dumping": 2, "crashed": 2, "crashing": 2,
    "collapse": 2, "garbage": 2, "trash": 2, "overvalued": 2, "bubble": 2,
    "hack": 2, "hacked": 2, "exploit": 2, "vulnerability": 2, "insecure": 2,
    "fake": 2, "lying": 2, "misleading": 2, "manipulate": 2,
    "shady": 2, "sketchy": 2, "red flag": 2, "red flags": 2,
    "don't buy": 2, "dont buy": 2, "stay away": 2, "not safe": 2,
    "no product": 2, "empty promises": 2,
    # soft fud (weight 1)
    "bearish": 1, "sell": 1, "selling": 1, "avoid": 1, "warning": 1,
    "careful": 1, "risk": 1, "risky": 1, "concern": 1, "worried": 1,
    "doubt": 1, "skeptical": 1, "suspicious": 1, "rip": 1, "exit": 1,
}

SHILL_KEYWORDS = {
    "bullish": 1, "moon": 1, "mooning": 1, "gem": 1, "alpha": 1,
    "buy": 1, "buying": 1, "hold": 1, "hodl": 1, "accumulate": 1,
    "undervalued": 1, "100x": 2, "1000x": 2, "10x": 1,
    "lfg": 1, "wagmi": 1, "based": 1, "chad": 1,
    "love": 1, "amazing": 1, "incredible": 1, "best": 1,
    "bullrun": 1, "bull run": 1, "pump": 1, "pumping": 1,
    "🚀": 1, "🔥": 1, "💎": 1,
}

# ---------------------------------------------------------------------------
# Multi-engine web search (no API key)
# ---------------------------------------------------------------------------

def _fetch(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _search_via_ddg_lite(query: str) -> List[str]:
    """DuckDuckGo Lite — less likely to captcha."""
    try:
        url = "https://lite.duckduckgo.com/lite/?" + urllib.parse.urlencode({"q": query})
        html = _fetch(url)
        # Lite version uses <td> cells for snippets
        cells = re.findall(r'<td[^>]*class="result-snippet"[^>]*>(.*?)</td>', html, re.DOTALL)
        if not cells:
            # fallback: grab all td content that looks like text
            cells = re.findall(r'<td[^>]*>\s*<a[^>]*class="result-link"[^>]*>.*?</a>\s*</td>\s*<td[^>]*>(.*?)</td>', html, re.DOTALL)
        results = []
        for c in cells:
            clean = re.sub(r'<[^>]+>', '', c).strip()
            if clean and len(clean) > 15:
                results.append(clean)
        return results
    except Exception:
        return []


def _is_junk(text: str) -> bool:
    """Filter out HTML artifacts, nav elements, and irrelevant content."""
    junk_signals = [
        "SearchImagesVideos", "javascript", "function(", "window.", "document.",
        "cookie", "privacy policy", "terms of service", "sign up", "log in",
        "©", "Copyright", ".onclick", ".href", "classList", "querySelector",
        "MoreShoppingFlights", "var ", "const ", "hostname", "createElement",
    ]
    text_lower = text.lower()
    for signal in junk_signals:
        if signal.lower() in text_lower:
            return True
    # too short or too long (likely page chrome)
    if len(text) < 30 or len(text) > 500:
        return True
    # mostly non-alpha (likely code/URLs)
    alpha_ratio = sum(c.isalpha() or c.isspace() for c in text) / max(len(text), 1)
    if alpha_ratio < 0.6:
        return True
    return False


def _search_via_google_scrape(query: str) -> List[str]:
    """Google search scraping as fallback."""
    try:
        url = "https://www.google.com/search?" + urllib.parse.urlencode({"q": query, "num": 20})
        html = _fetch(url)
        spans = re.findall(r'<span[^>]*>(.*?)</span>', html)
        results = []
        for s in spans:
            clean = re.sub(r'<[^>]+>', '', s).strip()
            if len(clean) > 40 and not _is_junk(clean):
                results.append(clean)
        return results[:15]
    except Exception:
        return []


def _search_via_bing(query: str) -> List[str]:
    """Bing search as second fallback."""
    try:
        url = "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query})
        html = _fetch(url)
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        results = []
        for p in paragraphs:
            clean = re.sub(r'<[^>]+>', '', p).strip()
            if len(clean) > 30 and not _is_junk(clean):
                results.append(clean)
        return results[:15]
    except Exception:
        return []


def _search_tweets(username: str) -> List[str]:
    """Aggregate tweet-like snippets from multiple search engines."""
    queries = [
        f'"{username}" twitter crypto',
        f'"{username}" x.com crypto opinion',
        f'site:x.com/{username}',
        f'site:twitter.com/{username}',
        f'"{username}" crypto project',
    ]
    
    all_texts = []
    seen = set()
    
    for q in queries:
        for search_fn in [_search_via_ddg_lite, _search_via_google_scrape, _search_via_bing]:
            results = search_fn(q)
            for text in results:
                text_key = text[:50].lower()
                if text_key not in seen:
                    seen.add(text_key)
                    all_texts.append(text)
            if len(all_texts) >= 20:
                break
        if len(all_texts) >= 30:
            break
    
    return all_texts[:40]


# ---------------------------------------------------------------------------
# Analysis engine
# ---------------------------------------------------------------------------

def _score_text(text: str, keyword_bank: dict) -> float:
    text_lower = text.lower()
    score = 0.0
    for keyword, weight in keyword_bank.items():
        count = text_lower.count(keyword)
        score += count * weight
    return score


def _get_fud_label(score: float) -> str:
    if score >= 80:
        return "🚨 MAXIMUM FUD SPREADER — certified chaos agent"
    elif score >= 60:
        return "😈 HEAVY FUDDER — this person really hates crypto projects"
    elif score >= 40:
        return "🌧️ MODERATE FUDDER — skeptical but not unhinged"
    elif score >= 20:
        return "😐 MILD FUD — occasional negativity, mostly chill"
    elif score >= 10:
        return "😇 LOW FUD — pretty balanced actually"
    else:
        return "🤝 NO FUD DETECTED — either a shill or just vibing"


def analyze_fud(username: str) -> Dict[str, Any]:
    """
    Analyze a Twitter/X user's FUD level.
    
    Args:
        username: Twitter/X handle (without @)
    
    Returns:
        Dict with fud_score, shill_score, verdict, sample texts, etc.
    """
    username = username.strip().lstrip("@")
    
    texts = _search_tweets(username)
    
    if not texts:
        return {
            "username": f"@{username}",
            "error": "Could not find posts. Account may be private, or search engines blocked the request.",
            "tweets_found": 0,
            "tip": "Try running again, or check if the username is correct."
        }
    
    total_fud = 0.0
    total_shill = 0.0
    fud_tweets = []
    shill_tweets = []
    neutral_count = 0
    
    for text in texts:
        fud_s = _score_text(text, FUD_KEYWORDS)
        shill_s = _score_text(text, SHILL_KEYWORDS)
        total_fud += fud_s
        total_shill += shill_s
        
        if fud_s > 0:
            fud_tweets.append({"text": text[:200], "fud_points": round(fud_s, 1)})
        elif shill_s > 0:
            shill_tweets.append({"text": text[:200], "shill_points": round(shill_s, 1)})
        else:
            neutral_count += 1
    
    total = total_fud + total_shill
    if total > 0:
        fud_pct = round((total_fud / total) * 100, 1)
        shill_pct = round((total_shill / total) * 100, 1)
    else:
        fud_pct = 0.0
        shill_pct = 0.0
    
    fud_tweets.sort(key=lambda x: x["fud_points"], reverse=True)
    shill_tweets.sort(key=lambda x: x["shill_points"], reverse=True)
    
    return {
        "username": f"@{username}",
        "posts_analyzed": len(texts),
        "fud_score": fud_pct,
        "shill_score": shill_pct,
        "neutral_posts": neutral_count,
        "verdict": _get_fud_label(fud_pct),
        "raw_fud_points": round(total_fud, 1),
        "raw_shill_points": round(total_shill, 1),
        "top_fud_evidence": fud_tweets[:5],
        "top_shill_evidence": shill_tweets[:3],
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fud_analyzer.py <twitter_username>")
        print("Example: python fud_analyzer.py elonmusk")
        sys.exit(1)
    
    handle = sys.argv[1].lstrip("@")
    print(f"\n🔍 Analyzing @{handle} for FUD...\n")
    
    result = analyze_fud(handle)
    
    if "error" in result:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    print(f"  👤 Username:        {result['username']}")
    print(f"  📝 Posts analyzed:  {result['posts_analyzed']}")
    print(f"  🔴 FUD Score:       {result['fud_score']}%")
    print(f"  🟢 Shill Score:     {result['shill_score']}%")
    print(f"  ⚖️  Neutral:        {result['neutral_posts']} posts")
    print(f"  🏷️  Verdict:        {result['verdict']}")
    print()
    
    if result['top_fud_evidence']:
        print("  📛 Most FUD-like snippets found:")
        for i, t in enumerate(result['top_fud_evidence'][:3], 1):
            print(f"    {i}. [{t['fud_points']}pts] \"{t['text'][:120]}\"")
        print()
    
    if result['top_shill_evidence']:
        print("  💚 Most shill-like snippets found:")
        for i, t in enumerate(result['top_shill_evidence'][:2], 1):
            print(f"    {i}. [{t['shill_points']}pts] \"{t['text'][:120]}\"")
        print()
    
    print("--- Full JSON ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
