#!/usr/bin/env python3
"""
Bundle the four page site into one self-contained HTML file.

  python3 build-single-file.py            -> dist/francis-ruan.html (standalone page)
  python3 build-single-file.py --artifact -> dist/artifact.html     (body only)

The three project pages become in-document sections, so the whole portfolio
reads in one scroll. CSS and the headshot are inlined; nothing loads from disk
except the Google Fonts stylesheet.
"""
import base64, mimetypes, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
DIST = ROOT / "dist"
ARTIFACT = "--artifact" in sys.argv
PAGES = [("who-am-i.html","who-am-i"), ("finance.html","finance"), ("fight-on.html","fight-on"),
         ("my-why.html","my-why"), ("leadership.html","leadership"),
         ("building.html","building"), ("curiosity.html","curiosity"), ("trend.html","trend"),
         ("fun.html","fun"), ("awards.html","awards"), ("thorne.html","thorne"),
         ("celsius.html","celsius"), ("poppi.html","poppi"), ("vitabiotics.html","vitabiotics"),
         ("nestle.html","nestle"), ("bodi.html","bodi"), ("suntag.html","suntag"),
         ("invisible.html","invisible")]


def data_uri(rel):
    p = ROOT / rel
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def main_of(path):
    s = (ROOT / path).read_text(encoding="utf-8")
    return re.search(r'<main id="main"[^>]*>(.*?)</main>', s, re.S).group(1)


index = (ROOT / "index.html").read_text(encoding="utf-8")
css   = (ROOT / "styles.css").read_text(encoding="utf-8")

# project pages become sections of the one document
extra = []
for path, anchor in PAGES:
    body = main_of(path)
    body = body.replace('href="index.html#work"', 'href="#work"')
    body = re.sub(r'href="(who-am-i|finance|fight-on|my-why|leadership|building|curiosity|trend|fun|awards|thorne|celsius|poppi|vitabiotics|nestle|bodi|suntag|invisible)\.html"', lambda m: 'href="#%s"' % m.group(1), body)
    extra.append(
        f'<section id="{anchor}" class="wrap" style="border-top:1px solid var(--rule-strong)">\n'
        f'{body}\n</section>'
    )

index = index.replace("</main>", "\n".join(extra) + "\n</main>")
index = re.sub(r'href="(who-am-i|finance|fight-on|my-why|leadership|building|curiosity|trend|fun|awards|thorne|celsius|poppi|vitabiotics|nestle|bodi|suntag|invisible)\.html"', lambda m: 'href="#%s"' % m.group(1), index)
index = index.replace('<link rel="stylesheet" href="styles.css">', "<style>\n" + css + "\n</style>")

# 16MB of video cannot ride inside a single file, so the bundle keeps the poster
# frames and points at the real thing on the deployed site.
index = re.sub(r'<video[^>]*>.*?</video>',
               lambda m: '<img src="' + (re.search(r'poster="([^"]+)"', m.group(0)).group(1)
                          if re.search(r'poster="([^"]+)"', m.group(0)) else '') + '" alt="">',
               index, flags=re.S)
for src in sorted(set(re.findall(r'src="(assets/[^"]+)"', index))):
    index = index.replace(f'src="{src}"', f'src="{data_uri(src)}"')

if ARTIFACT:
    # artifact viewers cannot download files, so retarget the resume links
    index = index.replace(
        '<li><a href="Ruan_Francis_Resume.pdf" target="_blank" rel="noopener">Resume</a></li>', '')
    index = index.replace(
        '<span><a href="Ruan_Francis_Resume.pdf" target="_blank" rel="noopener">Resume, PDF</a></span>', '')
    index = index.replace(
        '<dt>Resume</dt><dd><a href="Ruan_Francis_Resume.pdf" target="_blank" rel="noopener">Download, PDF</a></dd>',
        '<dt>Resume</dt><dd>Available on the deployed site</dd>')
    index = re.sub(r'<a href="Ruan_Francis_Resume\.pdf"[^>]*>([^<]*)</a>', r'\1', index)
    # the single-file preview has to scroll, so drop the index-only viewport lock
    index = index.replace("body.index{ height:100dvh; overflow:hidden; }", "")
    index = index.replace(".cover{\n  height:100dvh;", ".cover{\n  min-height:100dvh;")
    index = index.replace('href="index.html"', 'href="#main"')
    index = re.sub(r'href="index\.html(#[a-z]+)"', r'href=""', index)

    head = re.search(r"<head>(.*?)</head>", index, re.S).group(1)
    body = re.search(r"<body[^>]*>(.*?)</body>", index, re.S).group(1)
    keep = []
    m = re.search(r"<title>.*?</title>", head, re.S)
    if m: keep.append(m.group(0))
    keep += re.findall(r'<link[^>]*fonts\.g(?:oogleapis|static)[^>]*>', head)
    m = re.search(r"<style>.*?</style>", head, re.S)
    if m: keep.append(m.group(0))
    out, name = "\n".join(keep) + "\n" + body, "artifact.html"
else:
    out, name = index, "francis-ruan.html"

DIST.mkdir(exist_ok=True)
(DIST / name).write_text(out, encoding="utf-8")
print(f"dist/{name}  {len(out.encode())/1024:.0f} KB")
