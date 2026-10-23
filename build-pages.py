#!/usr/bin/env python3
"""Emit every page from one shared chrome. One typeface, pure white, charcoal."""
import pathlib, math
ROOT = pathlib.Path(__file__).parent

# Canonical origin. Open Graph and canonical tags need absolute URLs; relative ones
# do not resolve when a link is unfurled by LinkedIn, iMessage, Slack.
SITE = "https://francisruan.com"

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Cormorant+SC:wght@400;500;600;700&display=swap" rel="stylesheet">')

ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 100 100'><text y='.9em' font-size='90' font-family='Cormorant Garamond,Georgia,serif' fill='%231C1C1C'>F</text></svg>\">")

def topbar(active=""):
    # No Index item. The name on the left is the way home.
    items=[("my-why.html","Why"),("who-am-i.html","I"),
           ("fight-on.html","Fight On"),("curiosity.html","Inquisitive"),
           ("leadership.html","Stewardship"),
           ("fun.html","Effervescent")]
    li="".join(f'<li><a href="{h}"{" target=_blank rel=noopener" if h.endswith(".pdf") or h.startswith("http") else ""}'
               f'{" style=color:var(--ink)" if t==active else ""}>{t}</a></li>' for h,t in items)
    return ('<header class="topbar"><div class="wrap topbar__in">'
            '<a class="topbar__name" href="index.html">Francis Ruan</a>'
            f'<ul>{li}</ul></div></header>')

FOOT = ('<footer class="foot"><div class="wrap foot__in">'
        '<span>Francis Ruan &middot; USC Marshall &amp; Viterbi, Class of 2029 &middot; Los Angeles</span>'
        '<span><a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a></span></div></footer>')

def page(fn, title, desc, body, active="", body_class="", chrome=True):
    bc = f' class="{body_class}"' if body_class else ""
    canon = SITE + "/" + ("" if fn == "index.html" else fn)
    html = (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta name="color-scheme" content="light">\n<title>{title}</title>\n'
            f'<meta name="description" content="{desc}">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{SITE}/assets/photos/headshot.jpg">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:url" content="{canon}">\n'
            f'<link rel="canonical" href="{canon}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n{ICON}\n{FONT}\n'
            f'<link rel="stylesheet" href="styles.css">\n</head>\n<body{bc}>\n'
            f'<a class="skip" href="#main">Skip to content</a>\n'
            + (topbar(active) + "\n" if chrome else "")
            + f'<main id="main">\n{body}\n</main>\n'
            + (FOOT + "\n" if chrome else "")
            + '</body>\n</html>\n')
    (ROOT / fn).write_text(html, encoding="utf-8")
    return fn

# ------------------------------------------------------------------ VENN ----
DEALCIRCLES = [
  # file, name, zone, disc fill (Alani Nu's mark is white on black)
  ("thorne.svg",        "Thorne",          "trust",         "#FFFFFF"),
  ("alaninu.png",       "Alani Nu",        "audience",      "#000000"),
  ("poppi.svg",         "poppi",           "audience+dist", "#FFFFFF"),
  ("naturesbounty.svg", "Nature's Bounty", "distribution",  "#FFFFFF"),
  ("vitabiotics.png",   "Vitabiotics",     "trust+dist",    "#FFFFFF"),
]

def venn(w=900, h=700):
    """Three soft value zones. Each deal is a brand circle sitting where it landed."""
    cx, cy = w/2, h*0.42
    R = min(w*0.222, h*0.286)
    ox, oy = R*0.535, R*0.30
    Z = {"trust": (cx-ox, cy-oy), "aud": (cx+ox, cy-oy), "dist": (cx, cy+R*0.45)}
    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="vt vd">',
         '<title id="vt">What each buyer paid for</title>',
         '<desc id="vd">Three zones: trust, audience, distribution. Thorne sits in trust, Alani Nu in '
         'audience, Nature\'s Bounty in distribution, Vitabiotics between trust and distribution, '
         'poppi between audience and distribution.</desc>']
    for k, col in (("trust","--trust"),("aud","--aud"),("dist","--dist")):
        x, y = Z[k]
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R}" fill="var({col})" fill-opacity=".05" '
                 f'stroke="var({col})" stroke-opacity=".35"/>')
    for t, x, y, anc, col in (
        ("TRUST",        Z["trust"][0]-R*0.86, Z["trust"][1]-R*0.80, "end",    "--trust"),
        ("AUDIENCE",     Z["aud"][0]+R*0.86,   Z["aud"][1]-R*0.80,   "start",  "--aud"),
        ("DISTRIBUTION", Z["dist"][0],         Z["dist"][1]+R*1.24,  "middle", "--dist")):
        o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anc}" font-size="12" font-weight="600" '
                 f'letter-spacing="2" fill="var({col})">{t}</text>')
    spots = {
      "trust":         (Z["trust"][0]-R*0.44, Z["trust"][1]-R*0.20),
      "audience":      (Z["aud"][0]+R*0.44,   Z["aud"][1]-R*0.20),
      "distribution":  (Z["dist"][0],         Z["dist"][1]+R*0.52),
      "trust+dist":    ((Z["trust"][0]+Z["dist"][0])/2 - R*0.16, (Z["trust"][1]+Z["dist"][1])/2 + R*0.10),
      "audience+dist": ((Z["aud"][0]+Z["dist"][0])/2 + R*0.16,   (Z["aud"][1]+Z["dist"][1])/2 + R*0.10)}
    r = 38
    for f, name, zone, fill in DEALCIRCLES:
        x, y = spots[zone]
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{fill}" stroke="var(--ink)" stroke-width="1"/>')
        o.append(f'<image href="assets/logos/{f}" x="{x-r*0.66:.0f}" y="{y-r*0.40:.0f}" '
                 f'width="{r*1.32:.0f}" height="{r*0.80:.0f}" preserveAspectRatio="xMidYMid meet"/>')
        o.append(f'<text x="{x:.0f}" y="{y+r+17:.0f}" text-anchor="middle" font-size="12" '
                 f'font-weight="500" fill="var(--ink)">{name}</text>')
    o.append("</svg>")
    return "".join(o)

# =============================================================== INDEX ======
PYRAMID = [
  # One word where one word will do. Why opens, the fun closes it out.
  ("my-why-title-sq.jpg",      "Why",                     "my-why.html"),
  ("who-am-i-speech.jpg",      "I",                       "who-am-i.html"),
  ("fight-on-sq.jpg",          "Fight On",                "fight-on.html"),
  ("origin-curiosity.jpg",     "Inquisitive",  "curiosity.html"),
  ("origin-leadership.jpg",    "Stewardship",     "leadership.html"),
  ("origin-fun.jpg",           "Effervescent",       "fun.html"),
]

