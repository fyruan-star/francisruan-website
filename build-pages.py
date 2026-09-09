#!/usr/bin/env python3
"""Emit every page from one shared chrome. One typeface, pure white, charcoal."""
import pathlib, math
ROOT = pathlib.Path(__file__).parent

# Canonical origin. Open Graph and canonical tags need absolute URLs; relative ones
# do not resolve when a link is unfurled by LinkedIn, iMessage, Slack.
SITE = "https://francisruan.com"

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,500;1,6..72,600&display=swap" rel="stylesheet">')
ICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' "
        "viewBox='0 0 100 100'><text y='.9em' font-size='90' font-family='Newsreader,Georgia,serif' fill='%231C1C1C'>F</text></svg>\">")

def topbar(active=""):
    items=[("index.html","Index"),("my-why.html","My Why"),("fight-on.html","Fight On"),
           ("finance.html","Finance"),("leadership.html","Leadership"),("building.html","Building"),
           ("curiosity.html","Curiosity"),("fun.html","Fun"),("awards.html","Awards"),
           ("who-am-i.html","Who am I"),("Ruan_Francis_Resume.pdf","Resume")]
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
  # One word where one word will do. The plate carries the feeling, the title only
  # has to name the door. Why opens, I closes.
  ("my-why-title-sq.jpg",      "Why",        "my-why.html"),
  ("fight-on-sq.jpg",          "Fight On",   "fight-on.html"),
  ("origin-relationships.jpg", "Finance",    "finance.html"),
  ("origin-curiosity.jpg",     "Curiosity",  "curiosity.html"),
  ("origin-engineer.jpg",      "Built",      "building.html"),
  ("origin-leadership.jpg",    "Leadership", "leadership.html"),
  ("awards.jpg",               "Awards",     "awards.html"),
  ("origin-fun.jpg",           "Fun",        "fun.html"),
  ("who-am-i-sq.jpg",          "I",          "who-am-i.html"),
]

TRACKS = {
  "my-why.html":    ("Cool",              "Daniel Caesar"),
  "fight-on.html":  ("Hold On",           "Alabama Shakes"),
  "leadership.html":("Ivy",               "Frank Ocean"),
  "finance.html":   ("Cantaloupe Island", "Herbie Hancock"),
  "curiosity.html": ("Lujon",             "Henry Mancini"),
  "building.html":  ("Electric Feel",     "MGMT"),
  "awards.html":    ("Golden",            "Harry Styles"),
  "fun.html":       ("Sundown",           "LEISURE"),
  "who-am-i.html":  ("Orange Blood",      "Mt Joy"),
  "trend.html":     ("Cantaloupe Island", "Herbie Hancock"),
  "invisible.html": ("Lujon",             "Henry Mancini"),
}

def soundtrack(fn):
    t = TRACKS.get(fn)
    if not t: return ""
    title, artist = t
    from urllib.parse import quote
    q = quote(f"{title} {artist}")
    return ('<div class="track"><span class="track__note" aria-hidden="true">&#9834;</span>'
            '<span class="track__k">Please play while reading</span>'
            f'<a class="track__l" href="https://open.spotify.com/search/{q}" target="_blank" rel="noopener">'
            f'<em>{title}</em>, {artist}</a></div>')

def ask(line="If any of this is worth an argument, I would like to have it."):
    return ('<div class="ask"><p>' + line +
            ' <a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a></p></div>')

def brick(fname, label, href):
    p = ROOT / "assets" / "photos" / fname
    img = f'<img src="assets/photos/{fname}" alt="">' if p.exists() else ""
    return (f'<a class="brick" href="{href}"><span class="brick__img">{img}</span>'
            f'<span class="brick__k">{label}</span></a>')

