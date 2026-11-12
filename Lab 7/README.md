# L6_L7_07 — Hospital Triage Priority

## Lab 7: Fuzz Testing for Input Validation Bugs with Hypothesis

**Student Name:** SAMHITHA KANTH  
**SRN:** PES1UG24AM245  
**Course:** Software Engineering (UE22CS351AA)  
**Institution:** PES University  

---

## 1. Overview

This laboratory exercise explores **property-based fuzz testing** using the Python **Hypothesis** library to detect, analyze, and resolve input validation vulnerabilities in hospital data processing routines (`processor.py`).

Traditional unit testing checks anticipated input vectors, often missing obscure edge cases. Hypothesis automates edge-case generation by producing randomized, diverse, and malformed inputs, systematically minimizing (shrinking) failing inputs down to minimal reproduction cases.

---

## 2. Functions Under Test

| Function | Expected Input Format | Intended Behavior |
|---|---|---|
| `parse_vitals_summary(vitals_csv)` | `"HR,SpO2,Temp"` (e.g. `"80,98,37.0"`) | Parses vitals, computes acuity flag (`CRITICAL` vs `STABLE`), and returns a formatted summary. |
| `compute_patient_bmi(bmi_string)` | `"weight/height"` (e.g. `"70/1.75"`) | Computes body mass index $BMI = \frac{\text{weight}}{\text{height}^2}$, rounded to 2 decimal places. |
| `assign_ward_bed(allocation_code)` | `"WARD-BED_NUM"` (e.g. `"ICU-05"`) | Maps department code to ward name and assigns bed number. |

---

## 3. Vulnerabilities Discovered via Fuzz Testing

Property-based testing with `@given(st.text() | st.none())` revealed that all three starter functions lacked defensive programming:

1. **`parse_vitals_summary`**:
   - `s = None`: Raised unhandled `AttributeError: 'NoneType' object has no attribute 'split'`.
   - `s = ''` or non-numeric: Raised `ValueError: could not convert string to float: ''`.
   - `s = '0'`: Raised `IndexError: list index out of range` (expected 3 parts).
   - Missing boundary checks for physiological ranges or non-finite numbers (`NaN`, `Inf`).

2. **`compute_patient_bmi`**:
   - `s = None`: Raised `AttributeError`.
   - `s = ''` or missing `/`: Raised `ValueError: not enough values to unpack`.
   - `height <= 0`: Raised fatal `ZeroDivisionError: float division by zero`.
   - Missing checks for non-numeric, negative, infinite, or `NaN` values.

3. **`assign_ward_bed`**:
   - `s = None`: Raised `AttributeError: 'NoneType' object has no attribute 'strip'`.
   - `s = ''`: Raised `ValueError: not enough values to unpack`.
   - `s = '-'`: Raised `ValueError: invalid literal for int() with base 10: ''`.
   - Invalid ward codes (e.g. `s = 'UNKNOWN-01'`): Raised `KeyError`.

---

## 4. Defensive Hardening Applied

The updated `processor.py` was hardened with defensive programming:
- **Type Guards:** Verifies that inputs are instances of `str` before invoking string operations (`.split()`, `.strip()`).
- **Delimiter & Token Validation:** Checks exact expected parts count before unpacking.
- **Robust Exception Handling:** Wraps numerical casts inside `try...except (ValueError, TypeError)` blocks.
- **Domain & Boundary Checks:** Validates physiological ranges, guards against zero or negative divisors (`height <= 0`), and excludes non-finite floats (`math.isnan`, `math.isinf`).
- **Safe Dictionary Access:** Validates ward keys before dictionary lookup and ensures bed numbers are positive integers.
- **Graceful Error Returns:** Returns descriptive error messages or `None` rather than crashing.

---

## 5. Test Execution & Verification

### Step 1: Install Dependencies
```bash
pip install hypothesis pytest
```

### Step 2: Run Application
```bash
python processor.py
```

### Step 4 & 6: Run Fuzz Tests
```bash
pytest test_processor.py -v
```
All 3 tests pass 100% of generated test cases across multiple randomized trials.

---

## 6. Deliverables

1. **PDF Document with Screenshots:**
   - `PES1UG24AM245_Lab7_Report.pdf` (and `Lab7_Report.pdf`)
   - Includes full lab report with Figure 1 (Step 2 output), Figure 2 (Step 4 failures), Figure 3 (Step 5 output), and Figure 4 (Step 6 passing tests).
2. **Fixed Application Python Script:**
   - `processor.py`
3. **Updated Test Script:**
   - `test_processor.py`
4. **Screenshot Assets:**
   - `Screenshot_Step2_Buggy_Processor_Output.png`
   - `Screenshot_Step4_Test_Processor_Failing.png`
   - `Screenshot_Step5_Fixed_Processor_Output.png`
   - `Screenshot_Step6_Test_Processor_Passing.png`
