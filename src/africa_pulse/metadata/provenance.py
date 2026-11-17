import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional




logger = logging.getLogger(__name__)






def create_run_metadata(
    source_id: str,
    connector_name: str,
    connector_version: str,
    city_id: Optional[str] = None,
    request_params: Optional[Dict[str, Any]] = None,
    raw_artifact_ref: Optional[str] = None,
    base_metadata_dir: str = "data/metadata/runs"
) -> Dict[str, Any]:
    """
    Initializes a run metadata dictionary tracking data provenance from start.
    """
    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}"
    
    metadata = {
        "run_id": run_id,
        "source_id": source_id,
        "connector_name": connector_name,
        "connector_version": connector_version,
        "city_id": city_id,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": None,
        "outcome": "RUNNING",
        "request_params": request_params or {},
        "metrics": {
            "received": 0,
            "accepted": 0,
            "rejected": 0,
            "written": 0
        },
        "raw_artifact_ref": raw_artifact_ref,
        "error_summary": None,
        "_metadata_dir": base_metadata_dir
    }
    return metadata

def finalize_run_metadata(
    run_metadata: Dict[str, Any],
    outcome: str,
    metrics: Optional[Dict[str, int]] = None,
    error_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Updates run metadata with final outcomes, metrics, and error summaries,
    then persists it to disk as a JSON record.
    """
    run_metadata["end_time"] = datetime.now(timezone.utc).isoformat()
    run_metadata["outcome"] = outcome.upper()
    
    if metrics:
        run_metadata["metrics"].update(metrics)
        
    if error_message:
        run_metadata["error_summary"] = error_message

    # Persist metadata to storage
    metadata_dir = Path(run_metadata.pop("_metadata_dir", "data/metadata/runs"))
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = metadata_dir / f"{run_metadata['run_id']}.json"
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(run_metadata, f, indent=2)
        logger.info(f"Successfully recorded run metadata for {run_metadata['run_id']} at {file_path}")
    except Exception as e:
        logger.error(f"Failed to write run metadata: {str(e)}")
        raise IOError(f"Run metadata storage failed: {str(e)}") from e

    return run_metadata