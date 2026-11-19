import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from africa_pulse.validation.router import DataIngestionRouter

@pytest.fixture
def router(tmp_path):
    return DataIngestionRouter(quarantine_dir=str(tmp_path / "quarantine"))

def test_mixed_batch_processing(router):
    batch = [
        {"timestamp": "2026-10-15T12:00:00Z", "source_id": "meteo_lagos", "value": 28.5},  # Valid
        {"timestamp": None, "source_id": "meteo_lagos", "value": 30.1},                     # Quarantined (missing timestamp)
        {"timestamp": "2026-10-15T12:00:00Z", "source_id": "openaq_nairobi", "value": -2.0} # Warning (negative value, retained)
    ]
    
    result = router.process_batch(batch, run_id="run_test_001")
    
    assert result["summary"]["total_processed"] == 3
    assert result["summary"]["accepted_count"] == 2
    assert result["summary"]["quarantined_count"] == 1
    assert result["summary"]["warning_count"] == 1
    assert len(result["quarantined_records"]) == 1
    assert result["quarantined_records"][0]["failure_reason"] == "Missing mandatory 'timestamp' field"

def test_fully_invalid_batch(router):
    batch = [
        {"timestamp": None, "source_id": "", "value": None},
        {"timestamp": "", "source_id": "meteo_cairo", "value": 9999}
    ]
    
    result = router.process_batch(batch, run_id="run_test_002")
    
    assert result["summary"]["total_processed"] == 2
    assert result["summary"]["accepted_count"] == 0
    assert result["summary"]["quarantined_count"] == 2
    assert len(result["accepted_records"]) == 0

def test_storage_failure_handling(router):
    batch = [
        {"timestamp": None, "source_id": "test", "value": 10}  # Triggers quarantine write
    ]
    
    # Mock open() to simulate a disk write failure / IOError
    with patch("builtins.open", side_effect=PermissionError("Disk write denied")):
        with pytest.raises(IOError, match="Quarantine storage write failed"):
            router.process_batch(batch, run_id="run_test_003")