TRACKS = {
  # page, track, artist, sleeve, and the licensed preview stream Apple serves
  # for this recording. Nothing here is hosted by us and nothing is a full track.
  "index.html":       ("Clocks", "Coldplay", "index", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/d2/9b/17/d29b173f-546a-606b-378f-8f3c333e81f1/mzaf_3952108508633208951.plus.aac.p.m4a"),
  "my-why.html":      ("Cool", "Daniel Caesar", "my-why", ""),
  "fight-on.html":    ("Sparks", "Coldplay", "fight-on", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/47/db/ce/47dbce82-d89c-0897-0da7-26d06ae7e2f2/mzaf_14852507599380441353.plus.aac.p.m4a"),
  "leadership.html":  ("Ivy", "Frank Ocean", "leadership", ""),
  "finance.html":     ("Cantaloupe Island", "Herbie Hancock", "finance", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/96/4f/d0/964fd064-c457-7aeb-d8cd-1c20b05bd82f/mzaf_10273878739295878154.plus.aac.p.m4a"),
  "curiosity.html":   ("Lujon", "Henry Mancini", "curiosity", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/f1/49/9b/f1499b91-e67a-046d-d8b5-35bac9fb4b54/mzaf_919471457877370426.plus.aac.p.m4a"),
  "building.html":    ("Electric Feel", "MGMT", "building", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/47/4a/00/474a0001-c9af-5e52-af16-695889678761/mzaf_2030537019671750043.plus.aac.p.m4a"),
  "awards.html":      ("Golden", "Harry Styles", "awards", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/ea/30/a6/ea30a68d-a13a-39fe-2b03-6d568c8cf735/mzaf_15210582114357314440.plus.aac.p.m4a"),
  "fun.html":         ("Sundown", "LEISURE", "fun", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/40/1d/9e/401d9e53-bfdf-5de6-9de4-f9fc03a88444/mzaf_1416381691062382667.plus.aac.p.m4a"),
  "who-am-i.html":    ("Bubbly", "Colbie Caillat", "who-am-i", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/78/7f/ca/787fca5f-4ce3-7817-37b8-981833738ac2/mzaf_3992405577716362448.plus.aac.p.m4a"),
  "trend.html":       ("Cantaloupe Island", "Herbie Hancock", "finance", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/96/4f/d0/964fd064-c457-7aeb-d8cd-1c20b05bd82f/mzaf_10273878739295878154.plus.aac.p.m4a"),
  "invisible.html":   ("Lujon", "Henry Mancini", "curiosity", "https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview211/v4/f1/49/9b/f1499b91-e67a-046d-d8b5-35bac9fb4b54/mzaf_919471457877370426.plus.aac.p.m4a"),
}

AUTOPLAY = (
  # Nothing plays for the first two seconds, so a page never opens with sound
  # on top of it. The element carries no autoplay attribute; this is the only
  # path to playing, which is what makes the gate hold.
  '<script>'
  '(function(){'
  'var a=document.querySelector("audio[data-auto]");if(!a)return;'
  'a.volume=0.35;var stopped=false,armed=false;'
  'a.addEventListener("pause",function(){stopped=true;});'
  'function go(){if(stopped||!armed)return;var p=a.play();if(p&&p.catch)p.catch(function(){});}'
  'setTimeout(function(){armed=true;go();},2000);'
  'if(document.readyState!=="complete")window.addEventListener("load",go,{once:true});'
  '["pointerdown","keydown","touchstart","wheel","scroll"].forEach(function(e){'
  'window.addEventListener(e,go,{once:true,passive:true});});'
  '})();'
  '</script>'
)

def soundtrack(fn):
    """The sleeve, the title, and a player that starts itself.

    The audio is Apple's own licensed thirty second preview for that exact
    recording, streamed from their CDN, so this site hosts no music and
    redistributes nothing. It loops, because thirty seconds of silence halfway
    down a page is worse than a repeat.

    Every browser blocks audible autoplay until a site has earned it or the
    visitor has touched the page, and that is enforced above the document where
    no markup can reach. So this does both: it asks to play on load, which works
    for anyone the browser already trusts, and it asks again on the first click,
    key, or scroll, which covers everybody else. Pausing it once stops it asking.
    """
    t = TRACKS.get(fn)
    if not t: return ""
    title, artist, sleeve, preview = t
    from urllib.parse import quote
    q = quote(f"{title} {artist}")
    player = (f'<audio class="track__p" data-auto loop controls '
              f'preload="auto" src="{preview}"></audio>' if preview else "")
    return ('<div class="track">'
            '<div class="track__top">'
            f'<img class="track__art" src="assets/tracks/{sleeve}.jpg" alt="" loading="lazy" width="300" height="300">'
            '<span class="track__meta">'
            f'<span class="track__t">{title}</span>'
            f'<span class="track__ar">{artist}</span>'
            '</span></div>'
            + player +
            f'<a class="track__l" href="https://open.spotify.com/search/{q}" target="_blank" rel="noopener">'
            'Full track &rarr;</a>'
            + (AUTOPLAY if preview else "")
            + '</div>')

def ask(line="If any of this is worth an argument, I would like to have it."):
    return ('<div class="ask"><p>' + line +
            ' <a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a></p></div>')

def brick(fname, label, href):
    p = ROOT / "assets" / "photos" / fname
    img = f'<img src="assets/photos/{fname}" alt="">' if p.exists() else ""
    return (f'<a class="brick" href="{href}"><span class="brick__img">{img}</span>'
            f'<span class="brick__k">{label}</span></a>')

def belt():
    """Three plates across, pushed sideways. Every image is held in black and white
    here and only takes its colour once you have opened it, which is done with a CSS
    animation on the destination page rather than with script. The counter under the
    belt is driven by a scroll-linked animation, so the counter itself needs no script
    and simply rests on 01 in browsers that do not support one."""
    rows = []
    n = len(PYRAMID)
    for i, (fname, label, href) in enumerate(PYRAMID, 1):
        pth = ROOT / "assets" / "photos" / fname
        img = f'<img src="assets/photos/{fname}" alt="" loading="lazy">' if pth.exists() else ""
        ext = ' target=_blank rel=noopener' if href.startswith('http') else ''
        rows.append(
            f'<a class="frame" href="{href}"{ext}>'
            f'<span class="frame__img">{img}</span>'
            f'<span class="frame__k">[ {label} ]</span>'
            f'</a>')
    ticker = "".join(f'<span>{i:02d}</span>' for i in range(1, n + 1))
    return ('<div class="beltwrap">'
            f'<div class="belt">{"".join(rows)}</div>'
            '<p class="belt__count" aria-hidden="true">'
            f'<span class="belt__win"><span class="belt__roll">{ticker}</span></span>'
            f'<span class="belt__of">of {n:02d}</span>'
            + '</p>'
            f'<p class="belt__sr">{n} sections, pushed sideways.</p>'
            '</div>')

INDEX = f"""<div class="sheet">
  <div class="cover">

    <header class="poster">
      <h1 class="poster__name">Francis<br>Ruan</h1>
      <p class="poster__sub">student at university of southern california</p>
      {soundtrack("index.html")}
    </header>

    {belt()}

    <footer class="cover__foot">
      <p class="cover__links">
        <a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a>
        <a href="https://www.linkedin.com/in/francisruan" target="_blank" rel="noopener">LinkedIn</a>
      </p>
    </footer>

  </div>
</div>"""

page("index.html","Francis Ruan",
     "USC student studying how companies build, measure and finance growth. Nine ways in.",
     INDEX, body_class="index", chrome=False)
print("index.html")




# ========================================================== SUPPLEMENTS =====
SHELF = [
  ("Gut + digestion", [
    ("L-Glutamine",  "Gut cell fuel, potential barrier support"),
    ("K\u0113pos",      "Beneficial gut bacteria, digestive comfort"),
    ("Milk Thistle", "Antioxidant activity. Clinical benefit uncertain")]),
  ("Energy + performance", [
    ("Creatine",     "ATP replenishment, strength, possible cognitive benefit"),
    ("Vitamin B1",   "Carbohydrate metabolism, nerve and heart function"),
    ("B-Complex",    "Energy metabolism, red blood cell production")]),
  ("Heart + brain", [
    ("Omega-3 EPA/DHA", "Heart, brain and retinal function"),
    ("Taurine",      "Cellular fluid balance, bile formation")]),
  ("Blood + oxygen", [
    ("Iron Bisglycinate", "Iron stores, hemoglobin, oxygen delivery"),
    ("Vitamin C",    "Iron absorption, collagen, antioxidant defense")]),
  ("Immune + repair", [
    ("Zinc",         "Immune function, wound healing, DNA synthesis"),
    ("Elderberry",   "Possible cold and flu symptom relief")]),
  ("Bones + recovery", [
    ("Vitamin D + K2", "Calcium absorption, bone mineralization"),
    ("Magnesium Glycinate", "Muscle and nerve function, sleep support"),
    ("Electrolytes", "Hydration, fluid balance, nerve signaling")]),
]

def shelf(w=1040, h=1520):
    r = 252
    cols = [300, 740]
    rows = [300, 772, 1244]
    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="st sd">',
         '<title id="st">What I take every day</title>',
         '<desc id="sd">Fifteen supplements grouped into six overlapping circles: gut and digestion, '
         'energy and performance, heart and brain, blood and oxygen, immune and repair, bones and recovery.</desc>']
    for i, (title, items) in enumerate(SHELF):
        cx, cy = cols[i % 2], rows[i // 2]
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="var(--ink)" '
                 f'stroke-width="1.2" stroke-opacity=".55"/>')
        ty = cy - 150
        o.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-family="var(--f-head)" '
                 f'font-size="30" font-weight="600" font-style="italic" fill="var(--ink)">{title}</text>')
        ty += 46
        for name, note in items:
            o.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-family="var(--f)" '
                     f'font-size="23" font-weight="600" fill="var(--ink)">{name}</text>')
            ty += 26
            o.append(f'<text x="{cx}" y="{ty}" text-anchor="middle" font-family="var(--f)" '
                     f'font-size="17" fill="var(--ink-2)">{note}</text>')
            ty += 40
    o.append("</svg>")
    return "".join(o)

# ============================================================== CHART =======
def multiples_chart(w=820, h=300):
    """Bloomberg-style: one accent, hairline grid, value at the bar end, source note."""
    rows = [("P&amp;G / Thorne", 5.8, "5.8x", "2026E revenue"),
            ("Celsius / Alani Nu", 2.8, "under 3.0x", "2024A revenue"),
            ("Yellow Wood / Nestl&eacute; VMS", 0.8, "0.8x", "2025 sales")]
    L, R, T = 250, 96, 74
    plot = w - L - R
    xmax = 6.5
    bh, gap = 34, 22
    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="ct cd">',
         '<title id="ct">Enterprise value as a multiple of revenue</title>',
         '<desc id="cd">P&G paid 5.8 times revenue for Thorne, Celsius under 3 times for Alani Nu, '
         'and Yellow Wood 0.8 times for Nestle\'s mainstream vitamin brands.</desc>',
         f'<text x="0" y="20" font-family="var(--f-head)" font-size="17" font-weight="600" '
         f'fill="var(--ink)">One aisle, three prices</text>',
         f'<text x="0" y="41" font-family="var(--f)" font-size="13" fill="var(--ink-2)">'
         f'Enterprise value as a multiple of revenue</text>']
    for i in range(0, 7, 2):
        x = L + plot * (i / xmax)
        o.append(f'<line x1="{x:.0f}" y1="{T-8}" x2="{x:.0f}" y2="{T + len(rows)*(bh+gap) - gap + 6:.0f}" '
                 f'stroke="var(--rule)" stroke-width="1"/>')
        o.append(f'<text x="{x:.0f}" y="{T-16}" text-anchor="middle" font-family="var(--f)" '
                 f'font-size="11.5" fill="var(--ink-3)">{i}x</text>')
    for i, (name, val, label, basis) in enumerate(rows):
        y = T + i * (bh + gap)
        bw = plot * (val / xmax)
        o.append(f'<text x="{L-16}" y="{y+bh*0.46:.0f}" text-anchor="end" font-family="var(--f)" '
                 f'font-size="14" fill="var(--ink)">{name}</text>')
        o.append(f'<text x="{L-16}" y="{y+bh*0.46+16:.0f}" text-anchor="end" font-family="var(--f)" '
                 f'font-size="11" fill="var(--ink-3)">{basis}</text>')
        o.append(f'<rect x="{L}" y="{y}" width="{bw:.1f}" height="{bh}" fill="var(--trust)"/>')
        o.append(f'<text x="{L+bw+10:.0f}" y="{y+bh*0.68:.0f}" font-family="var(--f)" font-size="15" '
                 f'font-weight="600" fill="var(--ink)">{label}</text>')
    base = T + len(rows)*(bh+gap) - gap + 6
    o.append(f'<line x1="{L}" y1="{base}" x2="{w-R}" y2="{base}" stroke="var(--ink)" stroke-width="1"/>')
    o.append(f'<text x="0" y="{base+30}" font-family="var(--f)" font-size="11" fill="var(--ink-3)">'
             f'Sources: company announcements, BevNET, SupplySide SJ, NutraIngredients. '
             f'Thorne consideration is trade-press reported.</text>')
    o.append("</svg>")
    return "".join(o)

# =============================================================== BRAIN ======
CURIOSITIES = [
  ("Right and wrong", [
    ("Ethics",            "Whether a thing being legal, profitable and completely normal has any bearing on whether it is right. Usually none, and the gap is where everything interesting is."),
    ("Philosophy",        "Mostly the old questions, asked by people with no internet and apparently far more time to think than anybody has now."),
    ("Inequality",        "Not the fact of it. The machinery that keeps it standing after everyone agrees it should not."),
    ("Education &amp; attention", "The most valuable thing a society allocates, handed out by postcode."),
    ("Mandarin",          "What I can and cannot say to my mother in her own language, and what that gap costs both of us."),
  ]),
  ("Things I am trying to make", [
    ("Script writing",    "Dialogue is the hardest thing I have tried to write, because people almost never say what they mean and the page has to know that."),
    ("Nineties films",    "The look, specifically. Why a frame shot in 1994 feels warmer than anything a far better camera manages now."),
    ("Stand-up",          "The same question as the page, with a stopwatch on it and no edit button."),
    ("Creative writing",  "How a sentence gets somebody to feel something they did not arrive intending to feel."),
    ("Interface design",  "Persuasion with no words in it at all, which is the hardest version."),
  ]),
  ("Questions nobody can answer for me", [
    ("The history of moustaches", "Yes, really. People decided this, repeatedly, across centuries, and almost nobody wrote down why."),
    ("Why avocados have pits",    "A seed that size needs something enormous to swallow it whole and wander off. The going theory is that whatever did is extinct."),
    ("The origins of tangerines", "Nearly every citrus in the shop is a blend of three ancestors, and the family tree reads like a scandal."),
    ("The terracotta army",       "Thousands of them, no two faces alike, standing in the dark for two thousand years for an audience of nobody."),
    ("Biphasic sleep",            "For most of recorded European history people slept in two shifts and woke on purpose around midnight. We forgot entirely, then started medicating it."),
  ]),
  ("Mechanism, and what things are worth", [
    ("Pathogenesis",             "Mechanism first, always. Not that sleep matters but what glymphatic clearance actually is."),
    ("Longevity",                "Looking after the body and the mind I was handed, with a standing suspicion that most of the advice is downstream of somebody selling something."),
    ("Self-quantification",      "Running bloodwork against my own baselines, which sounds clinical and is really curiosity pointed inward."),
    ("Endurance",                "The only laboratory I have where the variable is me."),
    ("Finance &amp; valuation",  "What a business is quietly worth to somebody who understands it better than its accounts do."),
    ("Consumer M&amp;A",         "Why two companies on the same shelf clear seven times apart."),
  ]),
]

def plate():
    """Numbered and ruled, in the cover's language. The groups are loose on
    purpose: the jump from the terracotta army to a gross margin is the whole
    point, so nothing here is arranged to look tidier than it is."""
    out, n = ['<div class="plate">'], 0
    for group, rows in CURIOSITIES:
        out.append(f'<section class="pl__g"><h3 class="pl__h">{group}</h3><ol class="pl__l">')
        for label, note in rows:
            n += 1
            out.append(f'<li class="pl__i"><span class="pl__n">[ {n:02d} ]</span>'
                       f'<span class="pl__t">{label}</span>'
                       f'<span class="pl__d">{note}</span></li>')
        out.append("</ol></section>")
    out.append("</div>")
    return "".join(out)


CURIO = f"""<header class="band">
  <div class="wrap band__in">
    <p class="band__k">Inquisitive</p>
    <h1 class="band__t">Things I Keep Going Back To</h1>
  </div>
</header>
<div class="wrap">
<div class="body">
{soundtrack("curiosity.html")}
<figure class="defn">
  <p class="defn__w">curiosity</p>
  <div class="defn__b">
    <p class="defn__d">not the wish to know a thing, which is appetite and passes, but the refusal to accept the headline as the answer. the suspicion that every explanation you were handed is the shortened version, and the willingness to be the only person in the room still asking after everybody else has moved on.</p>
    <p class="defn__p">[ kyoor-ee-<em>os</em>-i-tee ]</p>
  </div>
</figure>

<p>Most people are taught it as a childhood trait, something you have plenty of at six and are expected to grow out of by twenty, as though the questions were a phase rather than the point. I have come to think it is closer to a discipline, and an unfashionable one, because it costs you something socially to keep asking after the conversation has agreed to stop.</p><p>What follows does not resolve into a theme. I spent a while trying to make it resolve, and the honest version is that the same appetite that wants to know what a business is quietly worth also wants to know why an avocado has a pit that size. I have stopped apologising for the second one.</p>

{plate()}

<h2>Contents</h2>
<ol class="toc">
  <li><a href="https://www.paloaltoonline.com/short-story/2025/07/17/short-story-contest-2025-the-dinner-table/" target="_blank" rel="noopener">The Dinner Table</a><span class="toc__m">Palo Alto Weekly &middot; First place, Young Adult &middot; 2025</span></li>
  <li><span class="toc__t">The Hands We No Longer Raise</span><span class="toc__m">2025</span></li>
  <li><span class="toc__t">The Disunited States: How America Learned to Live with Inequality</span><span class="toc__m">2025</span></li>
  <li><span class="toc__t">Longitudinal Self-Quantification of Recovery, Stress, and Well-Being Using Wearable Technology</span><span class="toc__m">2025</span></li>
  <li><a href="assets/Trade-Build-Settle.pdf" target="_blank" rel="noopener">Trade, Build, Settle</a><span class="toc__m">Essay &middot; 1,600 words</span></li>
  <li><a href="trend.html">Five Deals, Six Weeks, and a Sevenfold Spread</a><span class="toc__m">September 2026</span></li>
  <li><a href="invisible.html">The Assets AI Builds That Nobody Records</a><span class="toc__m">2026</span></li>
</ol>

{ask("If any of this overlaps with something you are thinking about, write to me.")}
</div>
<nav class="nextprev"><a href="index.html">&larr; All six</a></nav>
</div>"""

page("curiosity.html","Inquisitive | Francis Ruan",
     "A labelled plate of what Francis Ruan is curious about, and the essays and stories that came out of it.",
     CURIO, active="Inquisitive")
print("curiosity.html")

# =============================================================== TREND ======
def rows(pairs, cap="From public sources."):
    r="".join(f'<tr><th scope="row">{k}</th><td class="n">{v}</td></tr>' for k,v in pairs)
    return f'<div class="tbl"><table><caption>{cap}</caption><tbody>{r}</tbody></table></div>'

def ul(items): return "<ul>"+"".join(f"<li>{i}</li>" for i in items)+"</ul>"

DEALS = [
 ("thorne.html","pg.svg","P&amp;G / Thorne","5.8x","2026E revenue","Trust"),
 ("celsius.html","celsius.svg","Celsius / Alani Nu","&lt;3x","2024A revenue","Audience"),
 ("poppi.html","pepsico.svg","PepsiCo / poppi","$1.65bn","net of tax benefits","Audience + Distribution"),
 ("vitabiotics.html","vitabiotics.png","Bain / Vitabiotics","~$1.2bn","no public revenue","Trust + Distribution"),
 ("nestle.html","yellowwood.svg","Yellow Wood / Nestl&eacute;","0.8x","2025 sales","Distribution"),
]
def dealgrid():
    out=['<div class="dealgrid">']
    for href,lg,nm,mx,sb,_ in DEALS:
        out.append(f'<a href="{href}"><span class="lg"><img src="assets/logos/{lg}" alt=""></span>'
                   f'<span class="nm">{nm}</span><span class="mx">{mx}</span>'
                   f'<span class="sb">{sb}</span></a>')
    out.append("</div>")
    return "".join(out)

TREND = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">The trend I follow</p>
  <h1>Five Deals, Six Weeks, and a Sevenfold Spread</h1>
  <p class="meta"><span>Consumer health and wellness</span><span>Public sources only</span><span>September 2026</span></p>
</header>

<div class="body">
{soundtrack("trend.html")}
<p class="kicker">Here is a thing that happened this summer, and I have not been able to stop turning it over.</p>

<p>In about six weeks, five companies that all essentially sell you a bottle of pills changed hands. Procter &amp; Gamble paid a reported $3.8 billion for Thorne, which is roughly <strong>5.8 times</strong> next year&rsquo;s revenue. Four weeks later Nestl&eacute; sold seven vitamin brands doing $1.2 billion of sales for $1 billion, which is about <strong>0.8 times</strong>.</p>

<p>What I keep returning to is that these were the same aisle, and in some stores genuinely the same shelf, and yet the price a buyer proved willing to pay for a foot of it varied by a factor of seven.</p>

<div class="chartwrap">{multiples_chart()}</div>

<p>My first instinct was that somebody had got it wrong, because that is everyone&rsquo;s first instinct and it is almost always the wrong one. Nobody at that size makes a seven-times error in public, twice, four weeks apart. So the more interesting question is what the two buyers thought they were buying, and whether it was the same thing at all. (It was not.)</p>

<h2>The six weeks, in order</h2>
<div class="tbl"><table>
  <caption>Announced 24 July to 2 September 2026. Thorne and Vitabiotics values are trade-press reported rather than confirmed by the parties, and Vitabiotics publishes no revenue, so there is no multiple for it rather than a guessed one.</caption>
  <thead><tr><th>Date</th><th>Buyer / target</th><th class="n">Value</th><th class="n">Basis</th></tr></thead>
  <tbody>
    <tr><td>24 Jul</td><td><a href="vitabiotics.html">Bain Capital / Vitabiotics</a></td><td class="n">~$1.2bn reported</td><td class="n">no public revenue</td></tr>
    <tr><td>4 Aug</td><td><a href="thorne.html">P&amp;G / Thorne</a></td><td class="n">$3.8bn reported</td><td class="n">~5.8x 2026E</td></tr>
    <tr><td>6 Aug</td><td>Kirin / Jamieson Wellness</td><td class="n">C$2.5bn EV</td><td class="n">27% premium</td></tr>
    <tr><td>1 Sep</td><td><a href="nestle.html">Yellow Wood / Nestl&eacute; VMS</a></td><td class="n">$1.0bn</td><td class="n">~0.8x 2025</td></tr>
    <tr><td>2 Sep</td><td>cbdMD / Twinlab</td><td class="n">undisclosed</td><td class="n">n/a</td></tr>
  </tbody>
</table></div>

<h2>Three things get bought in this aisle</h2>
<p><strong>Trust</strong> is what a clinician will put their own name behind. <strong>Audience</strong> is who already listens to you before you have sold them anything. <strong>Distribution</strong> is shelf space, freight, a factory, and all the deeply unglamorous machinery that gets a bottle into a hand. Nobody buys only one. But the price tells you which one they came for.</p>

<div class="vennwrap">{venn()}
<p class="vennkey"><span><b>Trust</b> what a professional vouches for</span><span><b>Audience</b> who already listens</span><span><b>Distribution</b> shelf, freight, factory</span></p>
</div>

<h2>The tell is the seller, not the buyer</h2>
<p>This is the part I find genuinely delightful, and I want to be clear that I mean delightful.</p>

<p>Nestl&eacute; did not leave the supplement business. It kept Solgar. It kept Pure Encapsulations. Those are its two science-led, practitioner-facing brands, and it sold the seven that compete on price and placement, and its chief executive said, in the flat language these announcements are always written in, that the company is focusing where it has the strongest competitive advantage.</p>

<p>Which is a very polite way of saying: these two things are not the same business and we have stopped pretending they are.</p>

<p class="pull">A seller sorted its own cupboard along exactly the line the market had drawn four weeks earlier, in public, with a billion dollars.</p>

<p>You do not often get confirmation that clean. Usually you have to wait years and squint.</p>

<h2>What I think happens next</h2>
<p>Supplements spent about forty years as a commodity business. Fill a bottle, buy shelf position, compete on price, win on distribution because there was nothing else to win on. The product was never really the product. The placement was.</p>

<p>What repriced this summer is not the pills. It is proof. And my read, which I will hold loosely because five deals is a cluster and not a dataset, is that the next decade in this category belongs to whoever can substantiate a claim rather than whoever can fill a shelf.</p>

<p>The moat will not be formulation. Formulation is copyable in a quarter and private label copies it for less, cheerfully, forever. The moat is third-party testing plus practitioner distribution, because a competitor can match your ingredient panel and cannot match a doctor saying your name out loud to a patient who is frightened.</p>

<h2>And where I would be wrong</h2>
<p>Every acquirer on that list has world-class distribution, and every one of them is going to be sorely tempted to use it. Putting a clinic brand into every store in America is precisely how you spend the thing you just paid six times revenue for. Trust erodes slowly and invisibly and does not appear in a quarterly number until well after it is gone.</p>

<p>There is also a decent chance I am reading a cycle as a structural shift, which is the classic error and I would rather name it than have it named for me. Rate cuts and a stalled IPO market push sponsors toward strategic exits regardless of anything anyone believes about trust.</p>

<p>So the thing I will actually be watching is small and checkable: whether Thorne is still sold through practitioners in three years, and at what share of revenue. One line. It will tell you whether P&amp;G understood what it bought.</p>

<h2>Why I actually care about this</h2>

<p>I should disclose something, which is that I am not a neutral observer of this aisle. I am a customer standing in it.</p>

<div class="shelfwrap">{shelf()}</div>

<p>Fifteen things, every day. I did not assemble that list casually. I read the mechanism on each one before it went in, and I get bloodwork drawn to check whether any of it is actually doing what it claims.</p>

<p>Here is what unsettled me once I started the deal research. Almost every bottle on that list is made by a company that has just been bought, or just been sold, by one of the parties in the notes above. Thorne. Nestl&eacute;. The names in my analysis turned out to be the names in my cupboard.</p>

<p class="pull">It is not the car. It is the driver.</p>

<p>That is when this stopped being an argument and became a personal question. If the whole premise is that what I am paying for is <em>trust</em>, third-party testing and a formulation somebody staked a reputation on, then the thing I care about is not the product at all. It is who is responsible for it now.</p>

<p>A bottle does not change the day the cap table does. Same label, same powder, same price for a while. What changes is who decides, two years from now, whether the third-party testing is still worth what it costs, and whether the practitioner channel is worth defending when a mass retailer walks in with a larger number.</p>

<p>Which means I will find out whether I was right before most people do. It will show up on my own shelf.</p>

<h2>The notes</h2>
{dealgrid()}
{ask("If you cover consumer and think I have this backwards, that is the email I most want to get.")}
</div>

<nav class="nextprev"><a href="thorne.html">Start with the 5.8x &rarr;</a><a href="index.html">Index</a></nav>
</div>"""

page("trend.html","Five Deals, Six Weeks, and a Sevenfold Spread | Francis Ruan",
     "Between July and September 2026 the supplement aisle changed hands five times at prices from one to six times sales. What the buyers were actually paying for.",
     TREND, active="Inquisitive")
print("trend.html")
print("trend.html")

# ============================================================ DEAL PAGES ====
def deal(fn, title, kicker, lede, meta, table, sections, nxt, srcs, logo):
    secs="".join(f"<h2>{h}</h2>{b}" for h,b in sections)
    src=ul(srcs)
    body=f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow"><a href="trend.html" style="color:inherit">The trend</a> / Deal note</p>
  <h1>{title}</h1>
  <p class="meta">{"".join(f"<span>{m}</span>" for m in meta)}</p>
</header>
<div class="body">
{soundtrack(fn)}
<p style="height:26px;margin:0 0 1.1rem"><img src="assets/logos/{logo}" alt="" style="height:26px;width:auto;max-width:150px"></p>
<p class="kicker">{kicker}</p>
{table}
{secs}
<h3>Sources</h3>{src}
{ask("If you have a better read on this one, I would like to hear it.")}
</div>
<nav class="nextprev"><a href="{nxt[0]}">{nxt[1]}</a><a href="trend.html">All five deals</a></nav>
</div>"""
    page(fn, title.replace("&amp;","&")+" | Francis Ruan", lede.replace('"',''), body, active="The Trend")
    print(fn)

deal("thorne.html","P&amp;G / Thorne",
 "Seven times the price of the deal four weeks later. I wanted to know what the extra six turns were buying, and the answer is not in the bottle.",
 "P&amp;G paid a growth multiple for the one asset in this aisle you cannot manufacture: a clinician willing to put their name on it.",
 ["Announced August 4, 2026","$3.8bn reported","~5.8x 2026E revenue","Perella Weinberg advised Thorne"],
 rows([("Buyer","The Procter &amp; Gamble Company (NYSE: PG)"),("Seller","L Catterton, Flagship Fund"),
       ("Reported consideration","$3.8bn"),("Revenue, 2025","Over $500m"),("Revenue, 2026E","~$650m"),
       ("Implied multiple","~5.8x forward revenue"),("Sponsor entry, Oct 2023","$680m, $10.20 per share, cash"),
       ("Entry premium","94% to unaffected close, July 20, 2023"),("Expected close","Later in 2026")]),
 [("What actually changed hands",
   "<p>P&amp;G already sells supplements. Metamucil, Align, New Chapter. Those brands win on shelf position, freight and price, and P&amp;G is world-class at all three.</p>"
   "<p>Thorne wins on none of them. It got its start in clinics, with practitioners who put their own reputation behind a recommendation, and only later went at consumers directly. That order of operations is the whole asset. You cannot buy into it and you cannot rebuild it once it is spent.</p>"),
  ("Why the seller took the exit",
   "<p>L Catterton took Thorne private in October 2023 for roughly $680m at $10.20 a share, a 94% premium to the undisturbed price. Handing it to a strategic three years later is a clean result and it dodges the risk of a second sponsor sale or a re-IPO in a category where sentiment turns fast.</p>"
   "<p>One thing I will not do is quote you a return. The $680m was an equity take-private value and the $3.8bn is a reported headline. Without the capital structure at both dates, any multiple of money I gave you would be a guess wearing a suit.</p>"),
  ("Does 5.8x survive contact",
   "<p>Thorne did over $500m in 2025 and is tracked near $650m for 2026. Call it 30% growth. At $3.8bn that is a growth-asset price, not a bolt-on price, which means the multiple is not asking whether Thorne is good. It is asking whether Thorne keeps compounding near 30% inside a company built for a completely different kind of brand.</p>"
   + ul(["Brand dilution, which erodes quietly and is only obvious once it is done.",
         "Growth dependence, because at 5.8x there is almost no room to slow down.",
         "Claims and labeling scrutiny, where a mass-market owner is a much bigger target.",
         "The practitioner who recommended Thorne may feel differently about a P&amp;G brand."])),
  ("My call",
   "<p>Not an overpayment. A bet on distribution discipline, which is historically the thing large acquirers of premium brands are worst at. The first thing I would diligence is P&amp;G&rsquo;s plan for holding the practitioner channel while it expands retail, because that channel is the entire 5.8x.</p>")],
 ("celsius.html","Next: Celsius buys an audience &rarr;"),
 ['<a href="https://www.prnewswire.com/news-releases/thorne-enters-into-definitive-agreement-to-be-acquired-by-procter--gamble-302842751.html" target="_blank" rel="noopener">Thorne, definitive agreement</a>, August 4, 2026.',
  '<a href="https://www.supplysidesj.com/market-trends-analysis/experts-give-high-marks-to-p-g-s-bet-on-thorne" target="_blank" rel="noopener">SupplySide SJ</a>, consideration, revenue and multiple.',
  '<a href="https://www.pehub.com/l-catterton-completes-take-private-buyout-of-vitamin-maker-thorne-healthtech/" target="_blank" rel="noopener">PE Hub</a>, take-private terms.'],
 "pg.svg")

deal("celsius.html","Celsius / Alani Nu",
 "A $1.65bn cheque for a brand whose main asset is that people already listen to it. This is the cleanest &lsquo;audience&rsquo; deal on my list.",
 "Celsius bought a following. The disclosure is unusually honest about it, and the EBITDA multiple tells you where the value was supposed to come from.",
 ["Announced February 2025","$1.8bn headline, $1.65bn net","&lt;3x 2024A revenue","~12x synergized EBITDA"],
 rows([("Buyer","Celsius Holdings (NASDAQ: CELH)"),("Target","Alani Nutrition LLC"),
       ("Headline consideration","$1.8bn"),("Less tax assets","$150m"),("Net purchase price","$1.65bn"),
       ("Structure","$1.275bn cash, $500m stock, $25m earn-out"),("Debt financing","$900m"),
       ("Alani Nu revenue, 2024A","$595m"),("Implied multiple","Under 3x revenue"),
       ("Synergized EBITDA, 2024A","$137m, about 12x"),("Stated cost synergies","$50m run-rate over two years")]),
 [("What they were really buying",
   "<p>Under 3x revenue is not a premium in this category, and that is the interesting bit. Alani Nu was not sold as a science story or a shelf story. It was sold as a community that happened to have a product attached, built largely by and for women in a segment that energy drinks had spent a decade ignoring.</p>"
   "<p>You cannot put &lsquo;they already trust her&rsquo; on a balance sheet. You can, however, put it through your own distribution and watch what happens, which is precisely the plan.</p>"),
  ("The number I keep looking at",
   "<p>$50m of run-rate cost synergies inside a $1.65bn price. That is a cost deal on its face. But roughly 12x <em>fully synergized</em> EBITDA is doing a lot of quiet work in that sentence, because it prices the target as though the synergies have already happened.</p>"
   "<p>So the honest read is a low revenue multiple paired with an EBITDA multiple that already assumes execution. Two very different pictures of the same cheque, and which one is true gets decided in the warehouse, not the deck.</p>"),
  ("Where I would push",
   ul(["An audience brand is only worth the audience&rsquo;s attention, and attention is rented, not owned.",
       "$500m of the price is Celsius stock, so the seller is still exposed to Celsius execution.",
       "Cost synergies are the easy half. Nobody has yet shown the revenue half."])),
  ("My call",
   "<p>The most defensible price of the five. Under 3x sales for a brand growing into an adjacent segment is not where deals go wrong. The risk is not the number, it is whether Celsius can scale the thing without sanding off the reason anyone cared.</p>")],
 ("poppi.html","Next: PepsiCo, $1.65bn again &rarr;"),
 ['<a href="https://ir.celsiusholdingsinc.com/news/news-details/2025/Celsius-Holdings-to-Acquire-Alani-Nu-Creating-a-Leading-Better-For-You-Functional-Lifestyle-Platform/default.aspx" target="_blank" rel="noopener">Celsius Holdings</a>, acquisition announcement and terms.',
  '<a href="https://www.bevnet.com/news/2025/celsius-acquires-alani-nu-for-1-8-billion/" target="_blank" rel="noopener">BevNET</a>, structure and multiples.'],
 "celsius.svg")

deal("poppi.html","PepsiCo / poppi",
 "The same net price as Celsius paid, four weeks apart, for a brand in a different aisle. Two of the largest beverage buyers in America agreed on a number without agreeing on a category.",
 "PepsiCo bought an audience and pointed the world&rsquo;s best distribution system at it. The tax structure is the tell.",
 ["Announced March 17, 2025","Closed May 19, 2025","$1.95bn headline, $1.65bn net","Prebiotic soda"],
 rows([("Buyer","PepsiCo, Inc. (NASDAQ: PEP)"),("Target","poppi"),
       ("Headline consideration","$1.95bn"),("Anticipated cash tax benefits","$300m"),
       ("Net purchase price","$1.65bn"),("Contingent consideration","~$0.2bn fair value at close"),
       ("Announced","March 17, 2025"),("Completed","May 19, 2025")]),
 [("Why the structure matters",
   "<p>$1.95bn is the number in the headline. $1.65bn is the number PepsiCo actually cared about, because $300m of anticipated cash tax benefits comes straight back. Add a performance earn-out worth about $0.2bn at close and you get a deal where a real slice of the price only gets paid if poppi keeps doing what it was bought for.</p>"
   "<p>That is a buyer being careful. Which is worth noticing, because the public story was that big soda was panic-buying growth.</p>"),
  ("The thing poppi had",
   "<p>poppi did not win on formulation, and prebiotic soda is not a defensible recipe. It won on being the can people wanted to be seen holding. That is audience, the same asset Celsius bought, and it is why these two deals landed at an identical net price within four weeks of each other.</p>"
   "<p>What PepsiCo adds is the part poppi could never buy: coolers, routes, and shelf position in every store in the country.</p>"),
  ("Where I would push",
   ul(["Audience brands decay when the audience stops feeling early. Ubiquity is the risk, not the reward.",
       "Prebiotic soda has no moat in the liquid. The moat is entirely in the memory of the buyer.",
       "PepsiCo has bought cult brands before. The record on preserving them is mixed at best."])),
  ("My call",
   "<p>The most structurally disciplined deal of the five. Tax benefits and an earn-out do a lot of work here, and I suspect PepsiCo knew exactly what it was underwriting. The open question is whether a distribution machine can carry a brand whose value was partly that it was hard to find.</p>")],
 ("vitabiotics.html","Next: the one nobody covered &rarr;"),
 ['<a href="https://www.pepsico.com/en/newsroom/press-releases/2025/pepsico-completes-acquisition-of-poppi-accelerating-strategic-portfolio-transformation" target="_blank" rel="noopener">PepsiCo</a>, completion announcement.',
  '<a href="https://www.cravath.com/news-insights/pepsicos-dollar195-billion-acquisition-of-poppi.html" target="_blank" rel="noopener">Cravath</a>, headline and net consideration.',
  '<a href="https://www.sec.gov/Archives/edgar/data/77476/000007747625000044/pep-20250614.htm" target="_blank" rel="noopener">PepsiCo Form 10-Q</a>, contingent consideration at close.'],
 "pepsico.svg")

deal("vitabiotics.html","Bain / Vitabiotics",
 "A billion-dollar brand almost nobody outside Britain has heard of. This is the deal that made me rethink the whole framework.",
 "Neither credibility nor commodity. Vitabiotics won a third way: being the one answer to one question, for fifty-five years.",
 ["Signed July 2026","~&pound;900m / ~$1.2bn reported","Not confirmed by the parties","Founded 1971"],
 rows([("Buyer","Bain Capital"),("Target","Vitabiotics Ltd. and VB Group"),
       ("Reported valuation","~&pound;900m / ~$1.2bn"),("Confirmed by parties","No"),
       ("Founded","1971"),("Brands","Pregnacare, Wellman, Wellwoman,<br>Perfectil, Osteocare"),
       ("Also included","Meyer Organics (India), VB Egypt"),("Public revenue","None published")],
      cap="Vitabiotics publishes no revenue, so no multiple appears here. Anyone quoting one is estimating."),
 [("The third model",
   "<p>Thorne won on what a clinician will vouch for. Nestl&eacute;&rsquo;s mainstream brands won on shelf economics. Vitabiotics did neither, and it is bigger than I expected.</p>"
   "<p>It won by owning specific-need aisles outright. Pregnancy. Men&rsquo;s. Women&rsquo;s. Hair and skin. Bone. These are shelves where the shopper arrives with exactly one question and wants exactly one answer. Ask a British pharmacist for a pregnancy multivitamin and you will get a brand name, not a comparison. Being that name for fifty-five years is a moat, and it is a cheaper moat than Thorne&rsquo;s.</p>"),
  ("What Bain is actually underwriting",
   "<p>Bain&rsquo;s Asian private equity team led this, and the perimeter deliberately includes Meyer Organics in India and the Egyptian business. That is not a UK consolidation thesis. That is: take a brand system already proven in one country and run it through markets where the specific-need habit is forming right now.</p>"),
  ("Where I would push",
   ul(["Specific-need aisles are exactly where private label attacks first, because the shopper already knows what they want.",
       "A founder-led company of this age carries commercial relationships that live in people, not contracts.",
       "The India and Africa thesis needs regulatory patience, which sponsors do not always have."])),
  ("My call",
   "<p>The most interesting of the five and the least written about, which is usually a good sign. Without revenue I cannot tell you if the price is right. I can tell you the question that settles it: does being the default answer travel across a border, or is it built one pharmacist at a time?</p>")],
 ("nestle.html","Next: the mirror image, at 0.8x &rarr;"),
 ['<a href="https://www.bloomberg.com/news/articles/2026-07-24/bain-capital-to-buy-1-2-billion-uk-supplements-firm-vitabiotics" target="_blank" rel="noopener">Bloomberg</a>, reported valuation.',
  '<a href="https://www.business-standard.com/companies/news/bain-capital-to-acquire-uk-vitamins-maker-vitabiotics-in-1-2-billion-deal-126072400930_1.html" target="_blank" rel="noopener">Business Standard</a>, group perimeter.'],
 "vitabiotics.png")

deal("nestle.html","Yellow Wood / Nestl&eacute;",
 "Four weeks after P&amp;G paid 5.8x, a seller put the other half of the same aisle on the market at 0.8x. That is the moment the pattern stopped being a coincidence.",
 "Nestl&eacute; did not leave supplements. It kept the science and sold the shelf, sorting its own cupboard along exactly the line the market had just drawn.",
 ["Announced September 1, 2026","$1.0bn","~0.8x 2025 sales","Close expected H1 2027"],
 rows([("Buyer","Yellow Wood Partners"),("Seller","Nestl&eacute;"),("Consideration","$1.0bn"),
       ("Portfolio sales, 2025","$1.2bn"),("Implied multiple","~0.8x trailing sales"),
       ("Brands","Nature&rsquo;s Bounty, Osteo Bi-Flex, Ester-C,<br>Gard, Nuun, Puritan&rsquo;s Pride, Sisu"),
       ("Also included","US private label, plants, distribution"),
       ("Nestl&eacute; retains","Solgar, Pure Encapsulations"),("Expected close","First half of 2027")]),
 [("The detail that gives it away",
   "<p>Read the retained list. Nestl&eacute; kept Solgar and Pure Encapsulations, its two premium science-led brands, and sold the seven that compete on price and placement. Its CEO said the company is focusing where it has the strongest competitive advantage, which is the politest possible way of saying these two things are not the same business.</p>"
   "<p>Eight weeks earlier the market had priced trust at 5.8x. Here is a seller applying the identical split to its own portfolio, with real money, in public.</p>"),
  ("What below 1x actually buys",
   "<p>At 0.8x sales you are not buying brands that compound. You are buying cash flow, a manufacturing base, and a distribution network, and the return has to come from operating the assets better than a conglomerate bothered to. Yellow Wood is a consumer carve-out specialist. This is a carve-out, not a growth story, and the price is honest about that.</p>"
   "<p>They have flagged hydration, gut health and immunity as the pockets with room. That reads right to me, and it points at one brand in particular.</p>"),
  ("The one I would watch",
   "<p>Nuun. Hydration is the only line in this portfolio that behaves like it belongs on the other side of the Venn. If it keeps growing, Yellow Wood bought a growth asset inside a value basket and paid value prices for it, which is how carve-outs make their reputation.</p>"
   + ul(["Standing up services the parent used to provide is where carve-outs usually slip.",
         "Owned brands plus private label under one roof is a channel conflict, not a synergy.",
         "Below 1x there is no multiple to hide behind. It is all operating execution."])),
  ("My call",
   "<p>The right price for what it is, and the most useful deal on the list, because it is the one that proves the framework. P&amp;G told you what trust costs. Nestl&eacute; told you what everything else costs.</p>")],
 ("trend.html","Back to all five &rarr;"),
 ['<a href="https://www.nutraingredients.com/Article/2026/09/01/yellow-wood-buys-nestle-vms-business-for-1b/" target="_blank" rel="noopener">NutraIngredients</a>, terms, brands and portfolio sales.',
  '<a href="https://www.nutritionaloutlook.com/view/yellow-wood-partners-to-acquire-nestle-mainstream-vitamins-supplements-brands" target="_blank" rel="noopener">Nutritional Outlook</a>, scope and retained brands.'],
 "yellowwood.svg")

# ============================================================== HONORS ======
def spiderweb(W=1060, H=680):
    cx, cy = W/2, H/2
    R1, R2 = 138, 268
    hubs = [
      ("ACADEMIC",   -140, ["Valedictorian, 1 of 553","GPA 3.92 at USC","SAT 1540","AI for Business, 1 of 35","Dean&rsquo;s List, 2x"]),
      ("SCHOLARSHIP", -40, ["USC Presidential Scholar","Goldman Scholar","Woodruff Family Endowed"]),
      ("RECOGNITION",  40, ["TEDx Speaker","1st Place, Stanford ProCo","OpenAI Challenge Finalist","California Congressional Award","Asian Pacific American of Action"]),
      ("LEADERSHIP",  140, ["Student Body President, 4 terms","Commencement Speaker","Marshall Ambassador","Lacrosse Alumni Chair","Vuori Campus Brand Ambassador"]),
    ]
    o=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="ht hd">',
       '<title id="ht">Honors and awards</title>',
       '<desc id="hd">A radial web linking Francis Ruan to four clusters: academic, scholarship, recognition and leadership, each with its awards.</desc>',
       '<g stroke="var(--rule-2)" fill="none" stroke-width="1">']
    lines=[]; nodes=[]; labels=[]
    for name, deg, leaves in hubs:
        a = math.radians(deg)
        hx, hy = cx + R1*math.cos(a), cy + R1*math.sin(a)
        lines.append(f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{hx:.0f}" y2="{hy:.0f}" stroke="var(--ink)"/>')
        n = len(leaves)
        spread = 46 if n > 3 else 34
        for i, leaf in enumerate(leaves):
            t = (i - (n-1)/2) / max(n-1, 1)
            la = math.radians(deg + t*spread)
            lx, ly = cx + R2*math.cos(la), cy + R2*math.sin(la)
            lines.append(f'<line x1="{hx:.0f}" y1="{hy:.0f}" x2="{lx:.0f}" y2="{ly:.0f}"/>')
            nodes.append(f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="3" fill="var(--ink)"/>')
            right = math.cos(la) >= 0
            tx = lx + (11 if right else -11)
            labels.append(f'<text x="{tx:.0f}" y="{ly+4:.0f}" text-anchor="{"start" if right else "end"}" '
                          f'font-size="13" fill="var(--ink)">{leaf}</text>')
        nodes.append(f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="5.5" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>')
        ox = 0 if abs(math.cos(a)) < .35 else (16 if math.cos(a) > 0 else -16)
        oy = -14 if math.sin(a) < 0 else 22
        anc = "middle" if abs(math.cos(a)) < .35 else ("start" if math.cos(a) > 0 else "end")
        labels.append(f'<text x="{hx+ox:.0f}" y="{hy+oy:.0f}" text-anchor="{anc}" font-size="10.5" '
                      f'font-weight="600" letter-spacing="1.6" fill="var(--ink-3)">{name}</text>')
    o += lines + ['</g>'] + nodes
    o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="46" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>')
    o.append(f'<text x="{cx:.0f}" y="{cy-3:.0f}" text-anchor="middle" font-size="13" font-weight="600">FRANCIS</text>')
    o.append(f'<text x="{cx:.0f}" y="{cy+13:.0f}" text-anchor="middle" font-size="13" font-weight="600">RUAN</text>')
    o += labels
    o.append("</svg>")
    return "".join(o)

RECORD = [
  ("Academic", [
    ("Valedictorian", "Top 5 of 553, Los Altos High School"),
    ("AI for Business, USC", "Joint Marshall and Viterbi degree. 1 of 35 admitted, under 1% acceptance, third cohort"),
    ("GPA", "3.92 at USC. 4.0 in high school"),
    ("SAT", "1540"),
    ("Dean&rsquo;s List", "Twice"),
    ("Global Leader Academy", "Top 10%"),
  ]),
  ("Scholarships", [
    ("USC Presidential Scholar", "Half-tuition merit award"),
    ("Woodruff Family Endowed Scholarship", ""),
    ("Morgan Stanley Endowed Scholarship", ""),
  ]),
  ("Recognition", [
    ("TEDx Speaker", "<em>Why You Should Make a Done List</em>"),
    ("1st Place, Stanford ProCo", "Competitive programming, modelled on ACM-ICPC"),
    ("AI Innovation Challenge", "USC Marshall OpenAI Lab. Selected from 500+ submissions"),
    ("State of California Congressional Award", ""),
    ("Asian Pacific American of Action", ""),
    ("Marshall Ambassador", ""),
    ("Short Story Contest, First Place", "Young Adult category, Palo Alto Weekly, 39th annual"),
  ]),
  ("Leadership", [
    ("Commencement Speaker", "Chosen by my class to address 500+ graduating seniors"),
    ("Student Body President", "Four terms"),
    ("Deployed Engineer, AI Builder Hub", "1 of 4 student engineers"),
    ("Alumni Chair, USC Men&rsquo;s Lacrosse", "350+ alumni, 51 graduating classes, $165K budget"),
    ("Campus Brand Manager, Vuori", "The only USC student selected"),
    ("Team Captain, Varsity Football", "Four years, three on varsity"),
  ]),
]

def record():
    out = []
    for group, rows in RECORD:
        out.append(f'<section class="rec"><h2 class="rec__h">{group}</h2><dl class="rec__l">')
        for name, note in rows:
            out.append(f'<div class="rec__r"><dt>{name}</dt><dd>{note}</dd></div>')
        out.append("</dl></section>")
    return "".join(out)

HON = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">Lucky</p>
  <h1>Everything, on One Page</h1>
  <p class="meta"><span>Los Altos High School, 2021 to 2025</span><span>USC, 2025 to present</span></p>
</header>
<div class="body">
  {soundtrack("awards.html")}
  <figure class="lead">
    <img src="assets/photos/awards.jpg" alt="Francis Ruan as a boy, arms raised on a school blacktop" width="900" height="900">
    <figcaption>Arms up on a blacktop, years before there was anything to put on a list. The reaction has not changed a great deal since.</figcaption>
  </figure>
  <p class="kicker">I have called this section Lucky, and I would like to be exact about what I mean by it, because false modesty is only bragging with better manners.</p>
  <p>I worked for all of these and I am not going to pretend otherwise. What I did not do is arrange the conditions that made the work count for anything, and those conditions turn out to be most of the story: the teacher who kept reading after the first impression had already been formed, the mother who took the night shift so that the school district would be the one it was, the particular year in which a competition happened to be looking for exactly the thing I happened to have been practising. Effort is the part I can honestly claim. Timing is not, and neither is anybody else&rsquo;s generosity, and a list like this one reads very differently once you have admitted how much of it was handed to you by people who do not appear anywhere on it.</p>
  {record()}
  {ask("If you want the story behind any one of these, ask me about it.")}
</div>
<nav class="nextprev"><a href="fight-on.html">How most of these actually happened &rarr;</a><a href="index.html">Index</a></nav>
</div>"""


# ======================================================== WORK + ESSAY ======
SVG_FLOW = ('<svg viewBox="0 0 800 250" role="img" aria-label="Before, five manual steps taking about ninety minutes. '
 'After, ingest, normalize and rules produce a short exception queue reviewed in one to three minutes.">'
 '<g font-family="Instrument Sans,Helvetica,Arial,sans-serif" font-size="12.5">'
 '<text x="0" y="12" font-size="10" font-weight="600" letter-spacing="1.5" fill="#9A9A9A">BEFORE</text>'
 '<g fill="#FFFFFF" stroke="#D4D4D4"><rect x="0" y="26" width="140" height="46"/><rect x="162" y="26" width="140" height="46"/>'
 '<rect x="324" y="26" width="140" height="46"/><rect x="486" y="26" width="140" height="46"/><rect x="648" y="26" width="140" height="46"/></g>'
 '<g fill="#1C1C1C" text-anchor="middle"><text x="70" y="45">Pull records</text><text x="70" y="61">by hand</text>'
 '<text x="232" y="45">Reconcile</text><text x="232" y="61">formats</text><text x="394" y="45">Read every</text><text x="394" y="61">line</text>'
 '<text x="556" y="45">Flag the</text><text x="556" y="61">outliers</text><text x="718" y="45">Route for</text><text x="718" y="61">sign-off</text></g>'
 '<g stroke="#D4D4D4"><line x1="142" y1="49" x2="158" y2="49"/><line x1="304" y1="49" x2="320" y2="49"/>'
 '<line x1="466" y1="49" x2="482" y2="49"/><line x1="628" y1="49" x2="644" y2="49"/></g>'
 '<text x="800" y="91" text-anchor="end" font-size="11.5" fill="#9A9A9A">About 90 minutes, every cycle</text>'
 '<line x1="0" y1="114" x2="800" y2="114" stroke="#E8E8E8"/>'
 '<text x="0" y="142" font-size="10" font-weight="600" letter-spacing="1.5" fill="#1C1C1C">AFTER</text>'
 '<g fill="#FAFAFA" stroke="#D4D4D4"><rect x="0" y="156" width="150" height="46"/><rect x="172" y="156" width="150" height="46"/>'
 '<rect x="344" y="156" width="150" height="46"/></g>'
 '<rect x="516" y="156" width="284" height="46" fill="#FFFFFF" stroke="#1C1C1C"/>'
 '<g fill="#1C1C1C" text-anchor="middle"><text x="75" y="175">Ingest</text><text x="75" y="191">records</text>'
 '<text x="247" y="175">Normalize to</text><text x="247" y="191">one shape</text><text x="419" y="175">Apply agreed</text><text x="419" y="191">rules</text>'
 '<text x="658" y="175" font-weight="600">Exception queue</text><text x="658" y="191">reviewed by a person</text></g>'
 '<g stroke="#D4D4D4"><line x1="152" y1="179" x2="168" y2="179"/><line x1="324" y1="179" x2="340" y2="179"/><line x1="496" y1="179" x2="512" y2="179"/></g>'
 '<text x="800" y="221" text-anchor="end" font-size="11.5" fill="#1C1C1C">One to three minutes on selected tasks</text>'
 '<text x="0" y="243" font-size="10" fill="#9A9A9A">Judgment stays with the accountant. Only the search for it is automated.</text></g></svg>')

def workpage(fn, logo, title, lede, meta, kicker, secs, nxt, active="Index"):
    body=f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow"><a href="index.html" style="color:inherit">Index</a> / Work</p>
  <h1>{title}</h1>
  <p class="meta">{"".join(f"<span>{m}</span>" for m in meta)}</p>
</header>
<div class="body">
{soundtrack(fn)}
<p style="height:28px;margin:0 0 1.1rem"><img src="assets/logos/{logo}" alt="" style="height:28px;width:auto;max-width:150px"></p>
<p class="kicker">{kicker}</p>
{"".join(f"<h2>{h}</h2>{b}" for h,b in secs)}
{ask()}
</div>
<nav class="nextprev"><a href="{nxt[0]}">{nxt[1]}</a><a href="index.html">Index</a></nav>
</div>"""
    page(fn, title+" | Francis Ruan", lede.replace('"',''), body, active=active)
    print(fn)

workpage("bodi.html","bodi.svg","BODi",
 "I built finance tooling that turned repetitive invoice and general-ledger review into exception-based work.",
 ["BODi, The Beachbody Company (NASDAQ: BODI)","AI Intern, Finance &amp; Growth","April 2026 to present","El Segundo"],
 "A task that ate ninety minutes a cycle now takes about three. The interesting part was never the speed. It was working out what a human was actually there to decide.",
 [("The problem","<p>Recurring invoice and general-ledger review burned analyst time on records that were almost always correct. The cost was never the reviewing. It was that the handful of exceptions worth a decision sat inside a queue you had to read line by line to find.</p>"),
  ("What I owned","<p>The tooling, not the policy. Thresholds, controls and sign-off stayed with FP&amp;A and Accounting. I built to their definitions and they validated every output before anything was relied on.</p>"),
  ("Approach", ul(["Defined a genuine exception with the FP&amp;A and Accounting owners before writing anything.",
                   "Rebuilt general-ledger cleansing so records arrived in one shape rather than several.",
                   "Ran automated output against manual review until they agreed, then tightened the thresholds."])),
  ("Result","<p>Selected recurring tasks moved from roughly 90 minutes to one to three minutes. I sized approximately <strong>$784K</strong> in annualized operating expense reduction and presented it to the MD of Accounting.</p>"
   f'<figure style="margin:1.6rem 0"><div style="border:1px solid var(--rule);background:var(--wash);padding:1.2rem;overflow-x:auto">{SVG_FLOW}</div>'
   '<figcaption class="quiet" style="margin-top:.6rem">Sanitized diagram, drawn from scratch. No BODi systems, screens, records or figures beyond those on my public resume appear here.</figcaption></figure>'),
  ("What I would fix","<p>The saving is a run-rate estimate from task frequency and loaded analyst cost, not realized P&amp;L, and I would say so before anyone asked.</p>"
   "<p>The thresholds are still set by hand. They should be learned from which flags accountants actually action. I would have built that feedback loop before optimizing anything else. Writing this up is what led me to <a href=\"invisible.html\">an essay about where savings like this actually go</a>, which is nowhere on the balance sheet.</p>")],
 ("suntag.html","Next: Suntag Co. &rarr;"))

workpage("suntag.html","suntag.svg","Suntag Co.",
 "I took a solar-powered magnetic charger from customer problem to funded pre-launch. The binding constraint was price, not engineering.",
 ["Founder","May 2025 to present","$5,000 pre-seed","300+ waitlist","Los Angeles"],
 "You have to name a price before anyone has ever paid you one. Tooling gets committed first. That is the whole problem, and I got a piece of it wrong.",
 [("The problem","<p>Hardware pricing is set before you have demand data, because tooling and the first production order are committed in advance. Price too low and you delete the margin that funds the second run. Price too high and you hold inventory with no signal about why.</p>"),
  ("What I owned","<p>All of it. Solar viability testing, the interface in Figma, the prototype code, and the demos I ran to watch people react. There was nobody to hand the pricing question to.</p>"),
  ("Approach", ul(["Tested solar output first, because the ceiling capped what the product could honestly claim.",
                   "Treated demos and the waitlist as directional signal, never as stated willingness to pay.",
                   "Reduced it to three inputs: landed unit cost, tolerable price, minimum viable order."])),
  ("Result","<p>Funded pre-launch on a $5,000 pre-seed with a waitlist above 300. That is validation, not revenue, and I will not describe it as more.</p>"
   '<div class="tbl"><table><caption>The pricing decision, split into what was measured and what was assumed.</caption>'
   '<thead><tr><th>Input</th><th>What I knew</th><th>What I assumed</th></tr></thead><tbody>'
   '<tr><td>Solar output</td><td>Measured in testing</td><td>Real use underperforms the bench</td></tr>'
   '<tr><td>Demand</td><td>300+ signups at zero cost</td><td>Some fraction converts at some price</td></tr>'
   '<tr><td>Landed cost</td><td>Quotes at several order sizes</td><td>First run holds quoted tolerances</td></tr>'
   '<tr><td>Price tolerance</td><td>Verbal reactions from demos</td><td>Interest survives a real checkout</td></tr>'
   '<tr><td>Order size</td><td>Supplier tooling and minimums</td><td>Run one funds run two</td></tr>'
   '</tbody></table></div>'),
  ("What I got wrong","<p>I treated the waitlist as demand. A waitlist measures interest at zero cost and says nothing about the price at which that interest survives.</p>"
   "<p>Running it again I would take refundable deposits at two price points before committing to tooling. That converts a soft signal into a number I could actually defend, and it costs almost nothing.</p>")],
 ("trend.html","Next: the trend I follow &rarr;"))

ESSAY = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">Writing</p>
  <h1>The Assets AI Builds That Nobody Records</h1>
  <p class="meta"><span>September 2026</span><span>About 550 words</span></p>
</header>
<div class="body">
{soundtrack("invisible.html")}
<p class="kicker">This summer I automated a finance workflow at a public company. A task that took ninety minutes took about three. I sized the annual saving at roughly $784,000, presented it, and then went looking for where it appeared in the financial statements. It does not.</p>

<p>What actually happened is that an operating expense line stopped growing. There is no asset called &ldquo;the encoded judgment of the accounting team.&rdquo; Under US GAAP, purchased intangibles are capitalized and internally developed ones are largely expensed as incurred, with narrow exceptions for certain software development costs. So the tool was expensed while it was built, and the thing it produced is visible only as an absence: headcount never added, hours never spent, a line that stayed flat while revenue did not.</p>

<p class="pull">The most valuable thing a company builds with AI shows up in its accounts as something that did not happen.</p>

<p>None of this is new in kind. Brand, process and institutional knowledge have always gone unrecorded. What is new is the rate. A workflow that used to take a decade of tribal knowledge to grind down can now be specified in a quarter, and the gap between a company&rsquo;s recorded assets and its real productive capacity opens faster than the accounting was designed to track.</p>

<h2>Why this is a valuation problem</h2>
<p>If you value a company on reported margins, you are measuring the output of these assets without ever seeing the assets. Two companies with identical income statements can hold very different amounts of encoded judgment. The one holding more will show operating leverage your model does not predict, and it will arrive as a pleasant surprise rather than as something you underwrote.</p>

<p>The obvious objection is that &ldquo;invisible asset&rdquo; is precisely what every management team claims when it wants credit for something it cannot prove. That objection is correct, and it is why the claim needs a footprint rather than a narrative.</p>

<p>The footprint I would look for is boring and checkable. Is revenue per employee rising across several periods while the relevant expense line stays flat, with no headcount reduction that explains it? If yes, something real is compounding. If the only evidence is a slide with the word AI on it, nothing is.</p>

<h2>The part I actually care about</h2>
<p>There is a second-order version of this that interests me more. The scarce skill is no longer operating the tool. It is being able to specify a judgment precisely enough that it can be encoded at all.</p>

<p>That is not a technical problem. To automate the invoice review I had to understand why the accountant flags the invoices she flags, which meant understanding the business before I understood the workflow. The model could not tell me that. Nobody could except her.</p>

<p>So this is the bet I am making with my own time. The tools will keep changing and the specification problem will not. I would rather be the person who can describe the judgment than the person who can operate the model, which is also why I would rather learn finance properly than learn another framework.</p>
{ask("If you value companies for a living and think this is wrong, please tell me why.")}
</div>
<nav class="nextprev"><a href="trend.html">The trend &rarr;</a><a href="index.html">Index</a></nav>
</div>"""
page("invisible.html","The Assets AI Builds That Nobody Records | Francis Ruan",
     "AI's most valuable output is an unrecorded intangible. Why that is a valuation problem, and what to look for instead.",
     ESSAY, active="Writing")
print("invisible.html")


FIN = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">Finance</p>
  <h1>What I Am Actually Trying to Learn</h1>
  <p class="meta"><span>Deal analysis</span><span>Operating finance</span><span>Updated September 2026</span></p>
</header>
<div class="body">

{soundtrack("finance.html")}
<p class="kicker">You ran a valuation this morning and did not notice you were doing it.</p>

<p>Somebody offered you something and you priced it in about four hundred milliseconds. Is this friendship accretive, or has it been quietly dilutive for a year and you have not wanted to say so out loud. Is the extra hour of sleep worth more than the extra hour of work, and worth more to which version of you, the one at eleven at night or the one at six in the morning, because those two are running very different discount rates. We do this constantly, we do it silently, and we almost never write any of it down, which is the only reason it does not look like finance.</p>

<p>I worked it out at a Catan table, of all places. A brick is worth nothing to the player holding four of them and very nearly everything to the player sitting one brick short of a city, and the entire game turns on holding both of those facts at once and knowing which one is true of the person you are trading with. Monopoly taught me the uglier version, which is that a property is worth what the person across from you can be talked into believing it is worth, and that the price printed on the card is mostly a suggestion. And the lunch table taught me the one that actually stuck, because a seat is worth wildly different amounts to different people on different days and the currency was never money, it was who noticed you sat down. I had no language for any of this at eleven. I just kept noticing that the same object changed price depending on who was holding it and what they happened to need that week.</p>

<p>Companies are that, except the board refuses to sit still. A business has a price today that depends on what a buyer believes it will produce in five years, which depends on what customers will want by then, which depends on a competitor&rsquo;s decision that has not been made yet, which depends on capital priced off a rate somebody will set next quarter. It is a puzzle where every piece moves while you are looking at the others, solved in public, by thousands of people at once, with real money on it. I find that genuinely thrilling and I have stopped pretending it is a strange thing to find thrilling.</p>

<p>Which is where the question I actually care about lives. Not what a company earns, because that is arithmetic and anybody can do arithmetic. What it is quietly worth to somebody who has understood it better than its own accounts have. The accounts are the price printed on the card, and the interesting number has never once been on the card.</p>

<p>I saw it most clearly in a supplement aisle, where two businesses selling more or less the same thing to more or less the same person cleared at six times revenue and at barely one within eight weeks of each other, which is not a rounding error so much as an argument about what was actually being bought. Then I ran into it again inside a finance workflow whose saving was real enough to measure in hours and yet had nowhere on a balance sheet to sit.</p>

<p>I should be honest about the route here, because it was not the obvious one. I did not grow up anywhere near this. What I grew up around was a household in which the arithmetic was never abstract, where somebody was awake at the wrong end of the clock so that a number would come out right at the end of the month, and where I learned early to read a room for the thing nobody was saying out loud. Finance turned out to be that same habit pointed at companies rather than at my own kitchen, which is why the question that holds me is not what a business earns but what it is quietly worth to somebody who has understood it better than its accounts have.</p>

<p>It runs in three places that feed one another, so that an argument I make in writing has to survive being sent to people who will reply to it, and both of those in turn have to survive the show, where I go and ask the people it is actually happening to whether any of it resembles their Tuesday.</p>
</div>

<div class="rack">
  <a class="rk" href="#blog">
    <span class="rk__n">[ 01 ]</span>
    <span class="rk__k">The brain dump</span>
    <span class="rk__t">Everything I have not finished thinking about</span>
    <span class="rk__d">The blog. Long pieces with the working left in, the wrong turns included, and the part at the end where I say what would change my mind.</span>
    <span class="rk__m">Two pieces &middot; live</span>
  </a>
  <a class="rk" href="#newsletter">
    <span class="rk__n">[ 02 ]</span>
    <span class="rk__k">The journal</span>
    <span class="rk__t">Entries on whichever deal will not leave me alone</span>
    <span class="rk__d">The newsletter. Not analysis so much as a diary kept in public: one transaction a week, what the buyer was really paying for, and the part of my own reasoning I trust least.</span>
    <span class="rk__m">In progress</span>
  </a>
  <a class="rk" href="#podcast">
    <span class="rk__n">[ 03 ]</span>
    <span class="rk__k">The podcast</span>
    <span class="rk__t">Wall Street&rsquo;s Trojan Horse</span>
    <span class="rk__d">What I think is happening to banking and M&amp;A now that AI is inside the building, told twice over: by the analysts living through it, and by the people who built the thing.</span>
    <span class="rk__m">In progress</span>
  </a>
</div>

<div class="body">
<h2 id="blog">The brain dump</h2>
<p>This is the blog, and I call it a brain dump because that is honestly what it is. None of it is worth anything unless I am willing to put it somewhere a stranger can disagree with me, so the working stays in, including the parts where I changed my mind halfway down. These are the two I would defend line by line.</p>
<div class="biglinks">
  <a href="trend.html"><span class="bl__lg"></span><span class="bl__n">Five Deals, Six Weeks, and a Sevenfold Spread</span><span class="bl__note">Five consumer wellness businesses changed hands this summer at prices seven times apart. The chart, the five notes, and the part where I say what would prove me wrong.</span></a>
  <a href="invisible.html"><span class="bl__lg"></span><span class="bl__n">The Assets AI Builds That Nobody Records</span><span class="bl__note">The essay that came out of the BODi work. The best output of a deployment never lands on the balance sheet.</span></a>
</div>
{dealgrid()}
<p><a href="trend.html"><strong>Read the full argument</strong></a>, including the chart and where I think I am wrong.</p>
<h3>Where the operating work happened</h3>
<div class="biglinks">
  <a href="bodi.html"><span class="bl__lg"><img src="assets/logos/bodi.svg" alt=""></span><span class="bl__n">BODi</span><span class="bl__note">Ninety minutes to three. $784K sized and presented to the MD of Accounting.</span></a>
</div>

<h2 id="newsletter">The journal</h2>
<p>The brain dump is where I take a month over something. The journal is the other half of it, which is a newsletter but mostly a diary I happen to send: entries on whichever deal has refused to leave me alone that week, written whether or not the week has been generous with material.</p>
<p>One transaction. What the buyer was actually paying for, stated plainly enough that somebody could tell me I have it wrong. And then the part most writing on this subject leaves out, which is the weakest link in my own reasoning, named by me before anybody else has to find it. I would rather be corrected in a reply than be right in private.</p>
<p class="quiet">First issues to come. If you would like to be sent them, or you would like to be the person who writes back disagreeing, say so and I will put you on it.</p>

<h2 id="podcast">The podcast</h2>
<div class="podcast">
  <img class="podcast__art" src="assets/logos/podcast-cover.svg" alt="Wall Street&rsquo;s Trojan Horse, placeholder cover">
  <div class="podcast__body">
    <p class="podcast__k">Wall Street&rsquo;s Trojan Horse</p>
    <p>A show about how quietly AI has already walked into investment banking. Not the version in the headlines, with the press releases and the transformation decks. The version where a first-year analyst stops doing four hours of work on a Tuesday and mentions it to nobody.</p>
    <p>I am collecting perspectives from two groups: first-year analysts who are living inside the change, and the people building the tools that caused it. They describe the same event in almost completely different language, and the distance between those two accounts is the actual show.</p>
    <p class="quiet">Artwork and first episodes to come. If you are a first-year analyst, or you build these tools, I would like to record with you.</p>
  </div>
</div>

<h2>What I am looking for</h2>
<p>An analyst seat where the work is genuinely difficult and somebody senior is willing to tell me plainly when I have got something wrong, which is a narrower request than it sounds. The longer ambition, and I am aware how it reads set down in writing, is to use these tools to make investment banking a more human business rather than merely a faster one, on the theory that once the searching becomes cheap the judgement is the only thing left, and judgement has always been the part that needed a person in it.</p>
{ask("If you work in a bank and have watched this happen from the inside, come on the show.")}
</div>
<nav class="nextprev"><a href="trend.html">The deal essay &rarr;</a><a href="index.html">Index</a></nav>
</div>"""

# finance.html is now a redirect. The section lives at https://trojanhorse.blog, and this URL was
# public long enough to be worth forwarding rather than dropping.
(ROOT / "finance.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Finance | Francis Ruan</title>
<meta http-equiv="refresh" content="0; url=https://trojanhorse.blog">
<link rel="canonical" href="https://trojanhorse.blog">
<meta name="robots" content="noindex">
</head>
<body>
<p>The finance writing now lives at <a href="https://trojanhorse.blog">trojanhorse.blog</a>.</p>
<script>location.replace("https://trojanhorse.blog");</script>
</body>
</html>
""", encoding="utf-8")
print("finance.html -> redirect to https://trojanhorse.blog")

# ================================================================= HUBS =====
def hub(fn, eyebrow, title, lede, blocks, active, sub="", band=False):
    """band=True puts the page head in a full-width navy plate above the wrap,
    set in small caps after the wordmark Francis asked this to echo."""
    if 'class="ask"' not in blocks:
        blocks = blocks + ask()
    subline = f'\n  <p class="dedication">{sub}</p>' if sub else ""
    if band:
        head = f"""<header class="band">
  <div class="wrap band__in">
    <p class="band__k">{eyebrow}</p>
    <h1 class="band__t">{title}</h1>{subline}
  </div>
</header>
<div class="wrap">"""
    else:
        head = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{title}</h1>{subline}
</header>"""
    body = head + f"""
<div class="body">
{soundtrack(fn)}
{blocks}
</div>
<nav class="nextprev"><a href="index.html">&larr; All six</a></nav>
</div>"""
    page(fn, title + " | Francis Ruan", lede.replace('"',''), body, active=active)
    print(fn)

def biglinks(items):
    out = ['<div class="biglinks">']
    for href, logo, name, note in items:
        lg = f'<span class="bl__lg"><img src="assets/logos/{logo}" alt=""></span>' if logo else ""
        out.append(f'<a href="{href}">{lg}<span class="bl__n">{name}</span>'
                   f'<span class="bl__note">{note}</span></a>')
    out.append("</div>")
    return "".join(out)

hub("my-why.html", "Why", "For Qiwen Ye",
    "",
    '<div class="videos">'
    '<figure><video controls preload="metadata" playsinline poster="assets/video/mom-1-poster.jpg">'
    '<source src="assets/video/mom-1.mp4" type="video/mp4">Your browser cannot play this video.</video></figure>'
    '<figure><video controls preload="metadata" playsinline poster="assets/video/mom-2-poster.jpg">'
    '<source src="assets/video/mom-2.mp4" type="video/mp4">Your browser cannot play this video.</video></figure>'
    '</div>'

    '<p class="kicker">She comes home a little after seven in the morning smelling faintly of hand '
    'sanitizer, and she will not go to bed until she has asked me at least two questions about my week, '
    'and she holds an unshakeable and entirely evidence-free confidence that both her sons are going to '
    'be fine.</p>'

    '<p>She is sixty-three, she has raised us on her own the entire time, and her friends are mostly in '
    'China, which in practice means her friends are mostly a phone screen at inconvenient hours. There is '
    'a version of all this that turns her into a lesson, and I would rather not write that one, because '
    'she is a person and not a moral.</p>'

    '<figure class="lead"><img src="assets/photos/my-why-title.jpg" '
    'alt="Francis Ruan as a boy with his mother, a mountain behind them" width="1200" height="1527">'
    '</figure>'

    '<h2>The games she missed</h2>'

    '<p>She missed all of them. Every football game. Every concert. The award nights, the banquets, the '
    'ones where they read your name out and you are supposed to look up into the stands and find your '
    'person. I would look up at the row where the other mothers sat, all of them together, and there '
    'would be a gap.</p>'

    '<p>I was angry about that for a while. I am saying so because leaving it out would flatter me. I was '
    'twelve and I thought the gap meant something about how much I was worth.</p>'

    '<p>It took me years to learn what was happening on the other side of it. That she cried about those '
    'nights. That missing them was never a scheduling problem, it was a grief she carried quietly and '
    'deliberately did not hand to us, because handing it to us would have taught us to think of ourselves '
    'as a cost. She would rather have been in that row than anywhere on earth. She went to work instead, '
    'every single time, for years.</p>'

    '<p class="pull">She would rather have been there than anything. That is exactly why she was not.</p>'

    '<p>She also did not have to raise us here. Silicon Valley is an absurd place to be a single nurse with '
    'two boys, where everything costs more than it should. She stayed because '
    'the schools were good. That was the entire calculation. She traded her own comfort for our classrooms '
    'and she has never once described it to me as a trade.</p>'

    '<h2>So here is the arithmetic</h2>'

    '<p>And I do mean arithmetic, because I have actually sat down and done it. Every hour I spend in a '
    'lecture hall is an hour she is standing somewhere under fluorescent light, awake at the wrong end of '
    'the clock, because that is what it costs for me to be sitting down.</p>'

    '<p>People expect that to be guilt. It is not. Guilt is heavy and it makes you slow, and I have watched '
    'it make other people slow. This is closer to the pressure you feel in a starting block, the good kind, '
    'the kind that is mostly just wanting to go. I get to be here. Somebody paid for that in a currency that '
    'does not convert back, and the only sensible response I have found is to be extremely, almost comically '
    'awake.</p>'

    '<h2>The part I have not made peace with</h2>'

    '<p>None of this is past tense. She is sixty-three and she is still on nights. Both her sons are out of '
    'the house. The thing the sacrifice was for has already happened, and she is still paying for it, and '
    'when I sit with that for too long it puts real weight on my chest.</p>'

    '<p>Which is, I suppose, the engine. There is no wall I would not run through for her, and I say that '
    'cheerfully, because having one non-negotiable thing makes every other decision enormously easier.</p>'

    '<h2>I wrote about her once</h2>'

    '<p>A short story about our dinner table. It won <strong>first place in the Young Adult category of the '
    'Palo Alto Weekly&rsquo;s 39th Annual Short Story Contest</strong>, and the judges said something I have '
    'thought about since, which is that it caught the smells and the sounds and the essence of true motherly '
    'love in a few paragraphs. I did not know you could do that with a few paragraphs. I have been trying to '
    'do it again ever since.</p>'

    '<p>It is short, and it is the best thing I have written. If you only have a minute on this site, spend it there.</p>'
    '<p><a href="https://www.paloaltoonline.com/short-story/2025/07/17/short-story-contest-2025-the-dinner-table/" '
    'target="_blank" rel="noopener"><strong>The Dinner Table</strong></a>, Palo Alto Online, July 2025.</p>'
    + ask("If you have a mother who did something like this, I would genuinely like to hear about her."),
    "Why",
    sub="&#25105;&#30340;&#22920;&#22920; &middot; w&#466; de m&#257;ma &middot; my mother", band=True)

LOVES = [
  ("Little Women",        "Greta Gerwig, 2019",     "film", "little-women"),
  ("A River Runs Through It","Robert Redford, 1992","film", "river-runs"),
  ("Pride and Prejudice", "Jane Austen, 1813",      "book", "pride-prejudice"),
  ("Good Will Hunting",   "Gus Van Sant, 1997",     "film", "good-will-hunting"),
  ("Rudy: My Story",      "Rudy Ruettiger, 2012",   "book", "rudy"),
]

def loves():
    """Five objects on a shelf. The artwork does the identifying; the argument for
    why they belong together is made once, underneath, rather than five times."""
    out = ['<div class="loves">']
    for title, credit, kind, slug in LOVES:
        out.append(f'<figure class="love">'
                   f'<span class="love__art"><img src="assets/loves/{slug}.jpg" alt="{title}" loading="lazy"></span>'
                   f'<figcaption class="love__cap">'
                   f'<span class="love__kind">{kind}</span>'
                   f'<span class="love__t">{title}</span>'
                   f'<span class="love__c">{credit}</span>'
                   f'</figcaption></figure>')
    out.append("</div>")
    return "".join(out)

hub("who-am-i.html", "So who is Francis", "So Who Is Francis?",
    "",
    '<p class="kicker">When I was interviewed for a paper after giving my graduation speech, they '
    'asked me to choose a teacher who would speak highly of me. I smiled, and chose the teacher who '
    'seemed least fond of me. My heart smiled when I read her quote.</p>'

    '<figure class="clip">'
    '<p class="clip__lede">Senior Francis Ruan is hard to miss.</p>'
    '<blockquote><p>&ldquo;Francis is an instigator, getting everyone riled up and distracted in a very '
    'enthusiastic way,&rdquo; Trigonometry Honors teacher Jeanne Yu said. &ldquo;He is the kind of '
    'student who gives the teacher a headache while in class, and then the teacher goes home and '
    'secretly laughs about all his antics.&rdquo;</p></blockquote>'
    '</figure>'

    '<figure class="lead lead--i"><img src="assets/photos/i-backpack.jpg" '
    'alt="Francis as a young boy outside school, a lunch box under one arm and a hand on the '
    'handle of a rolling backpack" width="1200" height="1600" loading="lazy"></figure>'

    '<p>I love life. Not in the polished, greeting-card way, but in the full, messy, wide-open way. I '
    'love waking up. I love living.</p>'

    '<p>There have been hard days, more than a few, and there will be many more ahead. I welcome them. '
    'Hard days are how I learned to stand, and every one of them still came with a sunrise. I&rsquo;ve '
    'found that there can be stress without worry. I love working hard, really hard, the kind of hard '
    'that leaves you tired and full at the same time. Pressure is a privilege. It means something '
    'matters.</p>'

    '<p>I am not better than anyone, but no one is better than me. I carry that sentence like a compass. '
    'It keeps me humble enough to listen and steady enough to stand tall in any room. And in every room, '
    'I believe each person has something I can learn. The janitor, the CEO, the quiet kid in the back: '
    'everyone is carrying a story I haven&rsquo;t read yet.</p>'

    '<p>I want to try everything. If I could, I would be everywhere all at once. I never order the same '
    'thing twice at a restaurant, because how could I, when there&rsquo;s a whole menu of lives I '
    'haven&rsquo;t tasted yet? Maybe the next dish is a mistake. Good. Now I have a story.</p>'

    '<p>No matter how old I get, I refuse to lose my childishness. I don&rsquo;t believe in that kind of '
    'growing up. I know the weight of respect, of listening, of showing up with professionalism, and I '
    'hold all of it close. But none of it asks me to give up my imagination, my dumb curiosity, or my '
    'love of being gloriously, unapologetically corny. I love being silly. I love the bad pun, the goofy '
    'dance, the joke that only lands with one person. Life is far too short to take yourself too '
    'seriously, and far too long to spend it without laughing. And I love laughing. The real kind, the '
    'kind that sneaks up from your stomach and won&rsquo;t let you breathe.</p>'

    '<p class="pull">I believe the grass is greener wherever it is I step. Not because the ground is '
    'perfect, but because I&rsquo;ve decided to tend it.</p>'

    '<p>I love people. I love loving. Some call me a pushover, and maybe they&rsquo;re right. But on my '
    'deathbed, I will smile knowing that I cared, that I gave, that I chose an open hand over a closed '
    'fist every time I could. I&rsquo;d rather be fooled now and then than live guarded forever.</p>'

    '<p>I love learning about almost everything. The history of moustaches. The terracotta army standing '
    'silent for two thousand years. The origins of tangerines. Why avocados have pits at all. The world '
    'is a library with no closing time, and I want to wander every aisle.</p>'

    '<p>I love learning about longevity, about taking care of the body and mind I&rsquo;ve been given. I '
    'love working out, pushing myself past the edges of what people think I can be. Every rep is a quiet '
    'conversation with the version of me I haven&rsquo;t met yet, and I&rsquo;m always excited to meet '
    'him.</p>'

    '<p>I want to be whole and then some. Not finished, never finished, but full. Full of wonder, full '
    'of gratitude, full of the stubborn belief that tomorrow could be the best day yet.</p>'

    '<p>So here I am. Curious, corny, hungry, hopeful.</p>'

    '<p class="finis">Wildly, wonderfully alive.</p>'

    '<div class="coda">'
    '<div class="videos videos--one videos--portrait">'
    '<figure><video controls playsinline preload="metadata" src="assets/video/i-portrait.mp4">'
    'Your browser cannot play this video.</video></figure>'
    '</div>'
    '<div class="gallery">'
    '<figure><img src="assets/photos/i-court.jpg" alt="Two boys on a school blacktop, Francis mid-gesture" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/i-green.jpg" alt="Francis as a boy in a green shirt on the schoolyard" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/i-boss.jpg" alt="Francis as a boy on a tiled porch with both arms flung wide" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/i-hill.jpg" alt="Friends messing about on a grass hill under an open blue sky" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/i-suits-1.jpg" alt="Francis with two friends in suits at night" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/i-suits-2.jpg" alt="Francis in a pink tie between two friends in suits" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/i-sunset.jpg" alt="Francis with both arms out beside a lamppost at sunset, a stone building behind him" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/i-beach.jpg" alt="Francis being carried by three friends on a beach" loading="lazy" width="900" height="900"></figure>'
    '</div>'
    '</div>'

    + ask("If you have made it this far you may as well introduce yourself."),
    "I", band=True)

hub("fight-on.html", "Fight On", "What &ldquo;Fight On&rdquo; Means to Me",
    "",
    '<figure class="lead"><img src="assets/photos/fight-on.jpg" '
    'alt="Francis Ruan as a young boy, grinning, holding up a peace sign" width="1200" height="1600">'
    '<figcaption>Roughly the era in question.</figcaption></figure>'

    '<p class="kicker">The bell went at three, and for about ten minutes the front of that school was the '
    'busiest place in the world.</p>'

    '<p>Cars curled around the loop with their engines running. Somebody&rsquo;s dad always had the window '
    'down. Somebody&rsquo;s mum always had a snack ready in the passenger seat, which I thought was the '
    'most extraordinary act of forethought I had ever witnessed. Then the loop was empty, the engines were '
    'gone, and what was left was a very large campus, a low sun, and me.</p>'

    '<p>My mother was a nurse, and her shift did not end when other people&rsquo;s did. So I had six hours, '
    'no phone, and an entire school to myself.</p>'

    '<p>I learned that place the way you learn a house in the dark. I knew which trees held weight and '
    'which ones dropped you. I knew the patch of concrete behind the cafeteria that stayed warm until five '
    'and took chalk well. I drew on it for years, rain took all of it, and I drew again. Mostly the same '
    'three things: a stadium, a house with far too many windows, and a car, always with two people in '
    'it.</p>'

    '<p class="pull">The six hours were never the hard part. A boy in a tree with an entire school to '
    'himself is closer to a king than a castaway.</p>'

    '<p>The hard part was nine o&rsquo;clock, when the headlights finally came around the loop, and I got '
    'in the car and saw her face and understood immediately that her day had been worse than mine.</p>'

    '<p>So I made a decision in that passenger seat that I have never unmade. Her day would not get any '
    'heavier because of me. I would be the easy part. I never mentioned the six hours. I told her something '
    'funny from recess, and if nothing funny had happened, I made something up. Then I watched her laugh on '
    'the drive home, and that felt like winning.</p>'

    '<p>That decision went everywhere with me after that.</p>'

    '<h2>At Ranch 99</h2>'
    '<p>It went with me to the grocery store, where a child does a particular arithmetic once he knows the '
    'family condition. You do not ask. That is the entire skill. You see the thing, you picture that nine '
    'o&rsquo;clock look on your mother&rsquo;s face, and you keep walking. Above all, you do not make it a '
    'moment.</p>'
    '<p>But not asking for things is only half of it. The other half is going and getting them '
    'yourself.</p>'

    '<h2>In the classroom</h2>'
    '<p>My English arrived late, so every summer of elementary school I went back to summer school to '
    'relearn what I had not held the first time. I never thought of it as punishment. I thought of it as '
    'another lap.</p>'
    '<p>In middle school I was not placed in the advanced math class. So I asked. Then I asked again. Then '
    'I walked to my teacher&rsquo;s door and knocked on it myself, a small, stubborn kid with nothing to '
    'offer but a promise that nobody in that room would outwork me.</p>'
    '<p>I was never the boy who simply knew. I was the boy who went back, found exactly where my '
    'understanding broke, and fixed it. Knowing things quickly runs out eventually. Refusing to leave never '
    'does.</p>'

    '<h2>On the field</h2>'
    '<p>I was the fat kid, picked last so often it stopped feeling like an event and started feeling like a '
    'forecast. I picked up a lacrosse stick for the first time at a tryout, in front of boys who had held '
    'one since they were eight, and I know the exact sound a group makes watching you fail at something '
    'easy.</p>'

    '<p class="pull">I came back the next day anyway.</p>'

    '<p>First one out, last one in. Diving for balls nobody else would chase. Knocked down by boys who were '
    'bigger, faster and six years ahead, and getting up smiling, every time, until getting knocked down '
    'stopped meaning anything at all.</p>'
    '<p>Those boys were not gifted. They were early. I had been comparing my first week to their sixth '
    'year. So I wrote down what beat me and trained only that. I was once laughed at for how badly I played '
    'spikeball. Today I am the best spikeball player I know. I was never handed talent. I just refused, '
    'very cheerfully and for a very long time, to go home.</p>'

    '<h2>With people</h2>'
    '<p>The third place I refused to quit was people. If you are going to be the worst athlete on the '
    'field, you had better be the warmest person on it. I learned to find what makes a room laugh, and to '
    'find it fast, especially for whoever was having a worse day than me. It is what I did in that car at '
    'nine o&rsquo;clock, and I have never stopped.</p>'
    '<p>Some people will mistake a soft heart for a weak one. I have loved people who did not love me back '
    'the same way, and I have never once regretted loving first. I would rather keep my heart open and '
    'bruised than closed, safe, and small.</p>'

    '<h2>And then I got to USC</h2>'
    '<p>And found they had made a slogan out of it. Fight On, on every wall and every shirt.</p>'
    '<p>To me it was never a cheer. It means nine o&rsquo;clock in an empty school loop and getting in the '
    'car smiling anyway. It means nobody is coming to make this easier, and you go anyway, and you go '
    'cheerfully, because bitterness is heavy and I never had room to carry it.</p>'
    '<p>I did not learn to fight on at USC. I learned it on warm concrete behind a cafeteria, with a piece '
    'of chalk and nobody watching. USC just gave me the words.</p>'

    '<p class="finis">I am not the victim of this story. I am the reason it has a good ending.</p>'

    + ask("If any of that landed, I would genuinely like to hear from you."),
    "Fight On", band=True)

hub("leadership.html", "Stewardship", "Keeper of the House",
    "",
    '<figure class="defn defn--two">'
    '<div class="defn__pair">'
    '<div class="defn__one"><p class="defn__w">leader</p>'
    '<p class="defn__src">Old English <em>l&aelig;dan</em>, to go before, to show the way. '
    'A word about position. The leader is in front.</p></div>'
    '<div class="defn__one"><p class="defn__w">steward</p>'
    '<p class="defn__src">Old English <em>st&#299;weard</em>, from <em>stig</em>, a hall or '
    'a house, and <em>weard</em>, a keeper. The one who keeps the house.</p></div>'
    '</div></figure>'

    '<p class="kicker">I want the second word. Position is a fact about where you are '
    'standing in a room. Responsibility is a fact about what stops working if you walk out '
    'of it. I have been more useful holding the second one.</p>'

    '<p>A steward is the roommate who washes the dishes. He books the place, works out who '
    'is free which weekend, and sends the third message to the two people who still have '
    'not replied.</p>'

    '<p>I do all of that and I like doing it. The part I care about is doing it without '
    'keeping a tally. I have watched people handle every detail of a trip and then spend '
    'the drive home listing what they handled. The list is the failure. It arrives late and '
    'it arrives in front of everybody.</p>'

    '<p>Three places taught me most of this.</p>'

    '<h2>Sports</h2>'

    '<p>Everyone on that football field was bigger than me, including the kicker. I checked. '
    'Freshman year I had never played a down and I was the worst player in the programme, '
    'which my friends confirmed at the time and still bring up.</p>'

    '<p>That hurt for about two years, in a small way, every afternoon at practice.</p>'

    '<p>Then I stopped watching the ball. I cannot name the day it happened. A player out '
    'there is looking at his assignment, the man across from him, and the next two seconds, '
    'which is exactly what he should be looking at. Somebody has to watch the rest of it, '
    'and that is usually whoever has the time. I had the time.</p>'

    '<p>Four years of football, three on varsity, a stretch as captain. Track. Lacrosse at '
    'USC now, and alumni chair. I was a mediocre athlete through all of it. What I took from '
    'it is that a team runs a second job underneath the first one and nobody is assigned to '
    'it.</p>'

    '<h2>Student government</h2>'

    '<p>I was student body president for four terms and I gave the commencement speech. '
    'Those are the two lines that fit on a page.</p>'

    '<p>The job was logistics. Finding out which room was free. Asking the teacher who '
    'controls that room. Remembering that the custodians have to know before you move two '
    'hundred chairs. Chasing a sign-up sheet for a week. Standing in a hallway at seven in '
    'the morning so that something could start at eight.</p>'

    '<p>An election gives you a title and nothing else. The rest comes slowly, from people '
    'deciding on their own that when you say a thing is handled it is handled. I never found '
    'a shortcut to that, and I stopped looking for one.</p>'

    '<h2>Relationships</h2>'

    '<p>My mother gave me rules and did not present them as optional. Buy flowers when there '
    'is no occasion, because an occasion is only a permission slip. Say the compliment out '
    'loud instead of thinking it warmly and assuming it arrived. Never go to bed upset, '
    'however late that makes the night. Open the door, every time, for the rest of your '
    'life.</p>'

    '<p>I send one person a real compliment every day. Specific, unprompted, to somebody who '
    'was not expecting anything from me that morning. It takes about eleven seconds.</p>'

    '<p>The harder rule is the one about going wrong. Sit down and work out how much of it '
    'is yours. It usually is, partly. It is almost never only yours, which is why the word '
    'is we. Take the accountability past the point where taking it still feels good about '
    'yourself, and then keep going a little further.</p>'

    '<p>I have loved people who did not love me back the same way. Some people call that a '
    'weakness. They may be right, and I would do it again.</p>'

    + ask("If you want somebody to handle the logistics, I am genuinely the person for it."),
    "Stewardship", band=True)

hub("fun.html", "Effervescent", "The Unserious Half",
    "",
    '<figure class="lead"><img src="assets/photos/origin-fun.jpg" '
    'alt="Francis Ruan as a small boy in a ninja costume with his older brother" width="900" height="900">'
    '<figcaption>No occasion. That was the point.</figcaption></figure>'

    '<p class="kicker">I have never really grown out of this. The costume changed and the sword got '
    'confiscated, but the operating principle has held.</p>'

    '<h2>Most of life is Tuesday</h2>'

    '<p>Not the bad Tuesday. The ordinary one, where nothing is wrong and nothing is interesting either '
    'and you have somewhere to be at ten. Nobody warns you what the ratio is going to be. The '
    'extraordinary days are real and they are rare, and a life built to work only on those is switched '
    'off almost all of the time.</p>'

    '<p>So I have spent a while thinking about crumbs.</p>'

    '<p>Take every small good thing out of one unremarkable day. The first sip while it is still too hot. '
    'The song that arrives at exactly the right moment. The dog you were not expecting. Save them the way '
    'you would save crumbs, and by the end of a year you have a meal. Probably several. Nobody has one '
    'enormous meal a year. That is not how eating works and I do not think it is how living works '
    'either.</p>'

    '<h2>The accounting version</h2>'

    '<p>Here is the version I actually believe, in the only vocabulary I have, which is unfortunately '
    'finance.</p>'

    '<p>Most people try to raise their happiness by increasing revenue. Bigger wins, better news, more of '
    'everything. That works briefly, it is expensive, and almost none of the revenue line is up to '
    'you.</p>'

    '<p>The other side of the statement is entirely up to you. Happiness has operating expenses. The '
    'grudge you are still carrying. The comparison you keep running. The thing you have not said to '
    'somebody. The room you will not clean. Every one of those drains the account daily, quietly, '
    'whether or not anything good happens to you.</p>'

    '<p>Take the costs out and the arithmetic changes. If your expenses sit near zero, any revenue at all '
    'leaves you positive. You do not need a good day. You need a day with nothing subtracting from it, '
    'and then the crumbs are enough on their own.</p>'

    '<p class="pull">Profit does not have to clear the bar for happiness. It only has to be greater than '
    'zero, and greater than zero is contentment, and contentment is available on a Tuesday.</p>'

    '<p>A house of contentment is built by removing things rather than acquiring them, and it stands up '
    'in weather that joy does not.</p>'

    '<h2>Collected on purpose</h2>'

    '<p>I take an unreasonable number of selfies for nobody in particular. I film short videos of '
    'completely ordinary afternoons, because a year from now the ordinary afternoon is the thing I will '
    'want back and it is the only thing nobody thinks to record.</p>'

    '<p>I talk to myself constantly, out loud, and I tell myself jokes, and I find them funny. This is '
    'either a warning sign or the cheapest entertainment ever devised and I have made my decision about '
    'which.</p>'

    '<p>And once a day I send somebody a real compliment. Specific, unprompted, to somebody who was not '
    'expecting anything from me that morning. This is not selfless. Watching a genuine compliment land, '
    'the small recalibration, the way somebody holds themselves differently for the next minute, is '
    'unmatched by anything I can buy. It costs nothing, it takes about eleven seconds, and I have never '
    'once regretted sending one.</p>'

    '<h2>Why I am always trying to make you laugh</h2>'

    '<p>People read the jokes as confidence. They did not start that way. They started as a door I could '
    'get through. When you are the smallest boy on the field and the worst one on it and still working '
    'out the language, there are not many currencies available to you.</p>'

    '<p class="pull">Nobody has ever asked whether I was qualified to be funny. They laughed or they did '
    'not, and the transaction settled instantly.</p>'

    '<p>So I got fast at it, and specifically under pressure. I am nervous more often than anybody '
    'watching would guess. The only difference is that my nerves come out as a joke instead of as '
    'silence, and a laugh is a genuinely useful thing to do with adrenaline. It lets the air out of a '
    'room that was holding its breath. It tells everybody else present that they are permitted to be '
    'human here.</p>'

    '<p>And if somebody is having a worse day than me, I want to find the thing that fixes it, fast. '
    'Failing at that is cheap. The joke lands flat, everybody moves on, and the only casualty is a small '
    'piece of my dignity, which I stopped guarding at around nine and have not missed since.</p>'

    '<h2>The rest of the inventory</h2>'

    '<p>I surf El Porto most mornings before class and teach lessons there on weekends. Training for the '
    'Santa Cruz Half Ironman, racing HYROX in Anaheim in December, lacrosse at USC, ran track, '
    '<a href="leadership.html">four years of football</a>. None of which explains why the best hours of '
    'any summer are on a lake with a rope in your hand and no plan at all.</p>'

    '<p>I invent recipes and make my friends eat the failed ones. I hold strong and unwelcome positions '
    'on bulgogi, on grilled cheese, and on the correct Arnold Palmer ratio, which is more lemonade than '
    'anyone will admit.</p>'

    '<p>Stand-up. Small films with no audience. A journal nobody has read. And I will put my face through '
    'any hole in any painted board I encounter, without hesitation, every single time. There has never '
    'needed to be a line.</p>'

    '<p>I also read pathology and nutrition research for fun, which is a strange thing to put in the fun '
    'section, and I am leaving it here anyway.</p>'

    '<h2>The people, mostly</h2>'

    '<p>Almost none of the above is really the point. The point is who is standing next to you while it '
    'happens, which is the sort of thing you are supposed to work out much later than I did.</p>'

    '<div class="coda"><div class="gallery">'
    '<figure><img src="assets/photos/sq/fun-corridor.jpg" alt="Friends sitting along a corridor, laughing at something on a phone" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-dorm.jpg" alt="A room full of friends, one playing guitar" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-couch.jpg" alt="Friends crowded onto a couch" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-hallway.jpg" alt="Friends in a hallway" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-indoors-group.jpg" alt="A group of friends dressed up indoors" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-dinner.jpg" alt="A long table of friends at the end of a dinner" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-two-friends.jpg" alt="Francis Ruan and a friend close to the camera, both grinning" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-cutout.jpg" alt="Francis Ruan and a friend behind a painted carnival cutout" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-river.jpg" alt="Francis Ruan tubing the Salt River with friends" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-boat.jpg" alt="Francis Ruan on a boat with an arm raised" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-lake-boat.jpg" alt="Friends crowded into the back of a boat on a lake" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/surf.jpg" alt="Francis Ruan riding a board behind a boat" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-wave.jpg" alt="A surfer riding a grey winter wave" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-wetsuits.jpg" alt="Two friends in wetsuits beside a car loaded with boards" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-boards-four.jpg" alt="Four friends standing behind surfboards on the sand" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-tower-boards.jpg" alt="Friends with boards in front of a lifeguard tower" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-tower.jpg" alt="Friends climbing a lifeguard tower" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-sand-ball.jpg" alt="Two friends playing on the sand at the water line" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-throw-beach.jpg" alt="Throwing a football on the beach" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-rock-group.jpg" alt="A group of friends standing on a rock above the water" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-zbot-group.jpg" alt="A large group of friends in suits outside a house at night" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-friends-night.jpg" alt="Four friends posing on a rooftop at night" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-venue.jpg" alt="Friends in white shirts at an outdoor venue" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-parking-friends.jpg" alt="Three friends in suits at the end of a night" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-trio-suits.jpg" alt="Francis Ruan between two friends, all three laughing" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-dock-night.jpg" alt="A line of friends standing on a platform at night" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-campfire.jpg" alt="Friends around a fire after dark" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-tiles-jump.jpg" alt="Francis Ruan and a friend jumping in front of a tiled wall" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-overlook.jpg" alt="A group of friends on a headland above the ocean" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-harbour-two.jpg" alt="Francis Ruan and a friend by the water at sunset" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-runners-sunset.jpg" alt="Two figures running a ridge at sunset" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-throw-dusk.jpg" alt="Throwing something into the dark at dusk" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-trail.jpg" alt="Two silhouettes on a trail at sunset" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-ridge.jpg" alt="A lone figure walking a coastal ridge" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-dusk-silhouettes.jpg" alt="Silhouettes on a beach after the sun has gone" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-beach-sunset.jpg" alt="Francis Ruan on the coast at dusk with both arms raised" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-parasail.jpg" alt="A parasail over the water off a coastline" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-yard.jpg" alt="Friends messing about under trees in a yard" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-prague.jpg" alt="Francis Ruan and a friend on a bridge in Prague at sunset" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-berlin.jpg" alt="A group of friends in front of a painted wall" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/fun-catalina.jpg" alt="Francis Ruan and a friend at a harbour in Catalina" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/football-team.jpg" alt="Los Altos football team with helmets raised" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/lacrosse-team.jpg" alt="USC men&rsquo;s lacrosse team" loading="lazy" width="900" height="900"></figure>'
    '<figure><img src="assets/photos/sq/barbershop.jpg" alt="Francis Ruan as a small boy in a barber chair, unconvinced" loading="lazy" width="900" height="900"></figure>'
    '</div></div>'

    + ask("If you want to be in one of these photographs at some point, that is arranged by email."),
    "Effervescent", band=True)



# ========================================================= TROJAN HORSE ====
# The blog's own front page. Five deals, short form, one habit: read the
# structure before the headline. Every figure here is from an announcement,
# a filing or named trade press, and the sources list says which.
TROJAN = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">Trojan Horse / Consumer M&amp;A</p>
  <h1>Trojan Horse</h1>
  <p class="meta"><span>Founder and author</span><span>Los Angeles</span><span>September 2026</span></p>
</header>
<div class="body">
{soundtrack("trojan-horse.html")}
<p class="kicker">Five consumer deals from this year. Every one of them was reported as a single number, and in every one the number is describing something other than the asset. That gap is the entire reason this blog exists.</p>

{rows([
 ("Unilever / Gr&uuml;ns, June 2026", "~$1.2bn, reported against 80% of the shares"),
 ("Danone / Huel, March 2026", "~&pound;860m for a brand with 59% gross margin and 8% EBITDA"),
 ("L Catterton / Good Culture, January 2026", "&gt;$500m, about 2x revenue, from the seller of Thorne at 5.8x"),
 ("Kimberly-Clark / Kenvue, closing H2 2026", "$48.7bn, of which about $6.7bn is cash"),
 ("Infinite Epigenetics / Tally Health, April 2026", "Undisclosed, and the asset is a dataset"),
], cap="Announcement terms. Sources at the foot of the page.")}

<h2>Unilever and Gr&uuml;ns, or why the quoted multiple is wrong</h2>

<p>Unilever completed its acquisition of Gr&uuml;ns on 1 June 2026. Gr&uuml;ns is a greens gummy brand founded in 2023 that reached roughly $300m of revenue in under four years, was profitable inside fourteen months, and sells mostly on subscription.</p>

<p>Almost every write-up ran the same arithmetic. $1.2bn on $300m of revenue, so four times sales. Trade reporting puts that consideration against 80% of the shares, not the whole company. If that is right, the implied whole-company value is closer to $1.5bn and the multiple is nearer five times, not four. A full turn of revenue is not a rounding error. It is the distance between a bolt-on price and a growth price.</p>

<p>I could not confirm the split in Unilever's own half-year 6-K, which notes the completion and not the terms. So I am flagging it rather than banking it.</p>

<p class="pull">Leaving a fifth of the company outstanding is not thrift. It is a retention device.</p>

<p>Unilever is buying a founder-run subscription machine three years old. The unpurchased 20% is the thing that keeps the founder in the building, and it is a deal term doing more work than the headline.</p>

<h2>Danone and Huel, a food company that is really a customer acquisition company</h2>

<p>Announced March 2026, cleared by the CMA in August, around &pound;860m. The numbers underneath are the interesting part. Huel did &pound;214m of revenue in FY2024 at a 59% gross margin, and &pound;18.2m of adjusted EBITDA. Revenue reached &pound;250m in FY2025, up 16%.</p>

<p>Run it. A 59% margin on &pound;214m is about &pound;126m of gross profit. EBITDA landed at &pound;18.2m. So roughly &pound;108m, close to half of all revenue, goes out below the gross line. In a direct-to-consumer subscription business, that is overwhelmingly the cost of finding the next customer.</p>

<p>Huel is not expensive to make. It is expensive to sell.</p>

<p>That is also the synergy case, and it is a real one rather than a slide. Danone owns shelf space. Pushing Huel into retail swaps paid acquisition for distribution Danone already has. Which gives a test that does not need a model: watch whether EBITDA margin climbs from 8% toward the gross margin. If it has not moved in three years, Danone bought revenue at a food multiple and inherited the marketing bill with it.</p>

<h2>L Catterton, twice, in the same year</h2>

<p>In January 2026, L Catterton took a majority of Good Culture, the cottage cheese brand, at a reported value above $500m. Good Culture did about $100m of revenue in 2023, close to double that in 2024, and was tracking near $250m in 2025. Call the entry about two times sales.</p>

<p>In August, the same sponsor sold Thorne to P&amp;G at a reported $3.8bn, roughly 5.8 times forward revenue. I wrote that one up <a href="thorne.html">separately</a>.</p>

<p>Same firm, same year, same broad bet that people are buying health. Buying at two and selling at six.</p>

<p>The spread is not explained by growth, because Good Culture roughly doubled. It is explained by whether the product can be copied. Cottage cheese is a refrigerated commodity with a cold chain, a short shelf life and a private label version sitting on the same shelf. Thorne had a practitioner willing to say the name out loud to a patient.</p>

<p class="pull">The multiple is the answer to one question. Can somebody make this for less, and would anyone notice.</p>

<h2>Kimberly-Clark and Kenvue, where $48.7bn was never a price</h2>

<p>Announced October 2025, approved by both shareholder bases, expected to close in the second half of 2026. Kenvue holders receive $3.50 in cash plus 0.14625 Kimberly-Clark shares for each share held, called $21.01 per share at announcement. That is roughly 280m new Kimberly-Clark shares and about $6.7bn of cash.</p>

<p>So about $6.7bn of a $48.7bn headline is money. The rest is Kimberly-Clark stock.</p>

<p>A stock-funded number is a snapshot, not a price. The $21.01 and the $48.7bn were both true on one day in October 2025, at one Kimberly-Clark share price. Every trading day between then and closing, the real consideration moved, and none of that movement had anything to do with Kenvue.</p>

<p>Anyone dropping $48.7bn into an EV/Revenue comparison is quoting a stale price for Kimberly-Clark and calling it a valuation of Kenvue. It is the cheapest error to avoid in this entire aisle, and I still see it in print most weeks.</p>

<h2>Infinite Epigenetics and Tally Health, where the asset is the scoreboard</h2>

<p>On 29 April 2026, Infinite Epigenetics acquired Tally Health in an asset purchase. Terms were not disclosed. Tally was co-founded in 2023 by David Sinclair and pairs epigenetic biological age testing with supplements. The buyer also owns TruDiagnostic and describes holding among the largest private adult DNA methylation datasets. Tally continues as a standalone brand.</p>

<p>Read what actually changed hands. Not a supplement line. A methylation dataset, and a competing clock.</p>

<p>Biological age is not a measurement in the way height is a measurement. It is a model, and somebody has to decide what counts as a year. If you already hold the largest reference dataset and you buy the most consumer-visible rival clock, you have not added a product. You have consolidated the benchmark that every longevity intervention eventually has to validate against, including the supplements sold by the buyers in all four deals above.</p>

<p>No price was disclosed, so I am not going to invent a multiple for you. The thing I will watch is narrow and checkable: whether Tally's test keeps reporting on its own clock, or quietly migrates onto TruDiagnostic's.</p>

<h2>What actually ties these together</h2>

<p>Five deals, five headline numbers, and in every case the number is pointing at something other than the asset. Four fifths of a company reported as a whole one. A food margin that is really an advertising budget. A two times entry and a six times exit from the same sponsor. A price denominated in the buyer's own stock. A supplement brand bought for its database.</p>

<p>The habit I am trying to build is unglamorous. Read the structure before the headline. What percentage changed hands. What currency it was paid in. What sits in the gap between gross margin and EBITDA. What was left undisclosed, and who that silence benefits.</p>

<h2>Where I would be wrong</h2>

<p>Most of the above leans on announcement language and trade press rather than completed purchase accounting, and that is a real limitation rather than a disclaimer. Until Unilever and Kimberly-Clark publish their allocations, the split between goodwill and identifiable intangibles is unknown, and that split is where a buyer's actual view shows up. A large allocation to goodwill says they paid for a business. A large allocation to brand and customer relationships says they paid for something they were willing to name and amortise.</p>

<p>There is also a decent chance I am reading a financing cycle as a structural shift, which is the standard error in this kind of writing, and I would rather name it than have it named for me. A closed IPO window pushes sponsors toward strategic exits no matter what anybody believes about protein or longevity.</p>

<p>I will come back and correct these when the filings land. The corrections are the interesting part.</p>

<h3>Sources</h3>
{ul([
 'Unilever PLC, Form 6-K, half-year results to 30 June 2026, SEC EDGAR, confirming completion of the Gr&uuml;ns acquisition in June 2026.',
 'BeautyMatter and Fitt Insider on the Gr&uuml;ns consideration, stake and revenue scale, June 2026.',
 'DairyReporter, CMA clearance of the Danone and Huel transaction at approximately &pound;860m, 20 August 2026, and the March 2026 announcement coverage.',
 'Sacra and NutraIngredients on Huel FY2024 and FY2025 revenue, gross margin and adjusted EBITDA.',
 'PR Newswire, Good Culture announces majority investment from L Catterton, January 2026, with valuation and revenue scale per DairyReporter and Food Dive.',
 'Kenvue Inc. investor relations, Kimberly-Clark to acquire Kenvue, October 2025, for per-share consideration and mix; Kimberly-Clark Form 8-K and shareholder approval releases.',
 'PR Newswire and NutraIngredients, Infinite Epigenetics acquires Tally Health, 29 April 2026.',
 'P&amp;G and Thorne figures as set out in my <a href="thorne.html">deal note</a>.',
])}
{ask("If you cover consumer and think I have one of these backwards, that is the email I most want to get.")}
</div>

<nav class="nextprev"><a href="trend.html">The five supplement deals &rarr;</a><a href="index.html">Index</a></nav>
</div>"""

page("trojan-horse.html","Trojan Horse | Francis Ruan",
     "Five consumer deals from 2026, each reported as one number that describes something other than the asset. Read the structure before the headline.",
     TROJAN)
print("trojan-horse.html")

# ================================================================= 404 ======
# GitHub Pages serves this file for any unmatched path, including deep ones like
# /a/b/c. Relative URLs would resolve against that phantom directory and 404 in
# turn, so every link and asset reference here is root-absolute on purpose.
NOTFOUND = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>Not Found | Francis Ruan</title>
<meta name="robots" content="noindex">
{ICON}
{FONT}
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar"><div class="wrap topbar__in">
<a class="topbar__name" href="/">Francis Ruan</a>
<ul><li><a href="/">Index</a></li><li><a href="/my-why.html">My Why</a></li>
<li><a href="/curiosity.html">Inquisitive</a></li><li><a href="/who-am-i.html">Who am I</a></li></ul>
</div></header>
<main id="main">
<div class="wrap">
<header class="phead">
  <p class="eyebrow">404</p>
  <h1>There Is Nothing At This Address</h1>
</header>
<div class="body">
<p class="kicker">A page that does not exist, which is at least honest about it.</p>
<p>The link was probably mistyped, or it pointed at something I have since renamed.
Either way the way back is <a href="/">the index</a>, where all nine sections are on
one belt you can push sideways.</p>
<p>If you got here from a link somewhere else and think it should work,
<a href="mailto:fyruan@usc.edu">tell me</a> and I will fix it.</p>
</div>
</div>
</main>
<footer class="foot"><div class="wrap foot__in">
<span>Francis Ruan &middot; USC Marshall &amp; Viterbi, Class of 2029 &middot; Los Angeles</span>
<span><a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a></span></div></footer>
</body>
</html>
"""
(ROOT / "404.html").write_text(NOTFOUND, encoding="utf-8")
print("404.html")
