import json
import pytest
from pathlib import Path
from africa_pulse.storage.raw_archiver import save_raw_response, load_and_reprocess






def test_save_raw_response(tmp_path):
    source = "open_meteo"
    params = {"latitude": 6.5244, "longitude": 3.3792, "hourly": "temperature_2m"}
    payload = {"elevation": 15.0, "hourly": {"time": ["2026-10-15T00:00"], "temperature_2m": [27.5]}}
    run_id = "run_test_abc"

    saved_path = save_raw_response(source, payload, params, run_id, base_raw_dir=str(tmp_path / "raw"))

    assert saved_path.exists()
    
    with open(saved_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["source"] == source
    assert data["run_id"] == run_id
    assert data["request_params"] == params
    assert data["raw_response"] == payload
    assert "collected_at" in data

def test_load_and_reprocess(tmp_path):
    source = "openaq"
    params = {"city": "Lagos"}
    payload = {"results": [{"parameter": "pm25", "value": 35.2}]}
    run_id = "run_test_reprocess"

    saved_path = save_raw_response(source, payload, params, run_id, base_raw_dir=str(tmp_path / "raw"))

    def mock_parser(raw):
        return [item["value"] for item in raw["results"]]

    reprocessed_results = load_and_reprocess(str(saved_path), mock_parser)

    assert reprocessed_results == [35.2]