import json
import os
from datetime import datetime

class MetadataStore:

    def __init__(self, file_path="metadata/metadata.json"):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def _read(self):
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []

    def _write(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add(self, record: dict):
        data = self._read()

        record["created_at"] = datetime.now().isoformat()

        data.append(record)

        self._write(data)

    def get_all(self):
        return self._read()

    def search(self, key: str, value: str):
        data = self._read()

        results = []
        for item in data:
            if key in item and str(item[key]).lower() == value.lower():
                results.append(item)

        return results






