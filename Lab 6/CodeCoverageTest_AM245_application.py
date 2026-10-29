
import pytest
from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds,
)


def test_invalid_wards():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)


def test_negative_default_acuity():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_non_accepting_ward_is_skipped():
    result = process_triage_wards(
        [{"is_accepting": False, "patients": [{"unconscious": True}]}], 10
    )
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_default_patient_values():
    result = process_triage_wards([{"is_accepting": True, "patients": [{}]}], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_empty_accepting_ward():
    result = process_triage_wards([{"is_accepting": True}], 10)
    assert result["acuity_score"] == 10 if False else result["acuity_score"] == 0


def test_low_oxygen_patient():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [{"spo2": 85}]}], 10
    )
    assert result["acuity_score"] == 60


def test_high_heart_rate_patient():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [{"hr": 130}]}], 10
    )
    assert result["acuity_score"] == 60


def test_unconscious_general_patient():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [{"unconscious": True}]}], 10
    )
    assert result["acuity_score"] == 100


def test_unconscious_outpatient_resets_score():
    result = process_triage_wards(
        [{"is_accepting": True, "tier": "outpatient",
          "patients": [{"unconscious": True}, {"spo2": 80}]}], 10
    )
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_invalid_patient_readings():
    result = process_triage_wards(
        [{"is_accepting": True, "patients": [
            {"spo2": 0}, {"hr": 0}
        ]}], 10
    )
    assert result["acuity_score"] == 0


def test_five_flagged_entries_trigger_alert():
    patients = [{"spo2": 0} for _ in range(5)]
    result = process_triage_wards(
        [{"is_accepting": True, "patients": patients}], 10
    )
    assert result == {"acuity_score": 0, "status": "WARD_ALERT"}


def test_icu_standby_adds_acuity():
    result = process_triage_wards(
        [{"is_accepting": True, "icu_standby": True, "patients": [{}]}], 10
    )
    assert result["acuity_score"] == 35


def test_zero_acuity_returns_no_urgent_cases():
    result = process_triage_wards([{"is_accepting": True, "patients": [{}]}], 0)
    assert result["status"] == "NO_URGENT_CASES"


def test_empty_sensor_streams():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"
    assert monitor_oxygen_manifolds(None) == "NO_DATA"


def test_normal_oxygen_pressure():
    assert monitor_oxygen_manifolds([[5.0, 4.5, 4.0]]) == "PRESSURE_NORMAL"


def test_two_consecutive_low_pressure_readings():
    assert monitor_oxygen_manifolds([[3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_pressure_recovery_resets_streak():
    assert monitor_oxygen_manifolds([[3.0, 4.0, 3.0, 3.0]]) == "PRESSURE_FAILURE"


def test_empty_manifold():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"
