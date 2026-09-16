# MASVS coverage

Which of the 24 controls in **OWASP MASVS v2.1.0** a machine can decide on its own, and
which ones still need a human. This is the coverage map behind the assessments at
[vybebat.dev](https://vybebat.dev). It is published so you can check the claim before you buy.

## Read this first

MASVS v2.0.0 **removed** the old L1 and L2 verification levels. They now live in the MASTG as
MAS testing profiles: MAS-L1, MAS-L2, MAS-R, and MAS-P since v2.1.0. Anyone still selling a
"MASVS Level 2 certified" audit is quoting a standard that was retired in January 2024.

## The count

| Automation | Controls | Meaning |
|---|---|---|
| Automated | 6 | Decidable from the app package alone. |
| Partial | 12 | A tool produces candidate evidence. A human confirms or rejects it. |
| Manual | 6 | Analyst judgement, device testing, or document review. |

6 of 24. That is the honest ceiling for a fully automated mobile scan today. Any product
that claims full MASVS coverage without an analyst is counting controls it did not test.

## By group

| Group | Controls | Automated | Partial | Manual |
|---|---|---|---|---|
| MASVS-STORAGE - Storage | 2 | 0 | 2 | 0 |
| MASVS-CRYPTO - Cryptography | 2 | 1 | 1 | 0 |
| MASVS-AUTH - Authentication and Authorization | 3 | 0 | 1 | 2 |
| MASVS-NETWORK - Network Communication | 2 | 1 | 1 | 0 |
| MASVS-PLATFORM - Platform Interaction | 3 | 2 | 1 | 0 |
| MASVS-CODE - Code Quality | 4 | 2 | 1 | 1 |
| MASVS-RESILIENCE - Resilience Against Reverse Engineering and Tampering | 4 | 0 | 3 | 1 |
| MASVS-PRIVACY - Privacy | 4 | 0 | 2 | 2 |

The two groups that most often decide whether an assessment was real, RESILIENCE and PRIVACY,
are also the two with no fully automated control between them.

## The controls

| Control | Statement | Automation | How it is verified |
|---|---|---|---|
| `MASVS-STORAGE-1` | The app securely stores sensitive data. | Partial | Manifest and plist review, keystore and keychain usage, app sandbox dump on a device we own |
| `MASVS-STORAGE-2` | The app prevents leakage of sensitive data. | Partial | Log capture during a scripted walkthrough, backup flags, cache and snapshot review |
| `MASVS-CRYPTO-1` | The app employs current strong cryptography and uses it according to industry best practices. | Automated | Static rules for ECB mode, MD5 and SHA-1 used for security, predictable randomness, static IVs |
| `MASVS-CRYPTO-2` | The app performs key management according to industry best practices. | Partial | Hardcoded key and secret scanning, then manual review of the key lifecycle |
| `MASVS-AUTH-1` | The app uses secure authentication and authorization protocols and follows the relevant best practices. | Manual | Manual review of the token flow against endpoints you have authorised in writing |
| `MASVS-AUTH-2` | The app performs local authentication securely according to the platform best practices. | Partial | Static check of the biometric API and its crypto binding, then manual confirmation |
| `MASVS-AUTH-3` | The app secures sensitive operations with additional authentication. | Manual | Manual: does a high value action trigger step-up authentication |
| `MASVS-NETWORK-1` | The app secures all network traffic according to the current best practices. | Automated | Cleartext flags, network security config, iOS ATS exceptions, observed TLS version |
| `MASVS-NETWORK-2` | The app performs identity pinning for all remote endpoints under the developer's control. | Partial | Static detection of the pinning implementation, dynamic bypass attempt to test quality |
| `MASVS-PLATFORM-1` | The app uses IPC mechanisms securely. | Automated | Exported components, permission guards, PendingIntent mutability, URI permission grants |
| `MASVS-PLATFORM-2` | The app uses WebViews securely. | Automated | WebView JavaScript bridges, file access settings, legacy web view classes |
| `MASVS-PLATFORM-3` | The app uses the user interface securely. | Partial | Secure flag and input types statically, screenshot, clipboard and notification leakage on device |
| `MASVS-CODE-1` | The app requires an up-to-date platform version. | Automated | Minimum and target SDK, iOS deployment target |
| `MASVS-CODE-2` | The app has a mechanism for enforcing app updates. | Manual | Manual: is there a working forced upgrade or remote version gate |
| `MASVS-CODE-3` | The app only uses software components without known vulnerabilities. | Automated | Dependency and SBOM scan against known vulnerability databases |
| `MASVS-CODE-4` | The app validates and sanitizes all untrusted inputs. | Partial | Static injection sink detection, then manual confirmation that the sink is reachable |
| `MASVS-RESILIENCE-1` | The app validates the integrity of the platform. | Partial | Detect the integrity and attestation mechanism, then assess whether it is real or decorative |
| `MASVS-RESILIENCE-2` | The app implements anti-tampering mechanisms. | Partial | Signature and checksum verification logic, manual assessment of strength |
| `MASVS-RESILIENCE-3` | The app implements anti-static analysis mechanisms. | Partial | Decompile readability, obfuscation state, and whether a mapping file shipped in the artifact |
| `MASVS-RESILIENCE-4` | The app implements anti-dynamic analysis techniques. | Manual | Manual anti-debug and anti-instrumentation testing on a device we own |
| `MASVS-PRIVACY-1` | The app minimizes access to sensitive data and resources. | Partial | Declared permissions against observed usage, third-party SDK and tracker inventory |
| `MASVS-PRIVACY-2` | The app prevents identification of the user. | Partial | Identifier usage and device fingerprinting fields in traffic |
| `MASVS-PRIVACY-3` | The app is transparent about data collection and usage. | Manual | Privacy policy and store data safety declaration against observed traffic. The gap is the finding. |
| `MASVS-PRIVACY-4` | The app offers user control over their data. | Manual | Functional review of deletion, export and consent withdrawal |

## Questions worth asking any vendor

Whoever you buy a mobile assessment from, including us:

1. Which of these 24 controls did you test, and which did you skip? A report with 24 passes
   and no gaps is a report that did not look.
2. For every control you marked as passing, what evidence can you show me?
3. Is this an assessment or a penetration test? Those are different products at different prices.
4. When your tooling fails to parse something, does the report say NOT_TESTED, or does it
   quietly show a pass? Silence must never look like a pass.

## Data

[`coverage.yaml`](coverage.yaml) holds the same table in machine-readable form, if you want to
diff it against your own coverage or feed it to a tool.

## Source and licence

Control IDs and statements are taken verbatim from
[OWASP/owasp-masvs](https://github.com/OWASP/owasp-masvs) v2.1.0, licensed CC BY-SA 4.0 by the
OWASP Foundation. The automation column and the verification notes are our own assessment and
are open to argument. Open an issue if you disagree with a row.

This repository is published under the same licence, [CC BY-SA 4.0](LICENSE).
