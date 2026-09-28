# Password Audit Suite Project Report

## Title page

**Project:** Password Cracking and Credential Attack Suite: Controlled Password Audit Simulation  
**Student:** [Your name]  
**College:** [College name]  
**Course and semester:** [Fill in]  
**Guide:** [Fill in]  
**Academic year:** [Fill in]

## Certificate and acknowledgement

Insert the college-approved certificate with signatures. I thank my project guide and department for support during the lab demonstration. Replace this statement with your own acknowledgement before submission.

## Abstract

This project demonstrates weak password patterns, limited dictionary mutations, recognition of sample password hash formats, bounded local attempt simulation, and redacted audit reporting. Its purpose is to connect offensive password concepts to defensive controls without interacting with real accounts or operating system credential stores.

## Problem and objectives

Predictable passwords and reuse can make account compromise easier. The project aims to show how password choices affect an illustrative search space, flag common patterns, compare lab guesses, recognize hash formats, and recommend controls. Success is measured by runnable commands, deterministic sample findings, and a report that excludes plaintext.

## Requirements and tools

Python 3.10 or newer. Standard library modules: argparse, csv, getpass, hashlib, itertools, json, math, pathlib, re, unittest. The deck and figures are prebuilt, so users need no presentation package to run the toolkit. Commands work on Windows PowerShell, macOS, and Linux from the project directory.

## Design and modules

The flowchart is in `Architecture.md`. The CLI calls library functions for each operation. Dictionary variants include case changes, leet substitutions, numbers, and punctuation. Hash classification recognizes sample `$1$`, `$5$`, `$6$`, `$y$` prefixes and locked account markers. A 32-character hex digest is labeled ambiguous because its format alone is insufficient to identify MD5 or NT hashing. No live hash cracking or privileged extraction is performed.

The simulator uses SHA-256 only as a deterministic local comparison example, with a fixed cap. It does not represent secure password storage. The analyzer estimates a naive maximum entropy from observed character classes, then separately checks common phrases and predictable sequences. Human choice lowers real-world unpredictability, so its bit estimate is explicitly qualified.

## Sample execution and findings

Run `python main.py report samples/lab_passwords.csv` to generate `outputs/audit_report.json`. The four disposable samples contain two clearly weak examples and two longer examples. The sample report records labels, length, rating, and reasons. Try `python main.py simulate demo123 demo` to see a bounded candidate match. `python main.py estimate 8 62 1000` illustrates average guesses under a constant synthetic rate.

## Test plan

Run `python -m unittest discover -s tests -v`. Tests check variant limits, weak and stronger ratings, ambiguous hash identification, simulator stopping, estimate arithmetic, and plaintext omission from audit rows. Record the actual test output in the screenshots directory if submitting a live demonstration.

## Security interpretation

A password length and composition heuristic cannot establish that a password is safe. Recommended controls are unique passwords managed by a password manager, multifactor authentication, rate limits for online sign-in, monitoring, and salted adaptive hashes such as Argon2id for server storage. Online rate limiting changes the practical attack rate. Offline hash exposure depends strongly on the hash scheme and parameters.

## Scope and limitations

The toolkit does not copy `/etc/shadow`, export SAM or SYSTEM hives, authenticate to services, or operate on accounts. Students can describe Linux shadow and Windows SAM structures conceptually and use instructor-provided synthetic examples. The simulator intentionally excludes real hash cracking tools. Timing values are mathematical scenarios, not measured cracking benchmarks. The report input CSV contains lab plaintext and should never hold real user credentials.

## Conclusion and future work

The demonstration identifies weak patterns and shows why assumptions behind time estimates matter. Future defensive extensions could add approved organization policy profiles, breach screening through a privacy-preserving service, and a local GUI with secure input handling.

## References

NIST SP 800-63B, Digital Identity Guidelines, Authentication and Lifecycle Management. OWASP Password Storage Cheat Sheet and Authentication Cheat Sheet. Consult the current official editions when preparing the submitted bibliography.