def belt():
    """Stripe Press stacks its books down a void. This is that, upright, and built as
    an index: numbered, ruled, one word to a door. Scroll-snap on the y axis, and as
    with the rest of this site there is no JavaScript in it."""
    rows = []
    for i, (fname, label, href) in enumerate(PYRAMID, 1):
        p = ROOT / "assets" / "photos" / fname
        img = f'<img src="assets/photos/{fname}" alt="" loading="lazy">' if p.exists() else ""
        rows.append(
            f'<a class="frame" href="{href}">'
            f'<span class="frame__n">{i:02d}</span>'
            f'<span class="frame__img">{img}</span>'
            f'<span class="frame__k">{label}</span>'
            f'<span class="frame__go" aria-hidden="true">&rarr;</span>'
            f'</a>')
    rows.append(
        '<div class="frame frame--end">'
        '<span class="frame__n">&mdash;</span>'
        '<span class="frame__k">Say something</span>'
        '<span class="frame__links">'
        '<a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a>'
        '<a href="https://www.linkedin.com/in/francisruan" target="_blank" rel="noopener">LinkedIn</a>'
        '<a href="Ruan_Francis_Resume.pdf" target="_blank" rel="noopener">Resume</a>'
        '</span></div>')
    return ('<div class="beltwrap">'
            f'<div class="belt">{"".join(rows)}</div>'
            '<p class="belt__hint">Nine ways in &middot; scroll &darr;</p>'
            '</div>')

