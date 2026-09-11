#!/usr/bin/env python3
"""Emit every page from one shared chrome. One typeface, pure white, charcoal."""
import pathlib, math
ROOT = pathlib.Path(__file__).parent

# Canonical origin. Open Graph and canonical tags need absolute URLs; relative ones
# do not resolve when a link is unfurled by LinkedIn, iMessage, Slack.
SITE = "https://francisruan.com"

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,500;1,6..72,600&family=Inter:wght@400;500;800&display=swap" rel="stylesheet">')

ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 100 100'><text y='.9em' font-size='90' font-family='Newsreader,Georgia,serif' fill='%231C1C1C'>F</text></svg>\">")

def topbar(active=""):
    items=[("index.html","Index"),("my-why.html","Why"),("who-am-i.html","I"),
           ("fight-on.html","Fight On"),("curiosity.html","Curiosity"),
           ("leadership.html","Leadership"),("finance.html","Finance"),
           ("building.html","Engineer"),("awards.html","Lucky"),
           ("fun.html","Fun"),("Ruan_Francis_Resume.pdf","Resume")]
    li="".join(f'<li><a href="{h}"{" target=_blank rel=noopener" if h.endswith(".pdf") else ""}'
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
  ("who-am-i-wide.jpg",        "I",                       "who-am-i.html"),
  ("fight-on-sq.jpg",          "Fight On",                "fight-on.html"),
  ("origin-curiosity.jpg",     "Curiosity",               "curiosity.html"),
  ("origin-leadership.jpg",    "Leadership",              "leadership.html"),
  ("origin-relationships.jpg", "Finance",                 "finance.html"),
  ("origin-engineer.jpg",      "Engineer",                "building.html"),
  ("awards.jpg",               "Lucky",                   "awards.html"),
  ("origin-fun.jpg",           "The Art Of Having Fun",   "fun.html"),
]

PIECES = [
  ("fun.html",
   "Most people run happiness off the top line. Bigger wins, better news, more of everything, and almost "
   "none of that line is theirs to control. The cost side is. The grudge, the comparison, the thing left "
   "unsaid, the room you will not clean, every one of them a fixed cost accruing against you daily whether "
   "or not the day delivers. Drive the costs near zero and the smallest revenue clears. You do not need a "
   "good day. You need a day with nothing subtracting from it."),
  ("fun.html",
   "I am nervous more often than anybody watching would guess. My nerves come out as a joke rather than as "
   "silence, and I have stopped apologising for that, because a laugh is a genuinely useful thing to do "
   "with adrenaline. It lets the air out of a room that was holding its breath, and tells everybody "
   "present that they are permitted to be human here."),
  ("awards.html",
   "False modesty is only bragging with better manners."),
]

def pieces_box():
    """A small collection on the cover, kept between the marks and the contact
    line. Numbered in brackets like everything else on this page."""
    out = ['<div class="pieces"><p class="pieces__k">[ Small pieces ]</p><ol class="pieces__l">']
    for i, (href, text) in enumerate(PIECES, 1):
        out.append(f'<li class="pieces__i"><a href="{href}">'
                   f'<span class="pieces__n">{i:02d}</span>'
                   f'<span class="pieces__t">{text}</span></a></li>')
    out.append('</ol></div>')
    return "".join(out)

TRACKS = {
  # page                track                artist            sleeve
  "my-why.html":    ("Cool",              "Daniel Caesar",   "my-why"),
  "fight-on.html":  ("Hold On",           "Alabama Shakes",  "fight-on"),
  "leadership.html":("Ivy",               "Frank Ocean",     "leadership"),
  "finance.html":   ("Cantaloupe Island", "Herbie Hancock",  "finance"),
  "curiosity.html": ("Lujon",             "Henry Mancini",   "curiosity"),
  "building.html":  ("Electric Feel",     "MGMT",            "building"),
  "awards.html":    ("Golden",            "Harry Styles",    "awards"),
  "fun.html":       ("Sundown",           "LEISURE",         "fun"),
  "who-am-i.html":  ("Orange Blood",      "Mt Joy",          "who-am-i"),
  "trend.html":     ("Cantaloupe Island", "Herbie Hancock",  "finance"),
  "invisible.html": ("Lujon",             "Henry Mancini",   "curiosity"),
}

def soundtrack(fn):
    """The sleeve and the title, small, in the top right corner of the page. No
    instruction to the reader and no musical note; a record cover is legible on
    its own and does not need to be captioned."""
    t = TRACKS.get(fn)
    if not t: return ""
    title, artist, sleeve = t
    from urllib.parse import quote
    q = quote(f"{title} {artist}")
    return ('<div class="track">'
            f'<a class="track__l" href="https://open.spotify.com/search/{q}" target="_blank" rel="noopener">'
            f'<img class="track__art" src="assets/tracks/{sleeve}.jpg" alt="" loading="lazy" width="300" height="300">'
            '<span class="track__meta">'
            f'<span class="track__t">{title}</span>'
            f'<span class="track__a">{artist}</span>'
            '</span></a></div>')

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
    belt is driven by a scroll-linked animation, so it too runs without JavaScript
    and simply rests on 01 in browsers that do not support one."""
    rows = []
    n = len(PYRAMID)
    for i, (fname, label, href) in enumerate(PYRAMID, 1):
        pth = ROOT / "assets" / "photos" / fname
        img = f'<img src="assets/photos/{fname}" alt="" loading="lazy">' if pth.exists() else ""
        rows.append(
            f'<a class="frame" href="{href}">'
            f'<span class="frame__img">{img}</span>'
            f'<span class="frame__k">[ {label} ]</span>'
            f'</a>')
    ticker = "".join(f'<span>{i:02d}</span>' for i in range(1, n + 1))
    return ('<div class="beltwrap">'
            f'<div class="belt">{"".join(rows)}</div>'
            '<p class="belt__count" aria-hidden="true">'
            f'<span class="belt__win"><span class="belt__roll">{ticker}</span></span>'
            f'<span class="belt__of">of {n:02d}</span></p>'
            f'<p class="belt__sr">Nine sections, pushed sideways.</p>'
            '</div>')

INDEX = f"""<div class="sheet">
  <div class="cover">

    <header class="poster">
      <h1 class="poster__name">Francis<br>Ruan</h1>
      <p class="poster__sub">student at university of southern california</p>
    </header>

    {belt()}

    <footer class="cover__foot">
      <ul class="marks__row">
        <li><img class="mk mk--usc"   src="assets/logos/uscmarshall-black.png" alt="USC Marshall"></li>
        <li><img class="mk mk--vuori" src="assets/logos/vuori.svg"             alt="Vuori"></li>
      </ul>

      {pieces_box()}

      <p class="cover__links">
        <a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a>
        <a href="https://www.linkedin.com/in/francisruan" target="_blank" rel="noopener">LinkedIn</a>
        <a href="Ruan_Francis_Resume.pdf" target="_blank" rel="noopener">Resume</a>
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
  ("How people are persuaded", [
    ("Creative writing",  "How a sentence gets somebody to feel something they did not arrive intending to feel."),
    ("Comedy &amp; timing",   "The same question with a stopwatch on it. Why one beat lands and the identical line half a second later does not."),
    ("Interface design",  "Persuasion with no words in it at all, which is the hardest version."),
    ("Mandarin",          "What I can and cannot say to my mother in her own language, and what that gap costs both of us."),
  ]),
  ("How value hides", [
    ("Finance &amp; valuation",  "What a business is quietly worth to somebody who understands it better than its accounts do."),
    ("Consumer M&amp;A",         "Why two companies on the same shelf clear seven times apart."),
    ("Education &amp; attention","The most valuable thing a society allocates, handed out by postcode."),
    ("Inequality",               "Not the fact of it. The machinery that keeps it standing after everyone agrees it should not."),
  ]),
  ("How a body holds up", [
    ("Physiology &amp; recovery",     "Mechanism first, always. Not that sleep matters but what glymphatic clearance actually is."),
    ("Self-quantification",           "Running bloodwork against my own baselines, which sounds clinical and is really curiosity pointed inward."),
    ("Decision making under stress",  "What happens to judgement at mile nine, and whether any of it can be trained."),
    ("Endurance",                     "The only laboratory I have where the variable is me."),
  ]),
]

