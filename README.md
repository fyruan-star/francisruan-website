# francisruan.com

A personal site. Twenty static pages, one typeface (Newsreader), pure white,
charcoal ink. **No JavaScript anywhere**. The horizontal belt on the
index is CSS scroll-snap, not a carousel script.

Live at **https://francisruan.com**.

## Structure

    index.html          the belt. nine frames, pushed sideways. does not scroll vertically.
      |
      |-- my-why.html         two videos and the reason for all of it
      |-- finance.html   -->  trend.html --> thorne / celsius / poppi / vitabiotics / nestle
      |-- curiosity.html      the labelled plate, essays, publications
      |-- building.html  -->  bodi.html, suntag.html, invisible.html
      |-- fight-on.html       the long vignette
      |-- leadership.html
      |-- awards.html         the ruled record
      |-- fun.html
      +-- who-am-i.html

    404.html            served by GitHub Pages at any unmatched path, so every
                        link inside it is root-absolute rather than relative.

## Build

Every page is emitted from one shared chrome. Edit `build-pages.py`, never the
HTML. A rebuild overwrites it.

    python3 build-pages.py        # regenerate all pages
    python3 build-single-file.py  # bundle to dist/ as one portable HTML file
    python3 snapshot.py save      # snapshot to .backups/ before a risky change
    python3 snapshot.py back      # restore the most recent snapshot

`add-origins.py` reinstalls the childhood photographs from `~/Desktop/Baby Photos/`,
stripping the letterbox bars that phone screenshots carry and cropping square with
a per-image bias so nobody's head gets cut off. The bias pairs are in its JOBS table.

## Marks

Real: P&G, PepsiCo, Bain, Nestle (Wikimedia) · Thorne, Vitabiotics, Alani Nu,
Nature's Bounty, Celsius icon (brand sites) · Vuori (rebuilt as a single path) ·
Suntag (vectorised).

Type stand-ins rather than real marks: **BODi, Celsius, Yellow Wood, poppi**.
No clean vector is published for any of them.

## Deployment

GitHub Pages, served from `main` at the repository root.

- `CNAME` binds the apex domain. Do not delete it; Pages reads it on every build.
- `.nojekyll` skips Jekyll processing, which nothing here needs.
- DNS lives at Porkbun: four `A` records and four `AAAA` records at the apex
  pointing to GitHub's Pages anycast addresses, plus a `CNAME` on `www`.