INDEX = f"""<div class="cover">

  <div class="cover__side">
    <div class="mast">
      <img class="mast__face" src="assets/photos/headshot.jpg" alt="Francis Ruan" width="892" height="1400">
      <div class="mast__id">
        <h1>Francis Ruan</h1>
      </div>
    </div>

    <div class="marks">
      <p class="marks__k">Where the time goes</p>
      <ul class="marks__row">
        <li><img class="mk mk--usc"   src="assets/logos/uscmarshall.png" alt="USC Marshall"></li>
        <li><img class="mk mk--vuori" src="assets/logos/vuori.svg"       alt="Vuori"></li>
        <li><img class="mk mk--bodi"  src="assets/logos/bodi.svg"        alt="BODi"></li>
        <li><img class="mk mk--porto" src="assets/logos/elporto.png"     alt="El Porto Surfboards"></li>
      </ul>
    </div>

    <div class="cover__foot">
      <a href="mailto:fyruan@usc.edu">fyruan@usc.edu</a>
      <a href="https://www.linkedin.com/in/francisruan" target="_blank" rel="noopener">LinkedIn</a>
      <a href="Ruan_Francis_Resume.pdf" target="_blank" rel="noopener">Resume</a>
    </div>
  </div>

  {belt()}
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
  # label, marker x, y, which side the label sits on
  ("Creative writing",            452, 152, "L"),
  ("Education &amp; attention",   372, 210, "L"),
  ("Inequality",                  360, 262, "L"),
  ("Interface design",            420, 296, "L"),
  ("Comedy &amp; timing",         318, 352, "L"),
  ("Mandarin",                    300, 404, "L"),
  ("Finance &amp; valuation",     556, 132, "R"),
  ("Consumer M&amp;A",            632, 176, "R"),
  ("Decision making under stress",660, 240, "R"),
  ("Self-quantification",         648, 290, "R"),
  ("Physiology &amp; recovery",   632, 336, "R"),
  ("Endurance",                   578, 428, "R"),
]

def brain(w=1180, h=620):
    ink, line = "var(--ink)", "var(--trust)"
    o = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="bt bd">',
         '<title id="bt">A diagram of what I am curious about</title>',
         '<desc id="bd">A head in profile, labelled the way an anatomical plate is, '
         'with twelve areas of interest instead of anatomy.</desc>',
         f'<g fill="none" stroke="{line}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">']
    # skull and face, facing left
    o.append('<path d="M520 62 C400 64 320 146 305 232 C300 256 292 266 285 276 '
             'C268 298 250 324 248 340 C247 352 262 356 278 360 C288 362 286 372 282 380 '
             'C279 388 288 394 296 398 C289 404 285 412 288 420 C292 436 305 452 322 462 '
             'C345 476 372 486 400 496 C420 504 432 520 436 548 L444 596 L666 596 '
             'C670 536 674 476 678 426 C696 376 706 296 692 226 C678 146 610 70 520 62 Z"/>')
    # brain mass
    o.append('<path d="M340 238 C340 148 420 102 510 102 C600 102 666 148 669 233 '
             'C671 273 651 298 611 303 C541 310 431 308 376 298 C349 290 338 268 340 238 Z"/>')
    o.append(f'</g><g fill="none" stroke="{line}" stroke-width="1.05" stroke-opacity=".75" stroke-linecap="round">')
    # gyri
    for d in ["M362 232 C398 200 452 196 486 224 C516 248 556 246 584 220",
              "M356 268 C400 244 456 244 492 268 C528 292 580 288 614 262",
              "M380 292 C420 274 470 274 508 292 C544 308 588 306 620 288",
              "M392 178 C428 152 486 148 522 172 C556 194 606 190 636 166",
              "M420 138 C452 118 500 116 532 134"]:
        o.append(f'<path d="{d}"/>')
    o.append("</g>")
    # cerebellum and stem
    o.append(f'<g fill="none" stroke="{line}" stroke-width="1.4"><circle cx="632" cy="336" r="40"/>'
             '<path d="M560 300 C566 340 570 392 578 428 C582 450 584 470 582 492"/></g>')
    o.append(f'<g fill="none" stroke="{line}" stroke-width=".8" stroke-opacity=".65">'
             '<path d="M600 320 C616 330 640 334 664 330"/><path d="M600 344 C618 350 642 352 666 346"/>'
             '<path d="M606 362 C622 368 642 368 660 362"/></g>')

    left  = [c for c in CURIOSITIES if c[3] == "L"]
    right = [c for c in CURIOSITIES if c[3] == "R"]
    o.append(f'<g font-family="var(--f-agate)" font-size="13" fill="{ink}">')
    o.append(f'<g stroke="{ink}" stroke-width=".9" fill="none" stroke-opacity=".55">')
    lines, labels, dots = [], [], []
    for side, group in (("L", left), ("R", right)):
        n = len(group)
        span = h - 190
        for i, (lab, mx, my, _) in enumerate(group):
            ly = 108 + (span / max(n - 1, 1)) * i
            lx = 214 if side == "L" else w - 214
            elbow = 262 if side == "L" else w - 262
            lines.append(f'<path d="M{mx} {my} L{elbow} {ly} L{lx + (14 if side=="L" else -14)} {ly}"/>')
            anc = "end" if side == "L" else "start"
            tx = lx if side == "L" else lx
            labels.append(f'<text x="{tx}" y="{ly + 4}" text-anchor="{anc}">'
                          f'<tspan font-weight="600">{i + 1 + (0 if side=="L" else len(left))}.</tspan>'
                          f'<tspan dx="6">{lab}</tspan></text>')
            dots.append(f'<circle cx="{mx}" cy="{my}" r="3.4" fill="{ink}" stroke="none"/>')
    o += lines
    o.append("</g>")
    o += dots
    o += labels
    o.append("</g></svg>")
    return "".join(o)


CURIO = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">Intellectual curiosity</p>
  <h1>A Plate of What I Am Curious About</h1>
</header>
<div class="body">
{soundtrack("curiosity.html")}
<p class="kicker">Anatomical plates label a head by what each part does. This one labels it by what I keep going back to. The placements are a conceit. The list is not.</p>

<div class="brainwrap">{brain()}</div>

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

<p>Same aisle. In some stores, genuinely the same shelf. Seven times the price.</p>

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
    ("TEDx Speaker", "<em>Why You Should Make a Done List</em>. Not recorded"),
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
  <p class="eyebrow">Awards</p>
  <h1>Everything, on One Page</h1>
  <p class="meta"><span>Los Altos High School, 2021 to 2025</span><span>USC, 2025 to present</span></p>
</header>
<div class="body">
  {soundtrack("awards.html")}
  <figure class="lead">
    <img src="assets/photos/awards.jpg" alt="Francis Ruan as a boy, arms raised on a school blacktop" width="900" height="900">
    <figcaption>Awards. The reaction has not really changed.</figcaption>
  </figure>
  {record()}
  {ask("If you want the story behind any one of these, ask me about it.")}
</div>
<nav class="nextprev"><a href="fight-on.html">How most of these actually happened &rarr;</a><a href="index.html">Index</a></nav>
</div>"""

