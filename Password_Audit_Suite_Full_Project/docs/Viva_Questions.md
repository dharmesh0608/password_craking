# Viva questions and short answers

1. **What is a password hash?** A one-way transformation used for verification; production systems add per-password salts and use adaptive algorithms.
2. **Why is SHA-256 unsuitable alone for password storage?** It is fast and permits many offline guesses after a database leak.
3. **What is a salt?** A unique random value stored alongside each password hash to defeat shared precomputed tables.
4. **Can 32 hex characters prove a digest is NTLM?** No. Format alone is ambiguous with MD5 and other 128-bit values.
5. **What does entropy estimate assume?** Independent, uniform random choices from an alphabet; people rarely choose passwords that way.
6. **What limits online guessing?** Rate limits, MFA, monitoring, and account controls.
7. **Why are sample reports redacted?** Plaintext in reports creates another credential exposure route.
8. **What are project limitations?** Synthetic inputs, capped attempts, heuristic ratings, and illustrative time scenarios.
