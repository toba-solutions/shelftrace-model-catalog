"""Check that the public catalog follows Shelftrace's v1 format."""

import json
import re
from datetime import date
from pathlib import Path


CATALOG = Path(__file__).resolve().parents[1] / "models-v1.json"
MODEL_IDS = {
    "openai": r"[A-Za-z0-9._:-]{1,256}",
    "claude": r"[A-Za-z0-9._:-]{1,256}",
    "gemini": r"[A-Za-z0-9._-]{1,256}",
    "mistral": r"[A-Za-z0-9._:-]{1,256}",
}


def validate_entry(entry, model_pattern, seen, location):
    if not isinstance(entry, dict):
        raise ValueError(f"{location} must be an object")
    model_id = entry.get("id")
    if not isinstance(model_id, str) or not re.fullmatch(model_pattern, model_id):
        raise ValueError(f"{location}.id must be a valid API model ID")
    if model_id in seen:
        raise ValueError(f"{location}.id duplicates {model_id!r} in this provider")
    seen.add(model_id)

    name = entry.get("name")
    if not isinstance(name, str) or not name.strip() or len(name) > 128:
        raise ValueError(f"{location}.name must have 1–128 characters")
    for field in ("compatible", "recommended"):
        if not isinstance(entry.get(field), bool):
            raise ValueError(f"{location}.{field} must be a boolean")

    note = entry.get("note")
    if note is not None and (not isinstance(note, str) or len(note) > 240):
        raise ValueError(f"{location}.note must be text of up to 240 characters")
    retirement = entry.get("retiresOn")
    if retirement is not None:
        try:
            if not isinstance(retirement, str) or date.fromisoformat(retirement).isoformat() != retirement:
                raise ValueError
        except ValueError:
            raise ValueError(f"{location}.retiresOn must be a date in YYYY-MM-DD format") from None


def validate(data):
    if len(data) > 256_000:
        raise ValueError("catalog exceeds the app's 256,000 byte limit")
    catalog = json.loads(data)
    if not isinstance(catalog, dict) or type(catalog.get("schemaVersion")) is not int or catalog["schemaVersion"] != 1:
        raise ValueError("schemaVersion must be the integer 1")
    providers = catalog.get("providers")
    if not isinstance(providers, dict):
        raise ValueError("providers must be an object")
    total = 0
    for provider, entries in providers.items():
        if provider not in MODEL_IDS or not isinstance(entries, list):
            raise ValueError(f"providers.{provider} must be a model list for a supported provider")
        seen = set()
        total += len(entries)
        for index, entry in enumerate(entries):
            validate_entry(entry, MODEL_IDS[provider], seen, f"providers.{provider}[{index}]")
    if total > 800:
        raise ValueError("catalog exceeds the app's 800 entry limit")
    return total


if __name__ == "__main__":
    try:
        count = validate(CATALOG.read_bytes())
    except (OSError, ValueError) as error:
        raise SystemExit(f"{CATALOG.name}: {error}") from None
    print(f"{CATALOG.name}: {count} entries passed validation")