page("awards.html","Awards | Francis Ruan",
     "Francis Ruan's record: valedictorian, TEDx speaker, Stanford ProCo, USC Presidential and Morgan Stanley scholarships, Dean's List.",
     HON, active="Awards")
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
<p class="kicker">The through-line in all of this is one stubborn question: where does value sit when the accounts cannot see it?</p>

<p>It shows up in a supplement aisle that cleared at six times revenue and at one, eight weeks apart. It shows up in a finance workflow whose entire saving is invisible on a balance sheet. It is the same question wearing different clothes, and I have not got to the bottom of it yet, which is precisely why I keep going.</p>

<p>It runs in three places, and they feed each other. The study is where I do the arithmetic. The paper is where I have to defend it in public. The show is where I go and ask the people it is happening to.</p>

<div class="cats">
  <a class="cat" href="#study">
    <span class="cat__n">01</span>
    <span class="cat__k">The study</span>
    <span class="cat__t">Five deals, six weeks, a sevenfold spread</span>
    <span class="cat__d">Five consumer wellness businesses changed hands this summer at prices seven times apart. I plotted them and worked out what each buyer was really paying for.</span>
    <span class="cat__go" aria-hidden="true">&darr;</span>
  </a>
  <a class="cat" href="#paper">
    <span class="cat__n">02</span>
    <span class="cat__k">The paper</span>
    <span class="cat__t">What I have put in writing</span>
    <span class="cat__d">Two long pieces: the argument behind the deal spread, and an essay on the assets an AI deployment builds that never reach the balance sheet.</span>
    <span class="cat__go" aria-hidden="true">&darr;</span>
  </a>
  <a class="cat" href="#show">
    <span class="cat__n">03</span>
    <span class="cat__k">The show</span>
    <span class="cat__t">Wall Street&rsquo;s Trojan Horse</span>
    <span class="cat__d">A podcast in progress about how quietly AI already walked into investment banking, told by the analysts living it and the people who built it.</span>
    <span class="cat__go" aria-hidden="true">&darr;</span>
  </a>
</div>

<h2 id="study">The study</h2>
<p>Five consumer wellness businesses changed hands in six weeks this summer at prices seven times apart. I plotted them, worked out what each buyer was really paying for, and wrote a note on each.</p>
{dealgrid()}
<p><a href="trend.html"><strong>Read the full argument</strong></a>, including the chart and where I think I am wrong.</p>

<h2 id="paper">The paper</h2>
<p>Everything above is only worth something if I am willing to write it down where somebody can disagree with me. These are the two pieces I would defend.</p>
<div class="biglinks">
  <a href="trend.html"><span class="bl__lg"></span><span class="bl__n">Five Deals, Six Weeks, and a Sevenfold Spread</span><span class="bl__note">The full argument, the chart, the five notes, and the part where I say what would prove me wrong.</span></a>
  <a href="invisible.html"><span class="bl__lg"></span><span class="bl__n">The Assets AI Builds That Nobody Records</span><span class="bl__note">The essay that came out of the BODi work. The best output of a deployment never lands on the balance sheet.</span></a>
</div>
<h3>Where the operating work happened</h3>
<div class="biglinks">
  <a href="bodi.html"><span class="bl__lg"><img src="assets/logos/bodi.svg" alt=""></span><span class="bl__n">BODi</span><span class="bl__note">Ninety minutes to three. $784K sized and presented to the MD of Accounting.</span></a>
</div>

