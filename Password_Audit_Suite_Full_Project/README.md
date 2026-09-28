# Password Audit Suite

A self-contained Python 3.10+ teaching lab for password policy assessment. It uses disposable examples and requires no packages for the CLI.

## Quick start

```bash
python main.py dictionary demo
python main.py analyze
python main.py inspect '$6$salt$example'
python main.py simulate demo123 demo
python main.py estimate 8 62 1000
python main.py report samples/lab_passwords.csv
python -m unittest discover -s tests -v
```

Run commands from the project directory. `analyze` prompts without echo when the argument is omitted. Command arguments can appear in shell history, so use only disposable lab inputs. The generated report contains labels and ratings, not plaintext samples. Remove sample CSVs after a class demo if you substitute your own data.

## Included modules

| Module | What it demonstrates | Boundary |
|---|---|---|
| Dictionary | Small word mutations | 5,000 result ceiling |
| Hash inspector | Recognition of sample crypt strings and ambiguous 32-hex digests | No OS credential access |
| Simulator | Bounded SHA-256 comparison against a lab value | 100,000 attempt ceiling, no authentication requests |
| Analyzer | Length, variety, common patterns, naive entropy | Heuristic, not a breach lookup |
| Report | CSV sample audit and recommendations | Never includes password plaintext |

The simulator's SHA-256 comparison is educational. Production password storage needs a salted, adaptive password hashing scheme. Time estimates assume uniformly random passwords and a chosen constant guess rate; they are illustrations, not predictions for a particular system.

See `docs/Project_Report.md`, `docs/Architecture.md`, `docs/Viva_Questions.md`, `screenshots/`, and `Presentation.pptx`.
