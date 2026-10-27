# Lab 5 – Reflection

**1. Which issues were the easiest and which were the hardest to fix?**

The easiest were the mechanical ones: Flake8's blank-line and line-length
warnings, the missing docstrings, the `assignDriver` rename and switching to
an f-string. Each one has an obvious, local fix that does not change behaviour.
The hardest was the bare `except: pass` that Bandit flagged. Deleting it is
easy, but doing so exposed why it was there: bad data (`-6`, `"full"`) was
getting into the system and the exception handler was hiding the damage. The
real fix was to validate input at the point of entry and make `average_load`
fail with clear messages. The unused `route_id` and the odd
write-then-reload in `sync_fleet_data` also needed thought about what the code
was meant to do.

**2. Did the tools report any false positives?**

Bandit's B311 on `random.choice` is a false positive in practice: picking a
shuttle driver is not a security decision, so a non-cryptographic generator is
fine. I switched to `secrets.choice` anyway because it costs nothing and gives a
clean report, but a `# nosec B311` with a justification would also have been
reasonable. Pylint's missing-docstring and naming messages are not bugs, but
they are valid maintainability findings. No other result was wrong.

**3. How would you integrate static analysis into a real workflow?**

Run Flake8 and Pylint locally through a pre-commit hook so style and quality
problems are caught before a commit exists. Run all three tools in CI (for
example GitHub Actions) on every pull request and fail the build on Bandit
findings, Flake8 errors or a Pylint score below an agreed threshold. Keep the
tool configuration (`.pylintrc`, `setup.cfg`, Bandit config) in the repo so
the whole team uses the same rules, and document any suppressions with a
reason.

**4. What tangible improvements did you see after the fixes?**

The numbers: Pylint went from 6.25 to 10.00, Bandit from 2 findings to 0 and
Flake8 from 10 violations to 0. More importantly, the behaviour improved. The
original program crashed with a `KeyError` at the end, accepted negative and
text passenger counts, and flagged R2 as under-used partly because of a
`-6` entry. The cleaned version rejects bad data with clear messages, no
longer shares one log list between calls, closes its files properly, can be
imported without running, and finishes without a traceback. The tools did not
flag the validation and crash problems directly, so running the program and
reading its output was just as important as the static analysis.
