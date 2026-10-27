# Lab 5 – Issues Found and Fixed

**File:** `shuttle_system.py` (Campus Shuttle Timetable & Fleet Tracker)
**Line numbers refer to the original starter file.**

## Score summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.25 / 10 (18 messages) | **10.00 / 10** |
| Bandit | 2 issues (both Low severity) | **No issues identified** |
| Flake8 | 10 violations | **0 violations** |

## Issue table

Ordered by severity (security and bugs first, style last). Rows marked
"manual" were found by running the program, not by a tool.

| # | Issue | Type | Line(s) | Description | Fix Approach | Commit |
|---|-------|------|---------|-------------|--------------|--------|
| 1 | Silent `try/except/pass` (Bandit B110, Pylint W0702, Flake8 E722) | Security / Bug | 26-30 | A bare `except:` followed by `pass` swallowed every error in `underused_routes`. It hid the `TypeError` caused by the string `"full"` and the divide-by-zero on routes with no trips. | Removed the try/except. Added an explicit `if route["trips"]` check, and `average_load` now raises a clear `ValueError` for unknown routes or routes with no trips. | 1 (Bandit) |
| 2 | No input validation (manual) | Bug | 11-14, 49-50 | `add_trip_log` accepted `-6` and `"full"` as passenger counts, so R2's average was `-1` (wrongly flagged as under-used because of bad data) and R3 held a string. | Reject non-integers, booleans, negative counts and unknown routes with `ValueError`. `main()` catches and reports rejected trips. | 1 (Bandit) |
| 3 | Crash on removed route (manual) | Bug | 55-58 | After `remove_route("R3")`, `average_load("R3")` raised an unhandled `KeyError`. Looking up an unknown route in the prompt also crashed. | `average_load` validates the route. `main()` handles unknown routes and prints a friendly message instead of a traceback. | 1 (Bandit) |
| 4 | `random` for driver selection (Bandit B311) | Security (Low) | 35 | `random.choice` is not a cryptographically secure generator, so Bandit flags it. | Replaced with `secrets.choice`. | 1 (Bandit) |
| 5 | Lines out of PEP 8 layout (Flake8 E302 x7, E305) | Style | 11, 16, 19, 23, 33, 37, 45, 60 | One blank line between top-level functions, and one before the module-level `main()` call. | Two blank lines around top-level definitions. | 2 (Flake8) |
| 6 | Line too long (Flake8 E501) | Style | 13 | Log line was 82 characters, limit is 79. | Wrapped the expression across two lines (later rewritten as a short f-string in commit 3). | 2 (Flake8) |
| 7 | Mutable default argument (Pylint W0102) | Bug | 11 | `logs=[]` is created once and shared across every call, so logs from separate calls piled up in one list. | Default changed to `None` and a fresh list is created inside the function. | 3 (Pylint) |
| 8 | Missing docstrings (Pylint C0114, C0116 x7) | Maintainability | 1, 11, 16, 19, 23, 33, 37, 45 | Module and all functions had no docstring. | Added a module docstring and a docstring for each function. | 3 (Pylint) |
| 9 | `assignDriver` naming (Pylint C0103) | Style | 33 | camelCase name violates snake_case convention. | Renamed to `assign_driver` and updated the caller. | 3 (Pylint) |
| 10 | Unused argument `route_id` (Pylint W0613) | Quality | 33 | The parameter was never used, so any value (even an invalid route) returned a driver. | Function now validates the route with `route_id`. Driver list moved to a `DRIVERS` constant. | 3 (Pylint) |
| 11 | `%` string formatting (Pylint C0209) | Style | 13 | Old-style formatting where an f-string is clearer. | Converted to an f-string. | 3 (Pylint) |
| 12 | File handling (Pylint R1732 x2, W1514 x2) | Resource / Quality | 39-43 | Files opened without `with` (second handle was never closed) and without an explicit encoding. | Use `with open(..., encoding="utf-8")` and `json.dump`. | 3 (Pylint) |
| 13 | `global routes` and pointless reload (Pylint W0603) | Design | 37-43 | `sync_fleet_data` wrote the file, read it straight back and replaced the global with an identical copy. | Dropped the global and the reload; the function now only writes the file. Behaviour is unchanged. | 3 (Pylint) |
| 14 | Script runs on import (manual) | Design | 60 | `main()` was called at module level, so importing the file ran the whole program. | Wrapped in `if __name__ == "__main__":`. | 3 (Pylint) |

## Verification

Reports are in `reports/before/` and `reports/after/`
(`pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`).
After the last commit: Pylint 10.00/10, Bandit "No issues identified",
Flake8 empty output, and the program runs end to end without a traceback.
