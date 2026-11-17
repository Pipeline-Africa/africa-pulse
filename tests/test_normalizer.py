import pytest
from africa_pulse.transformation.normalizer import (
    parse_and_convert_timestamp,
    convert_units,
    normalize_observation
)




def test_timestamp_normalization_with_explicit_tz():
    # Local time in Africa/Lagos (UTC+1)
    raw_ts = "2026-10-15T13:00:00"
    utc_ts, orig_ts = parse_and_convert_timestamp(raw_ts, source_timezone_str="Africa/Lagos")
    
    assert utc_ts == "2026-10-15T12:00:00+00:00"
    assert orig_ts == raw_ts

def test_timestamp_naive_rejection():
    raw_ts = "2026-10-15T13:00:00"
    with pytest.raises(ValueError, match="provided without an explicit source timezone"):
        parse_and_convert_timestamp(raw_ts, source_timezone_str=None)

def test_unit_conversion_fahrenheit_to_celsius():
    val_c = convert_units(77.0, current_unit="F", metric_type="temperature")
    assert pytest.approx(val_c, 0.01) == 25.0

def test_unit_conversion_unsupported_raises():
    with pytest.raises(ValueError, match="Unsupported unit conversion"):
        convert_units(100.0, current_unit="lightyears", metric_type="temperature")

def test_normalize_observation_complete():
    record = {
        "source_id": "open_meteo_lagos",
        "timestamp": "2026-10-15T14:00:00+01:00",
        "value": 86.0,
        "unit": "F"
    }

    normalized = normalize_observation(record, metric_type="temperature")

    assert normalized["timestamp"] == "2026-10-15T13:00:00+00:00"
    assert normalized["original_timestamp"] == "2026-10-15T14:00:00+01:00"
    assert pytest.approx(normalized["value"], 0.01) == 30.0
    assert normalized["unit"] == "C"
    assert normalized["original_unit"] == "F"
    assert normalized["normalization_applied"] is True