<h2 id="show">The show</h2>
<div class="podcast">
  <img class="podcast__art" src="assets/logos/podcast-cover.svg" alt="Wall Street&rsquo;s Trojan Horse, placeholder cover">
  <div class="podcast__body">
    <p class="podcast__k">Wall Street&rsquo;s Trojan Horse &middot; a podcast, in progress</p>
    <p>A show about how quietly AI has already walked into investment banking. Not the version in the headlines, with the press releases and the transformation decks. The version where a first-year analyst stops doing four hours of work on a Tuesday and mentions it to nobody.</p>
    <p>I am collecting perspectives from two groups: first-year analysts who are living inside the change, and the people building the tools that caused it. They describe the same event in almost completely different language, and the distance between those two accounts is the actual show.</p>
    <p class="quiet">Artwork and first episodes to come. If you are a first-year analyst, or you build these tools, I would like to record with you.</p>
  </div>
</div>
{ask("If you work in a bank and have watched this happen from the inside, come on the show.")}
</div>
<nav class="nextprev"><a href="trend.html">The deal essay &rarr;</a><a href="index.html">Index</a></nav>
</div>"""

page("finance.html","Finance | Francis Ruan",
     "Deal analysis, operating finance, and a podcast in progress about AI's quiet arrival inside investment banking.",
     FIN, active="Finance")
print("finance.html")

# ================================================================= HUBS =====
def hub(fn, eyebrow, title, lede, blocks, active):
    if 'class="ask"' not in blocks:
        blocks = blocks + ask()
    body = f"""<div class="wrap">
<header class="phead">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{title}</h1>
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
    biglinks([("bodi.html","bodi.svg","BODi","Ninety minutes to three. $784K sized and presented."),
              ("suntag.html","suntag.svg","Suntag Co.","$5,000 pre-seed, 300+ waitlist, and a pricing call I got wrong.")])

    + '<h2>USC Marshall, AI Builder Hub</h2>'
    + '<div class="biglinks">'
      '<a href="https://github.com/fyruan-star/usc-catalogue-scraper" target="_blank" rel="noopener">'
      '<span class="bl__lg"><img src="assets/logos/uscmarshall.png" alt="USC Marshall"></span>'
      '<span class="bl__n">AI Builder Hub Engineer</span>'
      '<span class="bl__note">One of four student engineers. Reverse engineered the course '
      'registration system used by 45,185 students.</span></a>'
      '</div>'
    + '<p>The piece that is public is the scraper underneath it: a collector that pulls one plain-text '
      'file per undergraduate programme out of USC&rsquo;s online catalogue, which is the input a degree '
      'requirements validator needs and which nobody had bothered to build. It parses <strong>470</strong> '
      'programme descriptions and feeds a rules engine that checks a student&rsquo;s courses against what '
      'their degree actually demands.</p>'
    + '<p><a href="https://github.com/fyruan-star/usc-catalogue-scraper" target="_blank" rel="noopener">'
      'github.com/fyruan-star/usc-catalogue-scraper</a></p>'

    + '<h2>Also running</h2>'
    + '<div class="biglinks">'
      '<a href="#" class="bl--flat"><span class="bl__lg"></span>'
      '<span class="bl__n">Los Altos Vintage</span>'
      '<span class="bl__note">Founded and operating. One line of detail still to come from me.</span></a>'
      '<a href="#" class="bl--flat"><span class="bl__lg"></span>'
      '<span class="bl__n">Elevated Youth</span>'
      '<span class="bl__note">Founded and operating. One line of detail still to come from me.</span></a>'
      '</div>'

    + '<p style="margin-top:2rem">The write-up that came out of the BODi work is '
      '<a href="invisible.html">here</a>. It argues that the most valuable thing you build with AI never '
      'lands on the balance sheet.</p>',
    "Building")

