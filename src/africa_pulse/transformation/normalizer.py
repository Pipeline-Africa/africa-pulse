import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

logger = logging.getLogger(__name__)

# Canonical unit definitions agreed for Africa Pulse
CANONICAL_UNITS = {
    "temperature": "C",
    "pm25": "ug/m3",
    "wind_speed": "m/s"
}



def parse_and_convert_timestamp(timestamp_str: str, source_timezone_str: Optional[str] = None) -> Tuple[str, str]:
    """
    Converts an incoming observation timestamp to a UTC ISO string, 
    making timezone assumptions explicit and retaining original traceability.
    
    Returns:
        (utc_timestamp_iso, original_timestamp_str)
    """
    if not timestamp_str or not isinstance(timestamp_str, str):
        raise ValueError(f"Invalid or missing timestamp: {timestamp_str}")

    try:
        # Parse ISO format string
        dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    except ValueError as e:
        raise ValueError(f"Unparsable timestamp format: {timestamp_str}") from e

    # If the datetime is naive (no timezone info provided)
    if dt.tzinfo is None:
        if not source_timezone_str:
            raise ValueError(f"Naive timestamp '{timestamp_str}' provided without an explicit source timezone.")
        try:
            tz = ZoneInfo(source_timezone_str)
            dt = dt.replace(tzinfo=tz)
        except ZoneInfoNotFoundError as e:
            raise ValueError(f"Invalid source timezone specified: {source_timezone_str}") from e

    # Convert strictly to UTC
    dt_utc = dt.astimezone(timezone.utc)
    
    return dt_utc.isoformat(), timestamp_str

def convert_units(value: float, current_unit: str, metric_type: str) -> float:
    """
    Converts supported measurements to agreed canonical units.
    """
    if value is None:
        raise ValueError("Cannot convert unit for a null value.")

    target_unit = CANONICAL_UNITS.get(metric_type)
    if not target_unit:
        return value  # If metric type is unknown, return value as-is

    current_unit_clean = current_unit.strip().lower()
    target_unit_clean = target_unit.strip().lower()

    if current_unit_clean == target_unit_clean:
        return value

    # Example unit conversion logic
    if metric_type == "temperature":
        if current_unit_clean in ["fahrenheit", "f"]:
            return (value - 32) * 5.0 / 9.0
        elif current_unit_clean in ["kelvin", "k"]:
            return value - 273.15

    elif metric_type == "wind_speed":
        if current_unit_clean in ["km/h", "kmh"]:
            return value / 3.6
        elif current_unit_clean in ["mph"]:
            return value * 0.44704

    raise ValueError(f"Unsupported unit conversion from '{current_unit}' to '{target_unit}' for metric '{metric_type}'.")

def normalize_observation(
    record: Dict[str, Any], 
    metric_type: str, 
    source_timezone: Optional[str] = None
) -> Dict[str, Any]:
    """
    Applies shared normalization for timestamps and units to an incoming observation record.
    """
    raw_timestamp = record.get("timestamp")
    raw_value = record.get("value")
    raw_unit = record.get("unit")

    # 1. Normalize Timestamp to UTC
    utc_ts, orig_ts = parse_and_convert_timestamp(raw_timestamp, source_timezone)

    # 2. Normalize Measurement Units
    normalized_val = raw_value
    if raw_unit and metric_type in CANONICAL_UNITS:
        normalized_val = convert_units(float(raw_value), raw_unit, metric_type)

    # Construct normalized record retaining traceability
    normalized_record = {
        **record,
        "timestamp": utc_ts,
        "original_timestamp": orig_ts,
        "value": normalized_val,
        "original_value": raw_value,
        "unit": CANONICAL_UNITS.get(metric_type, raw_unit),
        "original_unit": raw_unit,
        "normalization_applied": True
    }

    return normalized_record