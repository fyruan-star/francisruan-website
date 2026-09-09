#!/usr/bin/env python3
"""
Version safety net.

  python3 snapshot.py save  "note"   take a snapshot of the current site
  python3 snapshot.py list            show snapshots, newest first
  python3 snapshot.py back            restore the most recent snapshot
  python3 snapshot.py back 3          restore snapshot number 3 from the list

Snapshots live in .backups/ and cover every source file: html, css, the build
scripts and assets. Restoring writes the files back and leaves a snapshot of
what it replaced, so "back" is itself undoable.
"""
import sys, shutil, pathlib, datetime, json

ROOT = pathlib.Path(__file__).parent
BAK = ROOT / ".backups"
SKIP = {".backups", "dist", "archive-editorial", "__pycache__", ".git"}
KEEP_SUFFIX = {".html", ".css", ".py", ".md", ".pdf", ".svg", ".png", ".jpg", ".jpeg"}


def files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        if p.suffix.lower() in KEEP_SUFFIX:
            yield rel


def save(note=""):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = BAK / stamp
    n = 0
    for rel in files():
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, out)
        n += 1
    (dest / "_note.json").write_text(json.dumps({"note": note, "files": n, "at": stamp}), encoding="utf-8")
    print(f"saved {n} files -> .backups/{stamp}  {note}")
    return stamp


def snaps():
    if not BAK.exists():
        return []
    return sorted([d for d in BAK.iterdir() if d.is_dir()], reverse=True)


def show():
    s = snaps()
    if not s:
        print("no snapshots yet")
        return
    for i, d in enumerate(s, 1):
        meta = {}
        f = d / "_note.json"
        if f.exists():
            meta = json.loads(f.read_text())
        print(f"  {i}. {d.name}  {meta.get('files','?')} files  {meta.get('note','')}")


def back(which=1):
    s = snaps()
    if not s:
        sys.exit("no snapshots to restore")
    if which > len(s):
        sys.exit(f"only {len(s)} snapshots exist")
    src = s[which - 1]
    save(f"auto: state replaced by restore of {src.name}")
    n = 0
    for p in src.rglob("*"):
        if not p.is_file() or p.name == "_note.json":
            continue
        rel = p.relative_to(src)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)
        n += 1
    print(f"restored {n} files from {src.name}")


cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
if cmd == "save":
    save(" ".join(sys.argv[2:]))
elif cmd == "list":
    show()
elif cmd == "back":
    back(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
else:
    sys.exit(__doc__)
