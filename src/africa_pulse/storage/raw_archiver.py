import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

def save_raw_response(
    source_name: str, 
    raw_payload: Any, 
    request_params: Dict[str, Any], 
    run_id: str,
    base_raw_dir: str = "data/raw"
) -> Path:
    """
    Preserves an original API response unmodified along with diagnostic metadata.
    Files are organized by source and named with timestamp and run_id.
    """
    raw_dir = Path(base_raw_dir) / source_name
    raw_dir.mkdir(parents=True, exist_ok=True)

    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{timestamp_str}_{run_id}.json"
    file_path = raw_dir / filename

    archival_envelope = {
        "source": source_name,
        "run_id": run_id,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "request_params": request_params,
        "raw_response": raw_payload
    }

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(archival_envelope, f, indent=2)
        logger.info(f"Successfully archived raw response for {source_name} at {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to archive raw response: {str(e)}")
        raise IOError(f"Raw response archival failed: {str(e)}") from e

def load_and_reprocess(file_path: str, parsing_function: Callable[[Any], Any]) -> Any:
    """
    Reads a saved raw response back from disk and runs it through a reprocessing/parsing function.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Archived raw response not found at {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        archival_envelope = json.load(f)

    logger.info(f"Loaded raw response from {file_path}, collected at {archival_envelope.get('collected_at')}")
    
    return parsing_function(archival_envelope["raw_response"])