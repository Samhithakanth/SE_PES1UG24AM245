"""
Lab 7: Hardened processor module with defensive programming against fuzzing bugs.
"""
import math

def parse_vitals_summary(vitals_csv):
    """
    Parse comma-separated vitals (HR, SpO2, Temp) and determine patient stability.
    Returns a summary string or an error message if the input is malformed.
    """
    if not isinstance(vitals_csv, str):
        return "Invalid input: vitals data must be a string"
    parts = [p.strip() for p in vitals_csv.split(',')]
    if len(parts) != 3:
        return "Invalid format: expected 3 comma-separated values (HR,SpO2,Temp)"
    try:
        hr = float(parts[0])
        spo2 = float(parts[1])
        temp = float(parts[2])
    except (ValueError, TypeError):
        return "Invalid vitals values: HR, SpO2, and Temp must be valid numbers"
    
    if any(math.isnan(x) or math.isinf(x) for x in (hr, spo2, temp)):
        return "Invalid vitals values: numbers must be finite"

    if hr <= 0 or hr > 300 or spo2 < 0 or spo2 > 100 or temp < 20 or temp > 50:
        return "Invalid vitals values: out of physiological range"

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"

def compute_patient_bmi(bmi_string):
    """
    Compute patient BMI from 'weight/height' string.
    Returns the rounded BMI float (2 decimal places) or None if invalid.
    """
    if not isinstance(bmi_string, str):
        return None
    parts = bmi_string.split('/')
    if len(parts) != 2:
        return None
    try:
        weight = float(parts[0].strip())
        height = float(parts[1].strip())
    except (ValueError, TypeError):
        return None
    
    if any(math.isnan(x) or math.isinf(x) for x in (weight, height)):
        return None

    if weight <= 0 or height <= 0:
        return None

    try:
        bmi = weight / (height ** 2)
        if math.isnan(bmi) or math.isinf(bmi):
            return None
        return round(bmi, 2)
    except (ZeroDivisionError, OverflowError):
        return None

def assign_ward_bed(allocation_code):
    """
    Assign ward bed from allocation code formatted as 'WARD-BED_NUM'.
    Returns the descriptive ward and bed assignment string or an error message.
    """
    if not isinstance(allocation_code, str):
        return "Invalid allocation code: must be a string"
    parts = allocation_code.strip().split('-')
    if len(parts) != 2:
        return "Invalid allocation format: expected 'WARD-BED'"
    ward = parts[0].strip().upper()
    bed_str = parts[1].strip()
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }
    if ward not in ward_names:
        return f"Unknown ward code: '{ward}'"
    try:
        bed_num = int(bed_str)
        if bed_num <= 0:
            return "Invalid bed number: must be positive"
    except (ValueError, TypeError):
        return "Invalid bed number: must be an integer"
    return f"{ward_names[ward]} Bed #{bed_num}"

def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))

if __name__ == "__main__":
    main()
