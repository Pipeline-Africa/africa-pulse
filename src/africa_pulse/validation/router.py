import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple
from pathlib import Path
import warnings


logger = logging.getLogger(__name__)

@dataclass
class ValidationOutcome:
    status: str   # 'valid', 'warning', 'quarantined'
    reason: str = None
    record: Dict[str, Any] = None
    
    
class DataIngestionRouter:
    def __init__(self, quarantined_dir: str = "data/quarantined"):
        self.quarantined_dir = Path(quarantined_dir)
        self.quarantined_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_record(self, record: Dict[str, Any]) -> ValidationOutcome:
        """
        Evaluates a raw record against agreed failure modes (from Issue #13):
        - Missing mandatory fields (timestamp, source_id, value) -> Quarantine
        - Implausible values or invalid formats -> Quarantine or Warning
        """
        # missing mandatory fields
        if not record.get("timestamp") or not record.get("source_id") or not record.get("value"):
            return ValidationOutcome(status="quarantined", reason="Missing mandatory fields", record=record)
        
        # implausible values or range checks
        val = record.get("value")
        if isinstance(val, (int, float)):
            # example range check for weather/ air quality data
            if val < -100 or val > 100:
                return ValidationOutcome(status="quarantined", reason="Implausible value", record=record)
            if val < 0:
                return ValidationOutcome(status="warning", reason="Negative value", record=record)
        return ValidationOutcome(status="valid", reason="Record is valid", record=record)
    
    
    def write_to_quarantine(self, quarantined_records: List[Dict[str, Any]], run_id: str) -> bool:
        """
        Safely writes quarantined payloads to disk/storage with run metadata.
        Includes storage failure handling.
        """
        if not quarantined_records:
            return True  # Nothing to write
        
        filename = f"quarantined_{run_id}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
        file_path = self.quarantined_dir / filename
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for quarantined_record in quarantined_records:
                    json.dump(quarantined_record, f, indent=4)
            logger.info(f"Successfully wrote {len(quarantined_records)} quarantined records to {file_path}")
            return True
        except Exception as e:
            logger.error(f"STORAGE FAILURE: Could not write quarantined records: {str(e)}")
            raise IOError(f"Failed to write quarantined records: {str(e)}") from e
        
        
    def process_batch(self, raw_records: List[Dict[str, Any]], run_id: str) -> Dict[str, Any]:
        """
        Processes a batch of raw records, validates them, and routes them accordingly.
        Returns a summary of the processing outcome.
        """
        valid_records = []
        quarantined_records = []
        warnings_count = 0
        
        for raw_record in raw_records:
            outcome = self.validate_record(raw_record)
            
            if outcome.status == "valid":
                valid_records.append(outcome.record)
            elif outcome.status == "warning":
                flagged_message = {**outcome.record, "ingestion_warning": outcome.reason, "run_id": run_id}
                valid_records.append(flagged_message)
                warnings_count += 1
            elif outcome.status == "quarantined":
                quarantined_records = {
                    "run_id": run_id,
                    "source_id": raw_record.get("source_id", "unknown"),
                    "failure_reason": outcome.reason,
                    "raw_payload": raw_record,
                    "quarantined_at": datetime.now(timezone.utc).isoformat()
                }
                quarantined_records.append(quarantined_records)
                
        
        # Flush quarantined records to disk
        if quarantined_records:
            self.write_to_quarantine(quarantined_records, run_id)
            
        summary = {
            "run_id": run_id,
            "total_records": len(raw_records),
            "valid_records": len(valid_records),
            "quarantined_records": len(quarantined_records),
            "warnings_count": warnings_count,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logger.info(f"Batch processing {run_id} summary: {summary}")
        return {
            "summary": summary,
            "valid_records": valid_records,
            "quarantined_records": quarantined_records
        }