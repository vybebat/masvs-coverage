"""Count the active OWASP MASTG tests for each MASVS v2.1 control.

    git clone --depth 1 --branch v2.0.0 https://github.com/OWASP/mastg
    git clone --depth 1 --branch v1.0.0 https://github.com/OWASP/maswe
    python scripts/mastg_counts.py mastg maswe > mastg-tests.json

A test is active unless its status is deprecated, placeholder or draft. Its control comes from
`masvs_v2_id` on older tests, or through its `weakness` on newer ones. Newer MASTG tests still
use the MASWE beta numbering, so each weakness is resolved through the `maswe-beta` mapping in
the MASWE v1.0.0 files.

A test's kind is its most human step: `manual` if its type lists manual, else `dynamic` if it
lists dynamic, else `static`. A test mapped to two controls counts for both.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def front_matter(path: Path) -> str:
    m = re.match(r"---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    return m.group(1) if m else ""


def field(fm: str, key: str) -> list[str]:
    m = re.search(rf"^\s*{key}:\s*\[(.*?)\]", fm, re.M)
    if m:
        return [x.strip() for x in m.group(1).split(",") if x.strip()]
    m = re.search(rf"^\s*{key}:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
    if m:
        return re.findall(r"-\s*(\S+)", m.group(1))
    m = re.search(rf"^\s*{key}:\s*(\S+)", fm, re.M)
    return [m.group(1)] if m else []


def main(mastg: Path, maswe: Path) -> dict:
    beta: dict[str, set[str]] = defaultdict(set)
    for p in (maswe / "weaknesses").rglob("MASWE-*.md"):
        fm = front_matter(p)
        controls = field(fm, "masvs-v2")
        for old in field(fm, "maswe-beta"):
            beta[old].update(controls)

    per: dict[str, dict] = defaultdict(lambda: {"tests": [], "kinds": Counter(),
                                                "profiles": Counter()})
    unmapped = []
    for sub in ("tests", "tests-beta"):
        for p in sorted((mastg / sub).rglob("MASTG-TEST-*.md")):
            fm = front_matter(p)
            if (field(fm, "status") or [""])[0] in ("deprecated", "placeholder", "draft"):
                continue
            controls = set(field(fm, "masvs_v2_id"))
            for w in field(fm, "weakness"):
                controls |= beta.get(w, set())
            if not controls:
                unmapped.append(p.stem)
                continue
            types = set(field(fm, "type"))
            kind = ("manual" if "manual" in types else
                    "dynamic" if "dynamic" in types else "static")
            for c in controls:
                e = per[c]
                e["tests"].append(p.stem)
                e["kinds"][kind] += 1
                e["profiles"].update(field(fm, "profiles"))
    return {
        "source": {"mastg": "v2.0.0", "maswe": "v1.0.0"},
        "unmapped": sorted(unmapped),
        "controls": {
            c: {
                "tests": len(e["tests"]),
                "static": e["kinds"]["static"],
                "dynamic": e["kinds"]["dynamic"],
                "manual": e["kinds"]["manual"],
                "profiles": sorted(e["profiles"]),
                "ids": sorted(e["tests"]),
            }
            for c, e in sorted(per.items())
        },
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    json.dump(main(Path(sys.argv[1]), Path(sys.argv[2])), sys.stdout, indent=2)
    print()
