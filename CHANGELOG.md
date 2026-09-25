# Changelog

## 2026-09-25

Stricter ratings. **Automated went from 6 to 2.**

The first version rated a control automated when a tool could check the part of it that is
visible in the package. That overstated it. Automated now means a tool can return PASS or FAIL
for the whole control with no human judgement, and the definition is written into
`coverage.yaml`.

| Control | Was | Now | Why |
|---|---|---|---|
| MASVS-CRYPTO-1 | Automated | Partial | Whether a weak hash or mode is a defect depends on its use. 10 of 13 MASTG tests include a manual step. |
| MASVS-NETWORK-1 | Automated | Partial | Custom certificate validation in app code cannot always be decided statically, and never in a compiled Flutter snapshot. |
| MASVS-PLATFORM-1 | Automated | Partial | An exported component is only a defect if what it exposes is sensitive. 12 of 16 MASTG tests include a manual step. |
| MASVS-PLATFORM-2 | Automated | Partial | A JavaScript bridge is only a defect if the WebView loads content an attacker can influence. |
| MASVS-RESILIENCE-4 | Manual | Partial | Anti-debug and anti-instrumentation code can be detected statically, which is useful evidence. |
| MASVS-PRIVACY-3 | Manual | Partial | Tracker inventories and captured traffic give the evidence; the comparison with the declarations is manual. |

Also added:

- A "why not fully automated" reason for every control.
- Active MASTG v2.0.0 test counts and MAS profiles per control, generated from OWASP's sources.
- `scripts/build.py`, which renders the README tables from the data and fails CI if they
  disagree or if a statement differs from MASVS.
- A section on Flutter apps.

## 2026-09-16

First publication. All 24 MASVS v2.1.0 controls rated: 6 automated, 12 partial, 6 manual.
