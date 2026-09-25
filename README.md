# MASVS coverage

Which of the 24 controls in **OWASP MASVS v2.1.0** a machine can decide on its own, and which
still need a person. This is the coverage map behind the assessments at
[vybebat.dev](https://vybebat.dev). It is public so you can check the claim before you buy,
from us or from anyone else.

## Read this first

MASVS v2.0.0 **removed** the old L1 and L2 verification levels. They now live in the MASTG as
MAS testing profiles: MAS-L1, MAS-L2, MAS-R, and MAS-P since v2.1.0. Anyone selling a "MASVS
Level 2 certified" audit is quoting a scheme that was retired in January 2024.

## The count

<!-- BEGIN COUNT -->
| Automation | Controls | Meaning |
|---|---|---|
| Automated | 2 | A tool can return PASS or FAIL for the whole control from the app package, with no human judgement. |
| Partial | 18 | Tools produce the evidence: candidates, captures, inventories. A person decides the verdict. |
| Manual | 4 | Tooling gives little useful evidence. The verdict comes from functional testing, document review or judgement. |
<!-- END COUNT -->

**2 of 24.** A tool can close two controls on its own: the minimum platform version and known
vulnerable dependencies. Everything else needs a person to look at what the tool found, or to
test by hand. Any product that claims full MASVS coverage without an analyst is counting
controls it did not decide.

Tools still do most of the work on 18 controls. "Partial" does not mean "barely automated". It
means the tool finds the evidence and a person decides what it means.

## How a control is rated

The bar for **Automated** is strict on purpose: a tool must be able to say PASS or FAIL for the
whole control, not just for the part it can see. A tool that finds every use of MD5 has not
decided MASVS-CRYPTO-1, because MD5 for a cache key is fine and MD5 for a password is not.

Each rating is ours, and the reason is written next to it. To keep it honest we compare it with
OWASP's own test catalogue. For every control, the tables show how many active
[MASTG](https://mas.owasp.org/MASTG/) v2.0.0 tests exist and how many of them include a manual
step. How that is counted is in [scripts/mastg_counts.py](scripts/mastg_counts.py).

## By group

<!-- BEGIN GROUPS -->
| Group | Controls | Automated | Partial | Manual | Active MASTG tests |
|---|---|---|---|---|---|
| MASVS-STORAGE - Storage | 2 | 0 | 2 | 0 | 68 |
| MASVS-CRYPTO - Cryptography | 2 | 0 | 2 | 0 | 38 |
| MASVS-AUTH - Authentication and Authorization | 3 | 0 | 1 | 2 | 17 |
| MASVS-NETWORK - Network Communication | 2 | 0 | 2 | 0 | 26 |
| MASVS-PLATFORM - Platform Interaction | 3 | 0 | 3 | 0 | 53 |
| MASVS-CODE - Code Quality | 4 | 2 | 1 | 1 | 43 |
| MASVS-RESILIENCE - Resilience Against Reverse Engineering and Tampering | 4 | 0 | 4 | 0 | 26 |
| MASVS-PRIVACY - Privacy | 4 | 0 | 3 | 1 | 9 |
<!-- END GROUPS -->

## The controls

<!-- BEGIN CONTROLS -->
| Control | Statement | Automation | How it is verified | Why not fully automated | Active MASTG tests | Profiles |
|---|---|---|---|---|---|---|
| `MASVS-STORAGE-1` | The app securely stores sensitive data. | Partial | Manifest and plist review, keystore and keychain usage, then a dump of the app sandbox on a device we own. | Whether stored data is sensitive depends on what the app does with it. | 15 (3 static, 5 dynamic, 7 manual) | MAS-L1, MAS-L2 |
| `MASVS-STORAGE-2` | The app prevents leakage of sensitive data. | Partial | Backup flags statically, then log, cache and snapshot capture during a scripted walkthrough. | Logs and backups have to be exercised on a device, and a leak only counts if the data is sensitive. | 65 (21 static, 13 dynamic, 31 manual) | MAS-L1, MAS-L2, MAS-P |
| `MASVS-CRYPTO-1` | The app employs current strong cryptography and uses it according to industry best practices. | Partial | Static rules for broken ciphers, ECB mode, weak hashes, predictable randomness and static IVs, then review of each hit in context. | MD5 for a cache key is fine and for a password it is not. The call site decides. | 13 (2 static, 1 dynamic, 10 manual) | MAS-L1, MAS-L2 |
| `MASVS-CRYPTO-2` | The app performs key management according to industry best practices. | Partial | Hardcoded key and secret scanning, then review of how keys are generated, stored and rotated. | Finding a hardcoded key is automatic. Judging the key lifecycle is not. | 33 (14 static, 10 dynamic, 9 manual) | MAS-L1, MAS-L2 |
| `MASVS-AUTH-1` | The app uses secure authentication and authorization protocols and follows the relevant best practices. | Manual | Review of the token flow against endpoints you have authorised in writing. | Authentication is enforced on the server. The app package shows the client half at best. | 6 (6 manual) | MAS-L1, MAS-L2 |
| `MASVS-AUTH-2` | The app performs local authentication securely according to the platform best practices. | Partial | Static check of the biometric API and whether it is bound to a keystore key, then a bypass attempt on a device. | The API calls are visible. Whether they actually gate access needs a device. | 11 (8 static, 3 dynamic) | MAS-L2 |
| `MASVS-AUTH-3` | The app secures sensitive operations with additional authentication. | Manual | Walk through the high-value actions and check each one asks for step-up authentication. | Which operations are sensitive is a business question. | none | - |
| `MASVS-NETWORK-1` | The app secures all network traffic according to the current best practices. | Partial | Cleartext flags, network security config, iOS ATS exceptions and custom trust code statically, then observed TLS on a device. | Platform config is decidable. Custom certificate validation in app code often is not, and in a compiled Flutter snapshot it cannot be told apart from an ordinary TLS socket. | 22 (9 static, 3 dynamic, 10 manual) | MAS-L1, MAS-L2 |
| `MASVS-NETWORK-2` | The app performs identity pinning for all remote endpoints under the developer's control. | Partial | Static detection of the pinning implementation, then a bypass attempt to test it. | Pinning code can be found statically. Whether it holds needs an attempt to break it. | 4 (3 static, 1 dynamic) | MAS-L2 |
| `MASVS-PLATFORM-1` | The app uses IPC mechanisms securely. | Partial | Exported components, permission guards, PendingIntent mutability and URI grants statically, then crafted intents on a device. | An exported component is only a problem if what it exposes is sensitive. | 16 (4 static, 12 manual) | MAS-L1, MAS-L2 |
| `MASVS-PLATFORM-2` | The app uses WebViews securely. | Partial | JavaScript bridges and channels, file access settings and legacy web views statically, then a check of what content each WebView loads. | A JavaScript bridge is only dangerous if the WebView loads content an attacker can influence. | 21 (9 static, 12 manual) | MAS-L1, MAS-L2, MAS-P, MAS-R |
| `MASVS-PLATFORM-3` | The app uses the user interface securely. | Partial | Secure flag and input types statically, then screenshot, clipboard and notification leakage on a device. | Which screens show sensitive data is a judgement, and leakage has to be observed. | 16 (7 static, 4 dynamic, 5 manual) | MAS-L2 |
| `MASVS-CODE-1` | The app requires an up-to-date platform version. | Automated | Minimum and target SDK, iOS deployment target. | (Declared values with a clear threshold.) | 1 (1 static) | MAS-L2 |
| `MASVS-CODE-2` | The app has a mechanism for enforcing app updates. | Manual | Check that a forced upgrade or remote version gate exists and works. | A forced update is a server-side policy that has to be seen working. | 4 (4 manual) | MAS-L2 |
| `MASVS-CODE-3` | The app only uses software components without known vulnerabilities. | Automated | Dependency and SBOM scan against known vulnerability databases. | (Automated for the control as written. Whether a vulnerable function is reachable is a further, manual question.) | 9 (9 static) | MAS-L1, MAS-L2 |
| `MASVS-CODE-4` | The app validates and sanitizes all untrusted inputs. | Partial | Static detection of injection sinks, then confirmation that each sink is reachable with outside input. | A sink is only a finding if untrusted input reaches it. | 34 (16 static, 18 manual) | MAS-L1, MAS-L2, MAS-P, MAS-R |
| `MASVS-RESILIENCE-1` | The app validates the integrity of the platform. | Partial | Detect the root, jailbreak and attestation checks, then test on a rooted device whether they are real or decorative. | Finding the check is automatic. Whether it does anything needs a device. | 2 (2 dynamic) | MAS-R |
| `MASVS-RESILIENCE-2` | The app implements anti-tampering mechanisms. | Partial | Signature and checksum verification logic statically, then a repackaged build to see if it is caught. | Only a tampered build shows whether the check works. | 7 (3 static, 2 dynamic, 2 manual) | MAS-R |
| `MASVS-RESILIENCE-3` | The app implements anti-static analysis mechanisms. | Partial | Obfuscation state, decompiled readability, and whether a symbol or mapping file shipped in the package. | Obfuscation can be detected, but how much it slows an attacker is a judgement. | 10 (4 static, 3 dynamic, 3 manual) | MAS-R |
| `MASVS-RESILIENCE-4` | The app implements anti-dynamic analysis techniques. | Partial | Static detection of anti-debug and anti-instrumentation code, then attaching a debugger and Frida on a device we own. | Detecting the code is automatic. Whether it stops an attacker is a test, not a scan. | 9 (3 static, 2 dynamic, 4 manual) | MAS-R |
| `MASVS-PRIVACY-1` | The app minimizes access to sensitive data and resources. | Partial | Declared permissions against observed use, plus a third-party SDK and tracker inventory. | Whether a permission is needed depends on the feature it serves. | 9 (2 static, 3 dynamic, 4 manual) | MAS-P |
| `MASVS-PRIVACY-2` | The app prevents identification of the user. | Partial | Identifier use and device fingerprinting fields in captured traffic. | Tools can list identifiers. Whether they identify a person depends on how they are combined. | none | - |
| `MASVS-PRIVACY-3` | The app is transparent about data collection and usage. | Partial | Tracker inventory and captured traffic, compared with the privacy policy and the store data safety declaration. | Tools show what leaves the device. Comparing that to what the app declares is reading, not scanning. | 4 (1 static, 3 dynamic) | MAS-P |
| `MASVS-PRIVACY-4` | The app offers user control over their data. | Manual | Functional review of deletion, export and consent withdrawal. | These are features to use and observe, not code to scan. | none | - |
<!-- END CONTROLS -->

## What the MASTG data shows

- **Three controls have no active MASTG test yet:** MASVS-AUTH-3, MASVS-PRIVACY-2 and
  MASVS-PRIVACY-4. A vendor who reports a verdict on them is using their own method. Ask what
  it was.
- **Controls we once rated automated are mostly manual in MASTG.** 10 of 13 MASVS-CRYPTO-1
  tests and 12 of 16 MASVS-PLATFORM-1 tests include a manual step. That is part of why they are
  rated partial here.
- **The profiles follow the groups.** Every RESILIENCE test is MAS-R, every PRIVACY test is
  MAS-P. An assessment on the MAS-L1 profile does not cover either group, and should say so.
- Four active tests (MASTG-TEST-0240, 0241, 0324 and 0325) reference a weakness with no MASVS
  mapping in MASWE v1.0.0 and are not counted.

## Flutter apps

Flutter compiles Dart into a native snapshot that the free mobile scanners cannot read. On a
Flutter app they go silent on the Dart side of MASVS-CRYPTO-1, MASVS-CRYPTO-2, MASVS-NETWORK-1,
MASVS-PLATFORM-2, MASVS-CODE-4 and MASVS-RESILIENCE-3, usually without saying so. Our open
source tool [vybebat/flutterscope](https://github.com/vybebat/flutterscope) covers part of that
gap and reports the rest as not tested.

## Questions worth asking any vendor

Whoever you buy a mobile assessment from, including us:

1. Which of these 24 controls did you test, and which did you skip? A report with 24 passes
   and no gaps is a report that did not look.
2. For every control you marked as passing, what evidence can you show me?
3. Which MAS testing profile did you test against? MAS-L1 alone leaves out resilience and
   privacy.
4. Is this an assessment or a penetration test? Those are different products at different
   prices.
5. When your tooling fails to parse something, does the report say NOT_TESTED, or does it
   quietly show a pass? Silence must never look like a pass.

## Data

| File | What it holds |
|---|---|
| [`coverage.yaml`](coverage.yaml) | Our rating, method and reason for each control. The source of truth. |
| [`mastg-tests.json`](mastg-tests.json) | Active MASTG v2.0.0 tests per control, with ids. Generated. |
| [`scripts/build.py`](scripts/build.py) | Checks the data and renders the tables above from it. |
| [`scripts/mastg_counts.py`](scripts/mastg_counts.py) | Regenerates `mastg-tests.json` from the MASTG and MASWE sources. |

CI fails if the tables and the data disagree, or if a control statement differs from OWASP's
text.

## Changes

See [CHANGELOG.md](CHANGELOG.md). Ratings changed on 2026-09-25, and every change is listed
with its reason.

## Source and licence

Control ids and statements are taken verbatim from
[OWASP/masvs](https://github.com/OWASP/masvs) v2.1.0. Test data is derived from
[OWASP/mastg](https://github.com/OWASP/mastg) v2.0.0 and
[OWASP/maswe](https://github.com/OWASP/maswe) v1.0.0. All are licensed CC BY-SA 4.0 by the
OWASP Foundation. The ratings, methods and reasons are our own and open to argument. Open an
issue if you disagree with a row.

This repository is published under the same licence, [CC BY-SA 4.0](LICENSE).