hub("my-why.html", "My why", "My Mother Works Nights",
    "",
    '<div class="videos">'
    '<figure><video controls preload="metadata" playsinline poster="assets/video/mom-1-poster.jpg">'
    '<source src="assets/video/mom-1.mp4" type="video/mp4">Your browser cannot play this video.</video></figure>'
    '<figure><video controls preload="metadata" playsinline poster="assets/video/mom-2-poster.jpg">'
    '<source src="assets/video/mom-2.mp4" type="video/mp4">Your browser cannot play this video.</video></figure>'
    '</div>'

    '<p class="kicker">I want to be careful how I tell this, because there is a version of it that turns '
    'my mother into a lesson, and she is not a lesson.</p>'

    '<p>She is a woman who comes home a little after seven in the morning smelling faintly of hand sanitizer, '
    'who will not go to bed until she has asked me at least two questions about my week, and who holds an '
    'unshakeable and entirely evidence-free confidence that both her sons are going to be fine. She is sixty-three. '
    'She has raised us on her own the entire time. Her friends are mostly in China, which in practice means '
    'her friends are mostly a phone screen at inconvenient hours.</p>'

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
    "My Why")

LOVES = [
  ("Little Women", "Greta Gerwig, 2019", "film", "little-women",
   "The first time a film made me feel like I was inside a sisterhood. I did not know a boy was "
   "allowed to feel that and it genuinely rearranged something. I have watched it more times than "
   "I am going to admit in writing."),
  ("A River Runs Through It", "Robert Redford, 1992", "film", "river-runs",
   "A film about fly fishing and a family that is really a film about how to love the ordinary. "
   "No yachts. No parties. Nobody performing a life for anybody. Set that against the version of "
   "living we are all shown now and it is almost radical."),
  ("Pride and Prejudice", "Jane Austen, 1813", "book", "pride-prejudice",
   "Elizabeth Bennet does not settle for good and does not settle for great. She holds out for the "
   "correct one and takes the social cost of holding out. That is the whole book to me."),
  ("The Notebook", "Nick Cassavetes, 2004", "film", "notebook",
   "I will not be defending this. I do not need to."),
  ("Ten Things I Hate About You", "Gil Junger, 1999", "film", "ten-things",
   "The poem at the end. Every single time."),
]

def loves():
    """Five plates. The book is its own 1813 title page, which is public domain and a
    better object than any modern cover; the films are their release posters."""
    out = ['<div class="loves">']
    for title, credit, kind, slug, note in LOVES:
        out.append(f'<figure class="love">'
                   f'<span class="love__art"><img src="assets/loves/{slug}.jpg" alt="{title}" loading="lazy"></span>'
                   f'<figcaption class="love__cap">'
                   f'<span class="love__kind">{kind}</span>'
                   f'<span class="love__t">{title}</span>'
                   f'<span class="love__c">{credit}</span>'
                   f'<span class="love__n">{note}</span>'
                   f'</figcaption></figure>')
    out.append("</div>")
    return "".join(out)

hub("who-am-i.html", "So who is Francis", "So Who Is Francis?",
    "",
    '<div class="videos videos--one">'
    '<figure><video controls preload="metadata" playsinline poster="assets/video/homecoming-poster.jpg">'
    '<source src="assets/video/homecoming.mp4" type="video/mp4">Your browser cannot play this video.</video>'
    '<figcaption>Homecoming court.</figcaption></figure>'
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

    '<h2>Three things that explain me faster than I can</h2>'
    + loves() +
        '<h2>I am a lover boy and I am not embarrassed about it</h2>'
    '<p>I am a poet before I am an analyst. I like the beach, I like reflecting, I like feeling things '
    'deeply and then going and finding somebody to talk about it with. Romance films work on me every '
    'single time and I have stopped pretending to be above them.</p>'
    '<p>And I have very specific instructions about how to treat somebody, because my mother taught them '
    'to me and she did not present them as optional. Buy the flowers, for no occasion. Say the compliment '
    'out loud instead of thinking it. Never go to bed upset, not once, no matter how late it makes the '
    'night. Open the door, every time, forever.</p>'
    '<p>And when something goes wrong, do the harder thing: sit down and work out whether this is actually '
    'a you problem, because it very often is, and it is almost never only a you problem either. It is a '
    'we. Take the accountability all the way to the bottom of it, past the point where it stops feeling '
    'good, and then keep going a little further.</p>'

    '<h2>And I am also the other thing</h2>'
    '<p>I look up to bodybuilders. I watch a genuinely unreasonable amount of NFL. I was a captain on a '
    'football team and I am the person yelling in the huddle, and I like being that person, and I do not '
    'think it is in tension with any of the paragraph above.</p>'
    '<p>That is the whole point I am making. Those are supposed to be different men. They are not.</p>'

    '<h2>Things I will read about until three in the morning</h2>'
    '<p>Human pathogenesis. Biology and anatomy, mechanism-first, always. I keep profiles on myself and '
    'run bloodwork against them, which sounds clinical and is actually just curiosity pointed inward.</p>'
    '<p>Then: human history. Archaeology. Ancient civilizations. What people did before they had any of '
    'this. I was an absolutely insufferable dinosaur child and I have simply redirected it.</p>'
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
    "Who am I")

