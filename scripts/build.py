"""Validate coverage.yaml and render the README tables from it.

    python scripts/build.py            rewrite the generated parts of README.md
    python scripts/build.py --check    fail if README.md is stale or the data is inconsistent
    python scripts/build.py --check --upstream path/to/masvs
                                       also compare every statement with OWASP MASVS

Needs PyYAML.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("automated", "partial", "manual")
GROUPS = {
    "MASVS-STORAGE": "Storage",
    "MASVS-CRYPTO": "Cryptography",
    "MASVS-AUTH": "Authentication and Authorization",
    "MASVS-NETWORK": "Network Communication",
    "MASVS-PLATFORM": "Platform Interaction",
    "MASVS-CODE": "Code Quality",
    "MASVS-RESILIENCE": "Resilience Against Reverse Engineering and Tampering",
    "MASVS-PRIVACY": "Privacy",
}
FIELDS = ("id", "group", "statement", "automation", "method", "why")


def validate(cov: dict, mastg: dict, upstream: Path | None) -> list[str]:
    errors = []
    controls = cov["controls"]
    ids = [c["id"] for c in controls]
    if len(ids) != 24 or len(set(ids)) != 24:
        errors.append(f"expected 24 unique controls, found {len(set(ids))}")
    for c in controls:
        for f in FIELDS:
            if not str(c.get(f, "")).strip():
                errors.append(f"{c.get('id')}: missing {f}")
        if c.get("automation") not in LEVELS:
            errors.append(f"{c['id']}: automation must be one of {LEVELS}")
        if c.get("group") not in GROUPS or not c["id"].startswith(c["group"] + "-"):
            errors.append(f"{c['id']}: bad group {c.get('group')}")
        for f in FIELDS:
            if "—" in str(c.get(f, "")):
                errors.append(f"{c['id']}: em dash in {f}")
    counts = Counter(c["automation"] for c in controls)
    for level in LEVELS:
        if cov["summary"][level] != counts[level]:
            errors.append(f"summary.{level} is {cov['summary'][level]}, rows say {counts[level]}")
    if cov["summary"]["total"] != len(controls):
        errors.append("summary.total does not match the number of rows")
    for cid in mastg["controls"]:
        if cid not in ids:
            errors.append(f"mastg-tests.json names unknown control {cid}")
    if upstream:
        for c in controls:
            text = (upstream / "controls" / f"{c['id']}.md").read_text(encoding="utf-8")
            m = re.search(r"## Control\s+(.+?)\n", text)
            if not m or m.group(1).strip() != c["statement"]:
                errors.append(f"{c['id']}: statement differs from upstream MASVS")
    return errors


def _tests(m: dict | None) -> str:
    if not m:
        return "none"
    parts = [f"{m[k]} {k}" for k in ("static", "dynamic", "manual") if m[k]]
    return f"{m['tests']} ({', '.join(parts)})"


def _profiles(m: dict | None) -> str:
    if not m:
        return "-"
    return ", ".join(f"MAS-{p}" for p in m["profiles"])


def render(cov: dict, mastg: dict) -> dict[str, str]:
    controls = cov["controls"]
    counts = Counter(c["automation"] for c in controls)
    blocks = {}

    rows = ["| Automation | Controls | Meaning |", "|---|---|---|"]
    for level in LEVELS:
        rows.append(f"| {level.capitalize()} | {counts[level]} | "
                    f"{' '.join(cov['levels'][level].split())} |")
    blocks["COUNT"] = "\n".join(rows)

    rows = ["| Group | Controls | Automated | Partial | Manual | Active MASTG tests |",
            "|---|---|---|---|---|---|"]
    for g, name in GROUPS.items():
        cs = [c for c in controls if c["group"] == g]
        n = Counter(c["automation"] for c in cs)
        # A test mapped to two controls of the same group is counted once here.
        tests = len({t for c in cs for t in mastg["controls"].get(c["id"], {}).get("ids", [])})
        rows.append(f"| {g} - {name} | {len(cs)} | {n['automated']} | {n['partial']} | "
                    f"{n['manual']} | {tests} |")
    blocks["GROUPS"] = "\n".join(rows)

    rows = ["| Control | Statement | Automation | How it is verified | Why not fully automated "
            "| Active MASTG tests | Profiles |",
            "|---|---|---|---|---|---|---|"]
    for c in controls:
        m = mastg["controls"].get(c["id"])
        why = c["why"] if c["automation"] != "automated" else f"({c['why']})"
        rows.append(f"| `{c['id']}` | {c['statement']} | {c['automation'].capitalize()} | "
                    f"{c['method']} | {why} | {_tests(m)} | {_profiles(m)} |")
    blocks["CONTROLS"] = "\n".join(rows)
    return blocks


def apply(readme: str, blocks: dict[str, str]) -> str:
    for name, body in blocks.items():
        pattern = re.compile(rf"(<!-- BEGIN {name} -->\n).*?(<!-- END {name} -->)", re.S)
        if not pattern.search(readme):
            raise SystemExit(f"README.md has no {name} markers")
        readme = pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), readme)
    return readme


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--upstream", type=Path)
    args = ap.parse_args()
    cov = yaml.safe_load((ROOT / "coverage.yaml").read_text(encoding="utf-8"))
    mastg = json.loads((ROOT / "mastg-tests.json").read_text(encoding="utf-8"))
    errors = validate(cov, mastg, args.upstream)
    if errors:
        sys.exit("\n".join(errors))
    path = ROOT / "README.md"
    current = path.read_text(encoding="utf-8")
    wanted = apply(current, render(cov, mastg))
    if args.check:
        if wanted != current:
            sys.exit("README.md is stale. Run: python scripts/build.py")
        print("ok: 24 controls, README in sync")
    else:
        path.write_text(wanted, encoding="utf-8", newline="\n")
        print("README.md updated")


if __name__ == "__main__":
    main()