def plate():
    """The twelve, grouped by the question underneath them rather than pinned to a
    picture of a head. Numbered and ruled, in the cover's language."""
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


CURIO = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">Intellectual curiosity</p>
  <h1>Twelve Things I Keep Going Back To</h1>
</header>
<div class="body">
{soundtrack("curiosity.html")}
<figure class="defn">
  <p class="defn__w">curiosity</p>
  <div class="defn__b">
    <p class="defn__d">not the wish to know a thing, which is appetite and passes, but the refusal to accept the headline as the answer. the suspicion that every explanation you were handed is the shortened version, and the willingness to be the only person in the room still asking after everybody else has moved on.</p>
    <p class="defn__p">[ kyoor-ee-<em>os</em>-i-tee ]</p>
  </div>
</figure>

<p>Most people are taught it as a childhood trait, something you have plenty of at six and are expected to grow out of by twenty, as though the questions were a phase rather than the point. I have come to think it is closer to a discipline, and an unfashionable one, because it costs you something socially to keep asking after the conversation has agreed to stop. What follows is not everything I find interesting. It is the twelve I keep going back to, and what I have noticed is that they are really only three questions wearing different clothes.</p>

{plate()}

<h2>Published</h2>
<div class="pubs">
  <article><h3 class="pub__t">The Dinner Table</h3><p class="pub__m">Palo Alto Weekly, 39th Annual Short Story Contest &middot; May 2025 &middot; First place, Young Adult</p>
    <p>A short story about my mother, our kitchen, and the arithmetic of what she gave up. The judges wrote that it caught the smells, the sounds and the essence of true motherly love in a few paragraphs.</p>
    <p><a href="https://www.paloaltoonline.com/short-story/2025/07/17/short-story-contest-2025-the-dinner-table/" target="_blank" rel="noopener">Read it</a></p></article>

  <article><h3 class="pub__t">The Hands We No Longer Raise</h3><p class="pub__m">December 2025</p>
    <p>Through classroom observation and policy frameworks, I argue that the promise of educational technology often obscures deeper questions about attention, autonomy, and what a classroom is actually for.</p></article>

  <article><h3 class="pub__t">The Disunited States: How America Learned to Live with Inequality</h3><p class="pub__m">December 2025</p>
    <p>An essay on segregation, education, and the architecture of inequality. Not the fact of it, but the machinery that keeps it standing after everyone agrees it should not.</p></article>

  <article><h3 class="pub__t">Longitudinal Self-Quantification of Recovery, Stress, and Well-Being Using Wearable Technology</h3><p class="pub__m">December 2025</p>
    <p>Does systematically optimizing daily life against physiological recovery data actually make you happier? I wore the sensors and tracked the answer, which is less flattering to the premise than I expected.</p></article>
</div>
<p class="quiet">Three of these live on LinkedIn and need their public links dropped in.</p>

<h2>Essays</h2>
<div class="pubs">
  <article><h3 class="pub__t">Trade, Build, Settle</h3>
    <p class="pub__m">An essay on scarcity &middot; 1,600 words</p>
    <p>What a cardboard island taught me about the business of capital. Catan is not a game about settling an island. It is a game about creating value under scarcity, uncertainty, competition and dependence on other people, which is also a serviceable description of investment banking.</p>
    <p>It ends where the analogy does: there is no fiduciary duty in Catan, no regulator, no reputational memory. A board game can model scarcity and negotiation. It cannot model responsibility.</p>
    <p><a href="assets/Trade-Build-Settle.pdf" target="_blank" rel="noopener">Read the essay</a></p></article>
</div>

<h2>Where the curiosity goes</h2>
<div class="biglinks">
  <a href="trend.html"><span class="bl__lg"></span><span class="bl__n">Five supplement deals in six weeks</span><span class="bl__note">One aisle, one summer, a sevenfold spread in price.</span></a>
  <a href="invisible.html"><span class="bl__lg"></span><span class="bl__n">The assets AI builds that nobody records</span><span class="bl__note">The best output of a deployment never lands on the balance sheet.</span></a>