hub("fight-on.html", "Fight on", "Nobody Came Until Nine",
    "",
    '<figure class="lead"><img src="assets/photos/fight-on.jpg" '
    'alt="Francis Ruan as a young boy, grinning, holding up a peace sign" width="1200" height="1600">'
    '<figcaption>Roughly the era in question.</figcaption></figure>'

    '<p class="kicker">School let out at three. My mother&rsquo;s shift did not end when other people&rsquo;s '
    'shifts ended, so most days I had six hours to fill and no phone to fill them with, which meant I had '
    'six hours and a campus.</p>'

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

    '<h2>What it meant on the way home</h2>'

    '<p>When practice ended and the parents pulled up in that long patient line, I ran. My friend&rsquo;s house '
    'was about a mile. I ran it in cleats more than once. A ride was a thing you had to ask for, and asking was '
    'the single currency I was most careful with, so I spent my legs instead.</p>'

    '<h2>The honest inventory</h2>'

    '<p>Roughly in order:</p>'

    '<p>I could not swim. Not slow at it, could not do it. Swimming lessons are something you pay for.</p>'

    '<p>I could not play spikeball, and I was laughed at for that repeatedly, by people who were not being '
    'cruel so much as accurate. I am now the best spikeball player I know. I would like that on the record. '
    'It took an absurd number of hours and I regret none of them.</p>'

    '<p>I was fat, and I was told so, in the specific unhurried way children tell each other things.</p>'

    '<p>I had never played a down of football, and I signed up anyway, and I was put on the ground for about '
    'two years without meaningful interruption.</p>'

    '<p>I picked up a lacrosse stick for the first time at a tryout, in front of people who had been holding '
    'one since they were eight, and the sound a group makes when it watches you fail at something easy is not '
    'a sound you forget.</p>'

    '<p>Teachers wrote me down. More than one decided early that I was a troublemaker and then stopped updating '
    'the file. I was not a troublemaker. I was a kid with six unsupervised hours who talked too much, because '
    'talking was the only thing available that was free.</p>'

    '<p>And my father was not a factor in any of this in the way that fathers are supposed to be.</p>'

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

    '<p>It means nobody is coming to make this easier, and you go anyway, and you go cheerfully, because '
    'bitterness is enormously heavy and I could never afford to carry any.</p>'

    '<p>There is a version of this story where the boy is bitter, and I understand how you get there. All the '
    'ingredients are present. But I have met bitter people and they are so tired, and being tired is the one '
    'thing my mother never got to be, so it always felt like a strange thing to spend her money on.</p>'

    '<p>I did not learn to fight on at USC. I learned it in a schoolyard at nine at night with a piece of '
    'chalk and nobody watching. USC only gave me the words for it, and I was glad to finally have them, '
    'because I had been doing the thing for about twelve years without knowing what to call it.</p>'
    + ask("If any of this sounds like your childhood too, I would like to hear from you."),
    "Fight On")

