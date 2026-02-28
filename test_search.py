import urllib.request, urllib.parse, re

q = 'site:x.com/elonmusk crypto'
url = 'https://html.duckduckgo.com/html/?' + urllib.parse.urlencode({'q': q})
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='replace')
print('HTML length:', len(html))

snippets = re.findall(r'class="result__snippet">(.*?)</a>', html, re.DOTALL)
print('Snippets found:', len(snippets))
for s in snippets[:3]:
    clean = re.sub(r'<[^>]+>', '', s).strip()
    print('  -', clean[:150])

snippets2 = re.findall(r'result__snippet[^>]*>(.*?)<', html, re.DOTALL)
print('Alt snippets:', len(snippets2))

body = re.findall(r'result__body[^>]*>(.*?)</a', html, re.DOTALL)
print('Body results:', len(body))

titles = re.findall(r'result__a[^>]*>(.*?)</a', html, re.DOTALL)
print('Titles:', len(titles))
for t in titles[:5]:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    print('  title:', clean[:150])

# save html for debug
with open('/tmp/ddg_debug.html', 'w') as f:
    f.write(html)
print('Saved to /tmp/ddg_debug.html')
