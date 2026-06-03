"""
File I/O storage handler. Reads and writes JSON data files for persistence.
"""
import json
import os
from typing import List, Dict, Any, Optional

DATA_DIR = os.environ.get("DATA_DIR") or os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class Storage:
    """Handles all file I/O operations for data persistence."""

    def __init__(self, filename: str):
        self.filepath = os.path.join(DATA_DIR, filename)
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(self.filepath):
            self._write([])

    def _read(self) -> List[Dict]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, data: List[Dict]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def get_all(self) -> List[Dict]:
        return self._read()

    def get_by_id(self, record_id: str) -> Optional[Dict]:
        records = self._read()
        return next((r for r in records if r.get("id") == record_id), None)

    def get_by_field(self, field: str, value: Any) -> Optional[Dict]:
        records = self._read()
        return next((r for r in records if r.get(field) == value), None)

    def get_many_by_field(self, field: str, value: Any) -> List[Dict]:
        records = self._read()
        return [r for r in records if r.get(field) == value]

    def create(self, record: Dict) -> Dict:
        records = self._read()
        records.append(record)
        self._write(records)
        return record

    def update(self, record_id: str, updates: Dict) -> Optional[Dict]:
        records = self._read()
        for i, r in enumerate(records):
            if r.get("id") == record_id:
                records[i].update(updates)
                self._write(records)
                return records[i]
        return None

    def delete(self, record_id: str) -> bool:
        records = self._read()
        new_records = [r for r in records if r.get("id") != record_id]
        if len(new_records) == len(records):
            return False
        self._write(new_records)
        return True

    def replace_all(self, data: List[Dict]) -> None:
        self._write(data)