hub("leadership.html", "Greatest leadership", "The Sideline Is a Vantage, Not a Consolation",
    "",
    '<figure class="lead"><img src="assets/photos/origin-leadership.jpg" '
    'alt="Francis Ruan as a boy dressed as George Washington" width="900" height="900">'
    '<figcaption>An early and unsubtle interest in standing in front of people.</figcaption></figure>'

    '<p class="kicker">Everyone on that field was bigger than me, and I have come to think of that as one of '
    'the luckier things that has happened to me.</p>'

    '<p>I was undersized. I was one of very few Asian kids in the program. I had never played a down in my life '
    'when I signed up freshman year, and my friends told me, kindly and often, that I was the worst guy out '
    'there. They were not being cruel. They were being accurate. I was nowhere near a starter for a long time '
    'and I never became the story, and for about two years I found that genuinely painful in the small daily '
    'way that things are painful when you are fifteen.</p>'

    '<p>Then something better happened, which is that I stopped watching the ball.</p>'

    '<h2>What you can see from four feet off the field</h2>'

    '<p>A player sees his assignment. He sees the man across from him and the next two seconds, and that '
    'narrowness is not a failing, it is the entire job, and the good ones protect it fiercely. But somebody has '
    'to be looking at the whole thing. Somebody has to notice that the left tackle has gone quiet since the '
    'second quarter. That the safety is pressing because he is angry, not because the coverage asked him to. '
    'That the sophomores have stopped talking to each other, which is always, always the first sign.</p>'

    '<p>Nobody assigns you that. You just start doing it, and one day you realize you have been doing it for '
    'months, and that it is a kind of work.</p>'

    '<h2>People arrive one at a time</h2>'

    '<p>A team is not a unit. It is forty separate difficult conversations wearing the same color. The corner '
    'who just got beaten deep does not want a speech, he wants somebody to sit down next to him and say nothing '
    'for a minute while the humiliation finishes moving through him. The lineman who is furious needs to be '
    'furious somewhere else first, before he says the sentence he will not be able to take back.</p>'

    '<p>I got good at working out which of those I had in front of me before I opened my mouth. That skill has '
    'turned out to be worth more than anything I learned in a weight room, and I use it roughly every day.</p>'

    '<h2>Monday is the whole job</h2>'

    '<p>Losing is not the hard part. Friday is loud and then it ends. Monday is quiet and it does not. Getting '
    'forty people who were humiliated in front of their families to come back and run it again, properly, in '
    'the cold, when nothing has changed except that they now hold evidence they are not as good as they hoped, '
    'is the actual work of leading anything at all.</p>'

    '<p>Anybody is useful when it is going well. I got very good at Mondays, and I have never once regretted it.</p>'

    '<h2>The game is bigger than the player</h2>'

    '<p>This is the one that rearranged me. My snap count was never going to be the story, and I spent two '
    'years letting that fact make me smaller. Then it simply stopped mattering, the way things sometimes do, '
    'without ceremony. Once I quit measuring my worth in reps I became far more useful, because I could finally '
    'see the entire field instead of my own small rectangle of it.</p>'

    '<p>There is a real freedom in working out that you are not the protagonist. It hands you back every bit of '
    'attention you had been spending on yourself, and there is a great deal of it, and you can spend it on '
    'almost anything.</p>'

    '<p class="pull">They voted me team captain. I did not play much.</p>'

    '<p>I think about that more than any award I have, because it is the only one I did not get by being good '
    'at something. The spotlight and the leadership turned out to be two different jobs, and plenty of people '
    'holding one never hold the other. You do not need the ball to carry a squad. You need to be the person '
    'everybody looks at when it goes badly, and you need to have decided, well before it goes badly, exactly '
    'what you intend to be like when it does.</p>'

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

    '<p>Keep the expenses near zero. Collect the crumbs on purpose. That is the whole method, and it has '
    'never let me down on a Tuesday.</p>'

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