</div>
{ask("If any of this overlaps with something you are thinking about, write to me.")}
</div>
<nav class="nextprev"><a href="index.html">&larr; All nine</a></nav>
</div>"""

page("curiosity.html","Intellectual Curiosity | Francis Ruan",
     "A labelled plate of what Francis Ruan is curious about, and the essays and stories that came out of it.",
     CURIO, active="Curiosity")
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
  <caption>Announced 24 July to 2 September 2026.</caption>
  <thead><tr><th>Date</th><th>Buyer / target</th><th class="n">Value</th><th class="n">Basis</th></tr></thead>
  <tbody>
    <tr><td>24 Jul</td><td><a href="vitabiotics.html">Bain Capital / Vitabiotics</a></td><td class="n">~$1.2bn reported</td><td class="n">no public revenue</td></tr>
    <tr><td>4 Aug</td><td><a href="thorne.html">P&amp;G / Thorne</a></td><td class="n">$3.8bn reported</td><td class="n">~5.8x 2026E</td></tr>
    <tr><td>6 Aug</td><td>Kirin / Jamieson Wellness</td><td class="n">C$2.5bn EV</td><td class="n">27% premium</td></tr>
    <tr><td>1 Sep</td><td><a href="nestle.html">Yellow Wood / Nestl&eacute; VMS</a></td><td class="n">$1.0bn</td><td class="n">~0.8x 2025</td></tr>
    <tr><td>2 Sep</td><td>cbdMD / Twinlab</td><td class="n">undisclosed</td><td class="n">n/a</td></tr>
  </tbody>
</table></div>
<p class="quiet">Thorne and Vitabiotics values are trade-press reported, not confirmed by the parties. Vitabiotics publishes no revenue, so there is no multiple here rather than a guessed one. Two 2025 comparables sit alongside: <a href="celsius.html">Celsius / Alani Nu</a> and <a href="poppi.html">PepsiCo / poppi</a>.</p>

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
     TREND, active="Curiosity")
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
    ("Valedictorian", "Ranked 1 of 553, Los Altos High School"),
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

page("awards.html","Awards | Francis Ruan",
     "Francis Ruan's record: valedictorian, TEDx speaker, Stanford ProCo, USC Presidential and Morgan Stanley scholarships, Dean's List.",
     HON, active="Lucky")
print("awards.html")
print("awards.html")

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
   '</tbody></table></div><p class="quiet">Every row on the right is an assumption a buyer would test. I have not published unit costs or margins, because the numbers are not stable enough to defend.</p>'),
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

page("finance.html","Finance | Francis Ruan",
     "Deal analysis, operating finance, and a podcast in progress about AI's quiet arrival inside investment banking.",
     FIN, active="Finance")
print("finance.html")

# ================================================================= HUBS =====
def hub(fn, eyebrow, title, lede, blocks, active, sub=""):
    if 'class="ask"' not in blocks:
        blocks = blocks + ask()
    subline = f'\n  <p class="dedication">{sub}</p>' if sub else ""
    body = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{title}</h1>{subline}
</header>
<div class="body">
{soundtrack(fn)}
{blocks}
</div>
<nav class="nextprev"><a href="index.html">&larr; All nine</a></nav>
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

hub("building.html", "Engineer", "What I Have Built",
    "",
    '<p class="kicker">Every one of these began the same way, with somebody doing a thing by hand that '
    'did not need a person in it, and a suspicion on my part that the person was in there for a reason '
    'nobody had bothered to name.</p>'

    '<h2>Ninety minutes down to three</h2>'
    '<p>At BODi I was the AI intern on the finance and growth side, which in practice meant sitting close '
    'enough to recurring invoice and general-ledger review to notice how much of it was spent confirming '
    'that things were fine. The records were almost always correct. That was precisely the difficulty, '
    'because the handful of exceptions that genuinely wanted a decision were sitting somewhere inside a '
    'queue you could only find by reading the whole thing line by line, and so the expensive part of the '
    'task was never the reviewing at all but the searching that came before it.</p>'

    '<p>The first useful thing I did was refuse to write anything for a while. I went to the FP&amp;A and '
    'Accounting owners and made them define, out loud and in writing, what actually constituted an '
    'exception, because the moment I encoded my own guess about that I would have been quietly setting '
    'policy while telling myself I was only building tooling. Thresholds, controls and sign-off stayed '
    'with them throughout, I built to their definitions, and they validated every output before anybody '
    'relied on it. Then I rebuilt the general-ledger cleansing so records arrived in one shape instead of '
    'several, and ran the automated output against manual review, again and again, until the two agreed '
    'often enough that I was willing to tighten the thresholds rather than loosen them.</p>'

    '<p>Selected recurring tasks went from roughly ninety minutes to somewhere between one and three, and '
    'I sized the annualised operating expense reduction at approximately <strong>$784K</strong> and '
    'presented it to the MD of Accounting. The speed was the least interesting part of it. What held my '
    'attention was the question underneath, which was what a human being was actually in that seat to '
    'decide, and how much of what looked like judgement turned out on inspection to be search.</p>'

    '<p>I should say plainly that the figure is a run-rate estimate built from task frequency and loaded '
    'analyst cost rather than realised profit and loss, and I would volunteer that before anyone thought '
    'to ask me for it. The thresholds are also still set by hand, which is the part I would go back and '
    'change first, because they ought to be learned from which flags accountants genuinely act on rather '
    'than from what I guessed would matter. I would build that feedback loop before optimising another '
    'thing. <a href="bodi.html">The full write-up is here</a>.</p>'

    '<h2>The price you have to name before anyone has paid you one</h2>'
    '<p>Suntag was mine end to end, which meant solar viability testing, the interface in Figma, the '
    'prototype code and the demos I ran mostly so that I could watch people&rsquo;s faces, and it also '
    'meant there was nobody in the room to hand the pricing question to. Hardware makes you commit tooling '
    'and a first production order before you have any demand data worth the name, so you price too low and '
    'delete the margin that funds the second run, or you price too high and end up holding inventory with '
    'no signal telling you why. We funded it pre-launch on a <strong>$5,000</strong> pre-seed with a '
    'waitlist above three hundred, and that is validation rather than revenue, and I am not going to '
    'describe it as more than it was.</p>'

    '<p>I got the important part wrong. I treated the waitlist as demand, when a waitlist only ever '
    'measures interest at a price of zero and says nothing whatsoever about the price at which that '
    'interest survives contact with a checkout page. Running it again I would take refundable deposits at '
    'two different price points before committing a cent to tooling, which converts a soft and flattering '
    'signal into a number I could defend to somebody sceptical, and costs almost nothing to do. '
    '<a href="suntag.html">The pricing decision, split into what I measured and what I assumed</a>.</p>'

    '<h2>USC Marshall, AI Builder Hub</h2>'
    '<div class="biglinks">'
      '<a href="https://github.com/fyruan-star/usc-catalogue-scraper" target="_blank" rel="noopener">'
      '<span class="bl__lg"><img src="assets/logos/uscmarshall.png" alt="USC Marshall"></span>'
      '<span class="bl__n">AI Builder Hub Engineer</span>'
      '<span class="bl__note">One of four student engineers. Reverse engineered the course '
      'registration system used by 45,185 students.</span></a>'
      '</div>'
    '<p>The piece that is public is the collector underneath it, which pulls one plain-text file per '
    'undergraduate programme out of USC&rsquo;s online catalogue. That is the input a degree requirements '
    'validator needs in order to exist at all, and nobody had built it, which is a recurring pattern in '
    'this kind of work: the unglamorous middle of a system is usually the part that is missing. It parses '
    '<strong>470</strong> programme descriptions and feeds a rules engine that checks a student&rsquo;s '
    'courses against what their degree actually demands rather than what they believe it demands.</p>'
    '<p><a href="https://github.com/fyruan-star/usc-catalogue-scraper" target="_blank" rel="noopener">'
    'github.com/fyruan-star/usc-catalogue-scraper</a></p>'

    '<h2>Also running</h2>'
    '<div class="biglinks">'
      '<a href="#" class="bl--flat"><span class="bl__lg"></span>'
      '<span class="bl__n">Los Altos Vintage</span>'
      '<span class="bl__note">Founded and operating.</span></a>'
      '<a href="#" class="bl--flat"><span class="bl__lg"></span>'
      '<span class="bl__n">Elevated Youth</span>'
      '<span class="bl__note">Founded and operating.</span></a>'
      '</div>'

    '<p>Writing the BODi work up is what pushed me toward '
    '<a href="invisible.html">an essay about where savings of that kind actually go</a>, which is nowhere '
    'the balance sheet can see them. That has become the question I keep circling.</p>',
    "Engineer")

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
    sub="&#25105;&#30340;&#22920;&#22920; &middot; w&#466; de m&#257;ma &middot; my mother")

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
    '<div class="videos videos--one videos--feature">'
    '<figure><video controls preload="metadata" playsinline poster="assets/video/homecoming-poster.jpg">'
    '<source src="assets/video/homecoming.mp4" type="video/mp4">Your browser cannot play this video.</video>'
    '</figure>'
    '</div>'

    '<p class="kicker">A fair question, asked of me often enough that I have had to develop an answer. '
    'The honest one is that I do not think I am one thing, and I have stopped apologizing for it.</p>'

    '<p>People get read as one-dimensional. The finance guy. The athlete. The funny one. Two dimensions '
    'if you are lucky, and three if somebody bothers to stay in the room. I would like to make the case '
    'that I am at minimum four, and that the fourth one is the interesting one, because it is the part '
    'that connects the other three and it is the part almost nobody asks about.</p>'

    '<h2>My spirit animal is a monkey who talked back to heaven</h2>'
    '<p>Sun Wukong. The Monkey King. His defining traits are appetite, cleverness, and mischief of the '
    'particular kind that makes trouble and makes people love him anyway. He is enormously capable and '
    'enormously undisciplined about it. He argues with heaven. He gets pinned under a mountain for five '
    'hundred years and comes out the same creature, still funny, still impossible, but finally pointed '
    'somewhere.</p>'
    '<p>I did not pick him to be flattering. I picked him because the appetite is real, the mischief is '
    'real, and I have had my own much shorter stint under a mountain.</p>'

    '<h2>The paperwork</h2>'
    '<dl class="keyval whoami">'
    '<dt>Sign</dt><dd>Pisces</dd>'
    '<dt>Lunar year</dt><dd>Golden Pig</dd>'
    '<dt>Trait I am accused of</dt><dd>Quicksilver tongued</dd>'
    '<dt>Trait I would claim</dt><dd>Intelligent playfulness</dd>'
    '<dt>Three words for 2026</dt><dd>Effervescent. Wonder-filled. Indomitable.</dd>'
    '<dt>Standing instruction</dt><dd>Doubt the default</dd>'
    '<dt>Second standing instruction</dt><dd>Talk to strangers</dd>'
    '</dl>'

    '<h2>What Ms. Yu said</h2>'
    '<p>My trigonometry teacher, asked about me for the school paper, described me as the kind of student '
    'who gives the teacher a headache in class, and then the teacher goes home and secretly laughs about '
    'all his antics.</p>'
    '<p class="pull">I have never disputed it. I have it more or less framed.</p>'
    '<p>There were other teachers who got as far as the headache and stopped. She is the one who kept '
    'reading, and I have thought about the difference between those two teachers for years.</p>'

    '<h2>Five things that explain me faster than I can</h2>'
    + loves() +
    '<p>Put them beside one another and the pattern stops being subtle. Every one of them is about '
    'somebody who was handed a smaller life than the one they turned out to be capable of and who '
    'declined it, politely in Austen&rsquo;s case and considerably less politely in Rudy&rsquo;s. They are '
    'also, all five, arguments that feeling things deeply is a form of competence rather than a failure '
    'of nerve, which is not the lesson boys are usually issued and is precisely the one I needed. What I '
    'take from Maclean and from Gerwig is that the ordinary hours are the prize itself and not the '
    'waiting room outside it. What I take from Will Hunting is that being clever is the least interesting '
    'thing about a person and by far the easiest thing to hide behind. And what I take from Elizabeth '
    'Bennet, who I am fairly sure would have found me exhausting, is that holding out for the correct '
    'thing costs you something socially and remains worth it anyway.</p>' +
        '<h2>Embracing your corny</h2>'
    '<p>I have decided to be corny deliberately, which I would recommend to anybody, because the '
    'alternative is a lifetime spent performing a coolness that not one person has ever actually enjoyed '
    'having performed at them. It is an enormous amount of work to seem unmoved, and the return on it is '
    'nothing.</p>'
    '<p>I am a poet some distance before I am an analyst. I like the beach, and I like reflecting on the '
    'beach, and I like finding somebody afterwards to tell about it. Romance films work on me without '
    'exception and without any resistance worth the name, and I stopped pretending to be above them at '
    'roughly the same age I stopped pretending not to want things, which turned out to be the same '
    'decision wearing two coats.</p>'
    '<p>And I have very specific instructions about how to treat somebody, because my mother taught them '
    'to me and she did not present them as optional. Buy the flowers, and buy them for no occasion, since '
    'an occasion is only a permission slip. Say the compliment out loud rather than thinking it warmly '
    'and assuming it arrived. Never go to bed upset, not once, however late that decision makes the '
    'night. Open the door, every time, for the rest of your life.</p>'
    '<p>And when something has gone wrong between you, do the harder thing, which is to sit down and work '
    'out honestly whether this is a you problem, because it very often is, and because it is almost never '
    'only a you problem either, which is the entire reason the word is we. Take the accountability all '
    'the way down to the bottom of it, past the point where it stops making you feel good about yourself '
    'for taking it, and then go a little further than that.</p>'

    '<h2>And I am also the other thing</h2>'
    '<p>I look up to bodybuilders, genuinely and without a trace of irony, for the specific reason that '
    'the whole discipline is a public argument that you can change what you were handed provided you are '
    'willing to be extremely boring about it for several years running.</p>'
    '<p>I watch an unreasonable quantity of NFL, and I mean unreasonable in the sense that I have '
    'developed opinions about offensive line play that nobody asked me for. I watch UFC and will happily '
    'explain why a fight was decided in the first ninety seconds by somebody&rsquo;s stance rather than by '
    'the thing everybody in the room was looking at. I know an embarrassing amount about cars, almost all '
    'of it useless, every bit of it retained without effort while the periodic table went straight '
    'through me. I was a captain on a football team and I am the person yelling in the huddle, and I like '
    'being that person a great deal. I still know more about dinosaurs than any grown man has a defensible '
    'reason to know, and I have made my peace with that.</p>'
    '<p>None of which is in tension with a single sentence of the section above it, and that is the whole '
    'of what I am trying to say. These are supposed to be two different men, the one who cries at Little '
    'Women and the one who wants to talk about the offensive line, and they were never two men at all. '
    'They have always been the same one, and the only thing that ever changes is which room he is '
    'standing in and how safe that room has made itself.</p>'

    '<h2>Things I will read about until three in the morning</h2>'
    '<p>Human pathogenesis. Biology and anatomy, mechanism-first, always. I keep profiles on myself and '
    'run bloodwork against them, which sounds clinical and is actually just curiosity pointed inward.</p>'
    '<p>Then: human history. Archaeology. Ancient civilizations. What people did before they had any of '
    'this. It is the same appetite that made me an insufferable dinosaur child, pointed at a longer stretch of time.</p>'
    '<p>Here is the one I bring up at dinner and refuse to let go of. For most of recorded European '
    'history people did not sleep the way we do. They slept in two shifts. You went down not long after '
    'dark for roughly four hours, then woke naturally around midnight into an interval people simply '
    'called <em>the watch</em>, and stayed up for an hour or two. Not anxiously. On purpose. They prayed, '
    'tended the fire, talked to whoever was next to them, visited neighbours, had sex, interpreted the '
    'dreams they had just surfaced from. Then a second sleep until dawn.</p>'
    '<p>The historian A. Roger Ekirch found hundreds of references to it, casually, across centuries, in '
    'diaries and court records and medical texts, described the way you would describe breakfast. It '
    'disappeared within a few generations of artificial light, and it disappeared so completely that we '
    'now diagnose the waking as a disorder and medicate it.</p>'
    '<p class="pull">We took a thing humans did for a thousand years, forgot it entirely, and started '
    'treating it as a symptom.</p>'
    '<p>I think about that constantly, and not only about sleep. I think about how much of what we call '
    'normal is about two hundred years old and wearing a very convincing costume.</p>'

    '<h2>The small operations</h2>'
    '<p>There is a whole method to this that I have set out <a href="fun.html">in the fun section</a>, '
    'about crumbs and operating expenses and why contentment is cheaper to build than joy. What belongs '
    'here is only the residue of it, the habits somebody would actually notice if they lived with me.</p>'
    '<p>I care about clothes. I like talking to strangers and I will do it in any queue, anywhere. And the '
    'genuine highlight of a given week is the part where all my roommates and I finally clean the '
    'apartment, and somebody puts music on, and everybody is loose and slightly stupid and dancing badly '
    'in a kitchen that is finally not disgusting. I have never wanted a better evening than that one.</p>'
    '<p>And once a day, every day, I send somebody a genuine compliment. It costs nothing and it '
    'returns more than anything else I do.</p>'
    '<p>I love waking up. I have never once been sorry that a day started.</p>'

    '<h2>The rules I actually keep</h2>'
    '<ul>'
    '<li>I will never raise my voice at my mother, my brother, or anyone in my family.</li>'
    '<li>I will not gossip, and I will not be disrespectful to friends or to strangers.</li>'
    '<li>I will spread encouragement to the people around me, on purpose, out loud.</li>'
    '<li>I will be more afraid of not trying than of failing.</li>'
    '</ul>'
    '<p>Those are written down in a note on my phone, which I realize is a slightly ridiculous place to '
    'keep a moral code. They have held up.</p>'

    '<h2>And three cats</h2>'
    '<div class="mosaic">'
    '<figure class="m1"><img src="assets/photos/cat-2.jpg" alt="A tabby cat asleep on a rocking chair" loading="lazy"></figure>'
    '<figure class="m2"><img src="assets/photos/cat-1.jpg" alt="A tuxedo cat sitting beside a parcel" loading="lazy"></figure>'
    '<figure class="m3"><img src="assets/photos/cat-3.jpg" alt="A cat stretched out on a counter" loading="lazy"></figure>'
    '</div>'
    '<p>Who have supervised, between them, most of the homework in this house. One of them appears in the '
    '<a href="my-why.html">first photograph on the site</a>, which tells you roughly how long this '
    'arrangement has been going on.</p>'
    + ask("If you have made it this far you may as well introduce yourself."),
    "I")

hub("fight-on.html", "Fight On", "What &ldquo;Fight On&rdquo; Means to Me",
    "",
    '<figure class="lead"><img src="assets/photos/fight-on.jpg" '
    'alt="Francis Ruan as a young boy, grinning, holding up a peace sign" width="1200" height="1600">'
    '<figcaption>Roughly the era in question.</figcaption></figure>'

    '<p class="kicker">The bell went at three, and for about ten minutes the front of that school was the '
    'busiest place in the world.</p>'

    '<p>The cars started lining up before the bell had even finished, a long patient row of them curling '
    'around the loop with their engines running, and mothers got out and leaned on the doors with their '
    'arms folded, and there was a particular sound the whole thing made, three hundred children coming out '
    'of a building at once and finding, every single one of them, the exact car they were looking for. '
    'Somebody&rsquo;s dad always had the window down. Somebody&rsquo;s mum always had a snack ready in the '
    'passenger seat, which I thought was the most extraordinary act of forethought I had ever witnessed. '
    'And within about ten minutes the loop was empty and the engines were gone and the sound went with '
    'them, and what was left was a very large campus, a low sun, and me.</p>'

    '<p>My mother was a nurse and her shift did not end when other people&rsquo;s shifts ended. She was '
    'standing somewhere under a fluorescent light while all of that was happening, and she would keep '
    'standing there for another six hours. So I had six hours to fill and no phone to fill them with, '
    'which meant that what I actually had was six hours and an entire school to myself.</p>'

    '<p>I learned that place the way you learn a house in the dark. I knew which trees held weight and which '
    'ones dropped you. I knew the patch of concrete behind the cafeteria that stayed warm until five and took '
    'chalk well, and I drew on it, badly, for years, and rain took all of it and I drew again. I knew every '
    'sound the building made as it emptied out, which is a strange thing for a nine-year-old to be an expert in.</p>'

    '<p>And I knew the fields. There were always kids out there after the last bell, in cleats, in club '
    'uniforms, running the drills that cost money. I watched a great deal of that. I want to be accurate here: '
    'I did not resent it, or not for long. It was more that I understood early that there were two categories, '
    'and I could name which one I was in, and the naming was not painful so much as simply factual, like '
    'knowing your own height.</p>'

    '<p>What I drew on that concrete was mostly the same three things over and over. A stadium. A house with '
    'far too many windows. And a car, always a car, always with two people in it, which is not subtle and I '
    'am not going to pretend I did not notice later what that was about.</p>'

    '<p>The hard part was never the six hours. I would like to be very clear about that, because people hear '
    'this and assume the loneliness was the wound. It was not. I was fine. I was a boy in a tree with a stick '
    'and an entire school to myself, which at nine years old is closer to a kingdom than a punishment.</p>'

    '<p>The hard part was nine o&rsquo;clock, when the headlights finally came around the loop, and I got in '
    'the car and saw her face and understood immediately that her day had been worse than mine.</p>'

    '<h2>What it meant at Ranch 99</h2>'

    '<p>There is a particular arithmetic a child performs in a grocery store when he already knows the family '
    'condition. You do not ask. That is the entire skill. You walk the aisle, you see the thing, and you run a '
    'small silent calculation about whether asking would put a certain look on your mother&rsquo;s face. The '
    'answer was usually yes. So you keep walking, and you say nothing, and above all you do not make it a moment.</p>'

    '<p>I got very good at not making it a moment. I am genuinely unsure whether that was healthy. I am quite '
    'sure it has been useful.</p>'

    '<h2>What it meant on a Tuesday morning</h2>'

    '<p>I showed up to school in a shirt inside out more than once. Backward too, which is a different and '
    'meaningfully worse mistake. Nobody had checked, because the person who would have checked got home at '
    'seven and needed to sleep before she did it again.</p>'

    '<p>So you learn to laugh first, and loudly, before anyone else can get there. If you say it, it is a joke. '
    'If they say it, it is something else entirely. I have used that reflex approximately every day since.</p>'

    '<h2>What it meant in sixth grade</h2>'

    '<p>I started answering my mother&rsquo;s email in sixth grade. Not forwarding it to her. Answering it. '
    'Permission slips, school forms, fundraiser notices, the endless administrative weather of having children '
    'in America, all of it arriving in a language she was still fighting with at the end of a fourteen-hour '
    'shift. So I wrote back as her, carefully, in the politest English an eleven-year-old could manage, and I '
    'signed it with her name.</p>'

    '<p>I did not experience that as unusual. I experienced it as my job. I think I was proud of it.</p>'

    '<h2>What it meant at the stove</h2>'

    '<p>I learned to cook young because the alternative was not eating. There was nothing charming about it. '
    'No adult stood behind me explaining heat. I burned things, and then over some months I stopped burning '
    'things, and nobody was there for either milestone.</p>'

    '<h2>What it meant for playdates</h2>'

    '<p>Other children were dropped off. I ran. My mother was at work and the distance between our '
    'apartment and wherever everybody was gathering was a mile or two of identical suburb, so I went on '
    'foot, in cleats more than once, and arrived warm and slightly out of breath and did not explain '
    'why.</p>'

    '<p>Sometimes I got lost. I had no phone, the streets in that part of town repeat themselves, and '
    'more than once a car slowed alongside a boy standing at an intersection trying to work out which '
    'direction was home. I had my mother&rsquo;s number memorised the way other children memorise a '
    'song. I would recite it to whoever had stopped, and somebody&rsquo;s father would ring her from his '
    'own phone, and she would tell him where we lived while I sat in the back of a stranger&rsquo;s car '
    'being driven home by a man whose name I never learned. She thanked every one of them. I think about '
    'that more than I expected to, that a working woman&rsquo;s entire contingency plan for her son '
    'getting lost was the decency of whoever happened to be passing, and that it held.</p>'

    '<h2>The honest inventory</h2>'

    '<p>Roughly in order.</p>'

    '<p>I could not swim. Not slowly, not badly, I simply could not do it, because swimming is a thing '
    'somebody pays for and then drives you to twice a week for a year. I could not throw a football with '
    'a spiral on it. I could not dribble a basketball with my left hand, or with any real conviction '
    'using my right. I had never stood in a batter&rsquo;s box. Soccer I understood mostly as a rumour, '
    'something other boys seemed to have been issued along with their shin pads. I could not hit a '
    'spikeball, and I was laughed at for that repeatedly, by people who were not being cruel so much as '
    'accurate. I picked up a lacrosse stick for the first time at a tryout, in front of boys who had been '
    'holding one since they were eight, and the sound a group makes while it watches you fail at '
    'something easy is not a sound you forget.</p>'

    '<p>I was fat, and I was told so, in the specific unhurried way children tell each other things. I '
    'was picked last often enough that it stopped registering as an event and began registering as '
    'information, which I have come to think is the part that actually does the damage. Nobody was being '
    'vicious. They were being correct, and by about nine I had quietly accepted the account they had '
    'given me, which was that I was unathletic, ungifted, and the fat kid, and that these were facts '
    'about my nature rather than about my circumstances. It is remarkable how fast a child will take '
    'somebody else&rsquo;s arithmetic and file it as truth about himself.</p>'

    '<p>School offered no rescue either. I went to summer school every summer of elementary school. My '
    'English was still arriving, and I spent those Junes being taught again what I had not managed to '
    'hold the first time, and I did not think of myself as somebody who was good at learning, because '
    'nothing in the available evidence suggested that I was.</p>'

    '<p>None of which made me miserable, and I would be lying by omission if I let this read as a sad '
    'childhood, because it was not one. I had friends, a great many of them, because I worked out '
    'extremely early that if you are going to be the worst athlete on the field you had better be the '
    'funniest person on it. Fart noises, I discovered, are universal. They translate across every '
    'language barrier a seven-year-old is ever going to meet, and mine was considerable. I once '
    'microwaved a plastic baby in the pretend kitchen of a kindergarten classroom and got a laugh so '
    'total, so unanimous, that I have been chasing it in one form or another ever since. I could not '
    'catch anything, but I could make a room go, and a room that is laughing does not much care what you '
    'cannot do.</p>'

    '<p>Add it up and the fair summary of me at eleven is: not good at anything yet.</p>'

    '<h2>What I actually had</h2>'

    '<p>Three things, and I have spent real time thinking about this.</p>'

    '<p><strong>Spirit</strong>, which is a soft word for a hard thing. I did not stop. Not out of discipline. '
    'Stopping simply was not on the menu at my house, and by the time I was old enough to notice that other '
    'houses had it on the menu, I had already lost the taste for it.</p>'

    '<p><strong>A smile</strong>, and a real one. Not a performance. I liked people. I still do, embarrassingly '
    'much, and it has cost me far less than people warned me it would.</p>'

    '<p><strong>A joke</strong>, always loaded, usually deployed about four seconds after something went badly '
    'and occasionally while I was still crying. If somebody in the room was having a worse day than I was, I '
    'would find the thing that made them laugh, and I would find it fast. That was the one skill I had before '
    'I had any others.</p>'

    '<p class="pull">I never wanted to do anything wrong. That is the part nobody believed.</p>'

    '<p>I wanted, more than almost anything available to want, to be good. Being read as trouble while you are '
    'trying that hard is a specific ache, and I would not wish it on a child, and I am not sure I would trade '
    'it either.</p>'

    '<h2>What nobody had told me</h2>'

    '<p>Here is the thing I did not understand until years later, and it has reorganised how I look at '
    'more or less everything since.</p>'

    '<p>The boys who could throw a spiral had been throwing one in a garden with somebody since they were '
    'four. The boy who moved fluidly through a lacrosse drill had six years of muscle memory behind him '
    'that I could not see, because muscle memory is invisible and from the outside it looks exactly like '
    'talent. The same was true in basketball, in baseball, in soccer, in the water. They were not gifted '
    'and I was not deficient. They were early, and early compounds, and I had been comparing my first '
    'week against their sixth year and drawing conclusions about my nature from the gap.</p>'

    '<p>What I had instead was video games, which nobody counts as anything at all. But a game teaches one '
    'specific and enormously transferable discipline, which is that dying is information. You die, and you '
    'ask what killed you, and you change a single variable, and you go again, and the loop tightens every '
    'time you run it. Thousands of hours of that is not nothing. It is a childhood spent rehearsing the '
    'one thing most people never rehearse, which is looking directly at your own failure without '
    'flinching and asking it a question.</p>'

    '<p>It is also, and I did not see the connection for a long time, the reason I got better at school. I '
    'was never the boy who simply knew. I was the boy who went back afterwards and worked out precisely '
    'where the understanding had broken, and that turned out to be worth considerably more than knowing, '
    'because it kept working after the material got hard and the boys who simply knew ran out of '
    'road.</p>'

    '<p>Everybody talks about getting up, and getting up is the cheap half of it. What changes the next '
    'repetition is getting up while knowing exactly what put you down, and that is the only version of '
    'resilience I have ever found that actually accumulates instead of merely repeating.</p>'

    '<p>So I keep notes now. After a session I write down what I could not do and why, and I look for the '
    'bottleneck rather than the failure, and then I train the bottleneck rather than the sport. I am, and '
    'I promise this is not a boast because it cost an absurd number of hours, now the best spikeball '
    'player I know. I am better than most of my friends at a good many things they used to beat me at '
    'without trying. And I found surfing, which almost none of them compounded as children either, so we '
    'all began at zero on the same morning and I finally got to see what happens when the starting line '
    'is honest.</p>'

    '<p>None of which made me talented. It made me suspicious of the word. I no longer believe there is '
    'any such thing as simply smarter or simply more athletic. There is only experience that compounded '
    'somewhere you were not standing to watch it, and the very large difference between a person who has '
    'been doing a thing for six years and a person who started on Tuesday, which almost everybody, '
    'including the person starting on Tuesday, mistakes for a difference in kind.</p>'

    '<h2>And then I got to USC</h2>'

    '<p>And found they had made a slogan out of it.</p>'

    '<p>Fight On. Two words on every wall and every shirt, thrown up with two fingers, chanted by eighty '
    'thousand people who mostly mean it as encouragement for a football team, which is a perfectly good thing '
    'to mean by it.</p>'

    '<p>I remember hearing it the first time and feeling something complicated, because it does not mean a '
    'cheer to me. It means nine o&rsquo;clock in an empty parking lot. It means not asking at Ranch 99. It '
    'means an inside-out shirt and getting to the joke before anybody else can. It means writing your '
    'mother&rsquo;s email in sixth grade, and learning the stove by yourself, and running a mile because '
    'asking for a ride costs something you have decided not to spend.</p>'

    '<p class="pull">It means nobody is coming to make this easier, and you go anyway, and '
    'you go cheerfully, because bitterness is enormously heavy and I could never afford to carry '
    'any.</p>'

    '<h2>On lemons</h2>'

    '<p>Everyone knows the line. If life gives you lemons, make lemonade, and it is a perfectly good '
    'sentiment for people who are being given lemons. The trouble with it, and nobody ever says this part '
    'out loud, is that it quietly assumes a delivery. It assumes somebody arrives at your door with a '
    'crate, and that your only real problem is deciding what to do with what has already been handed to '
    'you.</p>'

    '<p>Nobody came to our door. So the sentence had to be extended, and I have spent a long time '
    'extending it. If life gives you lemons, make lemonade. If life gives you nothing, then go and find '
    'the lemons, and accept that they will sit further away than they sit for other people and that you '
    'will be walking. If there are none to find, plant them, and understand while you are kneeling in the '
    'dirt that a lemon tree takes somewhere between three and six years to fruit, which means you are '
    'working on behalf of a version of yourself you have not met yet and will have to trust. If the soil '
    'will not take a seed, then spend a season making soil, which is the least romantic labour there is '
    'and the only labour that makes any of the rest of it possible. And if you have no land at all, go and '
    'be useful in somebody else&rsquo;s orchard until you know enough about lemons that the next stranger '
    'with a field wants you standing in it.</p>'

    '<p class="pull">Fight on has never meant the lemons are coming. It means you go looking anyway, and '
    'you plant anyway, and you stay cheerful about the digging, because the digging was always going to be '
    'the job.</p>'

    '<p>That is the whole of it, and I want to be precise, because it is not optimism, which sits and '
    'waits with a pleasant expression, and it is not grit, which grinds and calls the grinding a virtue. '
    'It is closer to a decision made early and re-made most mornings: that the absence of a crate at the '
    'door is information about the world rather than a verdict on me, and that there is a lemon somewhere '
    'with my name on it if I am willing to go the distance the other children were never asked to go. I '
    'have never resented that distance for very long. It is the one part of all this I would not trade, '
    'because the walking is where I learned everything I actually have.</p>'

    '<p>There is a version of this story where the boy is bitter, and I understand how you get there. All the '
    'ingredients are present. But I have met bitter people and they are so tired, and being tired is the one '
    'thing my mother never got to be, so it always felt like a strange thing to spend her money on.</p>'

    '<p>I did not learn to fight on at USC. I learned it in a schoolyard at nine at night with a piece of '
    'chalk and nobody watching. USC only gave me the words for it, and I was glad to finally have them, '
    'because I had been doing the thing for about twelve years without knowing what to call it.</p>'
    + ask("If any of this sounds like your childhood too, I would like to hear from you."),
    "Fight On")

hub("leadership.html", "Leadership", "The Sideline Is a Vantage, Not a Consolation",
    "",
    '<figure class="lead"><img src="assets/photos/origin-leadership.jpg" '
    'alt="Francis Ruan as a small boy in front of a flag" width="900" height="900">'
    '<figcaption>An early and unsubtle interest in standing in front of people.</figcaption></figure>'

    '<p class="kicker">Everyone on that field was bigger than me. I mean everyone, including at least one '
    'kicker, and I have come to think of it as one of the luckier things that ever happened to me, though '
    'it took about two years to start looking like luck.</p>'

    '<p>Here is what I actually signed up for. Freshman year, never played a down in my life, one of very '
    'few Asian kids in the programme, and genuinely the worst guy out there, which my friends told me '
    'often and kindly and which was simply accurate. I was nowhere near starting. I was not going to be '
    'the story that season or the one after it. And for about two years that hurt in the specific way '
    'things hurt when you are fifteen, which is not dramatically, just constantly, a little every day at '
    'practice.</p>'

    '<p>Then something shifted, and I have spent a long time trying to name it. The closest I can get is '
    'that I stopped watching the ball.</p>'

    '<h2>What you can see from four feet off the field</h2>'

    '<p>Nobody tells you this about a sideline. A player out there sees his assignment. He sees the man '
    'across from him and the next two seconds, and I want to be clear that this is not a limitation, it is '
    'the entire job, and the good ones guard that tunnel like it is their wallet.</p>'

    '<p>But somebody has to be watching the whole thing, and that somebody turns out to be whoever happens '
    'to have the time.</p>'

    '<p>So I started noticing. That the left tackle had gone quiet somewhere in the second quarter and '
    'nobody had clocked it. That the safety was pressing because he was angry about something from before '
    'the game, not because the coverage had asked him to. That the sophomores had stopped talking to each '
    'other, which I eventually worked out is always, always the first sign that something has gone wrong '
    'underneath. Nobody assigns you that. There is no meeting where it gets handed out. You start doing it '
    'because you can see it, and then one day you notice you have been doing it for months and that it is '
    'real work.</p>'

    '<h2>People arrive one at a time</h2>'

    '<p class="pull">A team is not a unit. It is forty separate difficult conversations wearing the same '
    'colour.</p>'

    '<p>That reads like a line, but I mean it operationally. The corner who has just been beaten deep does '
    'not want a speech. He wants somebody to sit down next to him and say absolutely nothing for a minute '
    'while the humiliation finishes moving through him, and if you talk during that minute you have made '
    'it worse. The lineman who is furious needs to be furious somewhere else first, before he says the '
    'sentence he will not be able to take back. Those are two entirely different people needing two '
    'entirely different things from about nine feet apart.</p>'

    '<p>I got good at working out which one I had in front of me before I opened my mouth. Honestly that is '
    'the most useful thing football ever gave me, well ahead of anything that happened in a weight room, '
    'and I use it constantly now, including in rooms with no helmets in them.</p>'

    '<h2>Monday is the whole job</h2>'

    '<p>People assume the hard part is losing. It is not. Friday night is loud and then it is over.</p>'

    '<p>Monday is the hard part, because Monday is quiet and Monday does not end. You have forty people who '
    'were beaten in front of their families, and now it is cold, and nothing has changed except that every '
    'one of them is carrying fresh evidence that they might not be as good as they had hoped. Getting that '
    'group back out to run it again properly is the actual work of leading anything at all, and I do not '
    'think I am overstating it.</p>'

    '<p>Anybody is useful when it is going well. I got very good at Mondays, and I have never once regretted '
    'the trade.</p>'

    '<h2>The game is bigger than the player</h2>'

    '<p>This is the part that rearranged me, and I want to say it without making it sound tidier than it '
    'was.</p>'

    '<p>My snap count was never going to be the story. I knew that. And I spent two years letting that fact '
    'make me smaller, which is such a waste of two years that I get mildly annoyed thinking about it now. '
    'Then at some point it simply stopped mattering. There was no moment, no speech, nothing cinematic. It '
    'just quietly stopped being the thing I was measuring myself with.</p>'

    '<p>And the second I stopped counting reps I became dramatically more useful, because I could finally '
    'see the whole field instead of my own small rectangle of it. There is a real and badly underrated '
    'freedom in working out that you are not the protagonist. It hands you back all the attention you had '
    'been spending on yourself, and that turns out to be an enormous amount of attention, and you can '
    'spend it on very nearly anything.</p>'

    '<p>They voted me team captain. I did not play much.</p>'

    '<p>I think about that more than any award I have, and there is a whole page of those, because it is '
    'the only one I did not get by being good at something. The spotlight and the leadership turned out to '
    'be two different jobs, and plenty of people who hold one never hold the other. You do not need the '
    'ball to carry a squad. You need to be the person everybody looks at when it goes badly, and you need '
    'to have decided, well before it goes badly, exactly who you intend to be when it does.</p>'

    '<h2>Where it turns out I still am</h2>'

    '<p>I am the alumni chair for USC men&rsquo;s lacrosse, which makes me responsible to roughly three '
    'hundred and fifty alumni across fifty-one graduating classes and for a budget somewhere near $165K, '
    'and it has turned out to be exactly the same job in different weather.</p>'

    '<p>Not one person in that group is obliged to answer me. They have careers and families and an '
    'entirely reasonable claim on their own Saturdays. The only thing that moves them is whether the '
    'person asking has bothered to understand what a particular season actually meant to the people who '
    'played in it, which means the work is the same work, just spread across five decades instead of one '
    'locker room. That is Monday again. And I find I am still considerably better at that than at anything '
    'likely to get my own name read out.</p>'

    '<p>Four years, three on varsity. <a href="awards.html">The rest of the record is here</a>, though it is '
    'much less interesting than this.</p>'
    + ask("If you are building a team and want to argue about any of this, I am easy to reach."),
    "Leadership")

hub("fun.html", "The art of fun", "The Unserious Half",
    "",
    '<figure class="lead"><img src="assets/photos/origin-fun.jpg" '
    'alt="Francis Ruan as a small boy in a ninja costume with his older brother" width="900" height="900">'
    '<figcaption>No occasion. That was the point.</figcaption></figure>'

    '<p class="kicker">I have never really grown out of this. The costume changed and the sword got '
    'confiscated, but the operating principle has held.</p>'

    '<h2>Most of life is Tuesday</h2>'

    '<p>Not the bad Tuesday. The ordinary one, where nothing is wrong and nothing is especially '
    'interesting either, and you have somewhere to be at ten. Nobody warns you what the ratio is going '
    'to be. The extraordinary days are real and they are rare, and if you have built a life that only '
    'works on those, you have built something that is switched off almost all of the time.</p>'

    '<p>So I have spent a while thinking about crumbs.</p>'

    '<p>If you took every genuinely small good thing out of one unremarkable day, the first sip while it '
    'is still too hot, the song that arrives at exactly the right moment, the dog you were not expecting, '
    'somebody holding a door about two seconds longer than they had to, and you saved them the way you '
    'would save crumbs, then by the end of a year you would have something you could actually eat. A meal. '
    'Probably several. Nobody has one enormous meal a year. That is not how eating works, and I do not '
    'think it is how living works either.</p>'

    '<h2>The accounting version</h2>'

    '<p>Here is the version I actually believe, and I am going to use the only vocabulary I have, which is '
    'unfortunately finance.</p>'

    '<p>Most people try to raise their happiness by increasing revenue. Bigger wins, better news, more of '
    'everything. That works, briefly, and it is expensive and deeply unreliable, because almost none of '
    'the revenue line is up to you.</p>'

    '<p>The other side of the statement is entirely up to you. Happiness has operating expenses. The grudge '
    'you are still carrying. The comparison you keep running. The thing you have not said to somebody. The '
    'room you will not clean. Every one of those is a fixed cost draining the account every single day, '
    'quietly, whether or not anything good happens to you.</p>'

    '<p>Take the costs out and the arithmetic changes completely. If your expenses sit near zero, then any '
    'revenue at all, however small, leaves you positive. You do not need a good day. You need a day with '
    'nothing subtracting from it, and then the crumbs are enough on their own.</p>'

    '<p class="pull">Profit does not have to clear the bar for happiness. It only has to be greater than '
    'zero, and greater than zero is contentment, and contentment is available on a Tuesday.</p>'

    '<p>I am not claiming this gets you to joy. Joy has a threshold and there are weeks you will not clear '
    'it and should not pretend to. But a house of contentment is something you build by removing things, '
    'not by acquiring them, and it stands up in weather that joy simply does not.</p>'

    '<h2>So, the crumbs, collected on purpose</h2>'

    '<p>I take an unreasonable number of selfies, for nobody in particular. I film short videos of '
    'completely ordinary afternoons, because a year from now the ordinary afternoon is precisely the thing '
    'I am going to want back and it is the only thing nobody thinks to record.</p>'

    '<p>I talk to myself constantly, out loud, and I tell myself jokes, and I find them funny. This is '
    'either a warning sign or the cheapest entertainment ever devised and I have made my decision about '
    'which.</p>'

    '<p>And once a day, every day, I send somebody a compliment. A real one. Specific, unprompted, to '
    'somebody who was not expecting anything from me that morning.</p>'

    '<p>I want to be honest that this is not selfless. It is the highest-return thing I have ever found. If '
    'a good day is dessert for your mouth, this is dessert for the heart, and watching what a genuine '
    'compliment does to a person, the small recalibration, the way they hold themselves slightly '
    'differently for the next minute, is genuinely unmatched by anything I can buy. It costs nothing. It '
    'takes about eleven seconds. I have never once regretted sending one and I have sent a great many.</p>'

    '<p>The whole method, such as it is, comes down to keeping the expenses near zero and collecting the '
    'crumbs deliberately rather than hoping they accumulate on their own, and I can report that it has '
    'never once let me down on a Tuesday.</p>'

    '<div class="band">'
    '<figure><img src="assets/photos/fun-house.jpg" alt="Francis Ruan with friends in front of a painted Trojan mural" loading="lazy"></figure>'
    '<figure><img src="assets/photos/fun-river.jpg" alt="Francis Ruan tubing the Salt River with friends" loading="lazy"></figure>'
    '<figure><img src="assets/photos/fun-dorm.jpg" alt="A room full of friends, one playing guitar" loading="lazy"></figure>'
    '</div>'

    '<h2>Water and training</h2>'
    '<p>I surf El Porto most mornings before class and teach lessons there on weekends. I am training for '
    'the Santa Cruz Half Ironman and race HYROX in Anaheim this December. I play lacrosse at USC, ran track, '
    'and played four years of football.</p>'
    '<p>None of which explains why the best hours of any summer are the ones on a lake with a rope in your '
    'hand and no particular plan.</p>'
    '<div class="pair">'
    '<figure class="pair__a"><img src="assets/photos/fun-boat.jpg" alt="Francis Ruan on a boat with an arm raised" loading="lazy"></figure>'
    '<figure class="pair__b"><img src="assets/photos/surf.jpg" alt="Francis Ruan riding a board behind a boat" loading="lazy">'
    '<figcaption>A lake, a tow rope, and the same forty square inches of board.</figcaption></figure>'
    '</div>'

    '<h2>The kitchen</h2>'
    '<p>I invent recipes and make my friends eat the failed ones. I hold strong and mostly unwelcome '
    'positions on bulgogi, on grilled cheese, and on the correct Arnold Palmer ratio, which is more '
    'lemonade than anyone will admit.</p>'

    '<h2>Why I am always trying to make you laugh</h2>'

    '<p>I should be honest about where the jokes come from, because people tend to read them as confidence '
    'and they did not start out that way at all. They started as a door I could get through. When you are '
    'the smallest boy on the field and the worst one on it, and you are still working out the language, '
    'there are not many currencies available to you, and it turns out that making somebody laugh is the '
    'one thing nobody checks your credentials for. Nobody has ever asked me whether I was qualified to be '
    'funny. They simply laughed or they did not, and the transaction settled instantly, which for a child '
    'with very little else to trade was an enormous discovery.</p>'

    '<p>So I got fast at it, and I got fast at it specifically under pressure, which is the part I have '
    'come to find interesting. I am nervous more often than anybody watching would guess. The difference '
    'is only that my nerves come out as a joke rather than as silence, and I have stopped apologising for '
    'that, because a laugh is a genuinely useful thing to do with adrenaline. It lets the air out of a '
    'room that was holding its breath. It tells everybody else present that they are permitted to be '
    'human here, which is often the only thing standing between a group of people and an actual '
    'conversation.</p>'

    '<p>The other half of it is simpler and less strategic. If somebody in the room is having a worse day '
    'than I am, I want to find the thing that fixes it, and I want to find it fast, and I have never once '
    'regretted the four seconds it costs me to try. Failing at that is cheap. You make the joke, it lands '
    'flat, everybody moves on, and the only casualty is a small piece of your dignity, which I stopped '
    'guarding at around age nine and have not missed since. That is a spectacular return on risk and I do '
    'not understand why more people are not taking it.</p>'

    '<h2>Making things nobody asked for</h2>'
    '<p>Stand-up comedy. Small films with no audience. A journal nobody has read. I document my life '
    'obsessively, mostly on a camera, and I will put my face through any hole in any painted board I '
    'encounter, without hesitation, every single time.</p>'
    '<figure class="offset"><img src="assets/photos/fun-cutout.jpg" alt="Francis Ruan and a friend behind a painted carnival cutout" loading="lazy">'
    '<figcaption>Exhibit A. There was no line. There did not need to be a line.</figcaption></figure>'

    '<h2>The people, mostly</h2>'
    '<p>If I am honest, almost none of the above is really the point. The point is who is standing next to '
    'you while it happens, which is the sort of thing you are supposed to work out much later than I did.</p>'
    '<div class="mosaic">'
    '<figure class="m1"><img src="assets/photos/fun-couch.jpg" alt="Friends crowded onto a couch" loading="lazy"></figure>'
    '<figure class="m2"><img src="assets/photos/fun-hallway.jpg" alt="Friends in a hallway" loading="lazy"></figure>'
    '<figure class="m3"><img src="assets/photos/fun-flash.jpg" alt="Two friends, flash photograph at night" loading="lazy"></figure>'
    '</div>'

    '<h2>And away from here</h2>'
    '<p>Prague at sunset. A harbour in Catalina. A fire road above the ocean at the end of a day. I take '
    'the camera everywhere and I am not sorry about it.</p>'
    '<div class="band band--three">'
    '<figure><img src="assets/photos/fun-prague.jpg" alt="Francis Ruan and a friend on a bridge in Prague at sunset" loading="lazy"></figure>'
    '<figure><img src="assets/photos/fun-catalina.jpg" alt="Francis Ruan and a friend at a harbour in Catalina" loading="lazy"></figure>'
    '<figure><img src="assets/photos/fun-trail.jpg" alt="Two silhouettes on a trail at sunset" loading="lazy"></figure>'
    '</div>'

    '<h2>Reading for the mechanism</h2>'
    '<p>I read pathology and nutrition research for fun, which is a strange thing to put in the fun section. '
    'What I am after is never the headline, it is the mechanism. Not that sleep matters, but what glymphatic '
    'clearance is and why eight hours are not four plus four. Same instinct that makes me read a deal and '
    'want to know what was actually bought.</p>'

    '<div class="tags"><span>Stand-up</span><span>Inventing recipes</span><span>Arnold Palmers</span>'
    '<span>Bulgogi</span><span>Morning surf</span><span>El Porto</span><span>Lacrosse</span><span>Football</span>'
    '<span>Track</span><span>HYROX</span><span>70.3 Ironman</span><span>Recreational filmmaking</span>'
    '<span>Creative writing</span><span>Journaling</span><span>Documenting my life</span><span>Pinterest</span>'
    '<span>Bento grid UI</span><span>Design</span><span>Huberman Lab</span><span>Psychology</span>'
    '<span>Pathology</span><span>Nutrition</span><span>Entrepreneurship</span><span>Travel</span>'
    '<span>Catan</span><span>Mandarin</span></div>'

    '<h2>Teams</h2>'
    '<div class="teamgrid">'
    '<figure><img src="assets/photos/football-team.jpg" alt="Los Altos football team with helmets raised" loading="lazy">'
    '<figcaption>Four years of football, three on varsity. <a href="leadership.html">What it actually taught me</a>.</figcaption></figure>'
    '<figure><img src="assets/photos/lacrosse-team.jpg" alt="USC men\'s lacrosse team" loading="lazy"></figure>'
    '</div>'
    '<figure class="lead"><img src="assets/photos/barbershop.jpg" '
    'alt="Francis Ruan as a small boy in a barber chair" width="900" height="900" loading="lazy">'
    '<figcaption>First time at the barbershop. Unconvinced.</figcaption></figure>'
    + ask("If you want to be in one of these photographs at some point, that is arranged by email."),
    "Fun")



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
<li><a href="/curiosity.html">Curiosity</a></li><li><a href="/who-am-i.html">Who am I</a></li></ul>
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
