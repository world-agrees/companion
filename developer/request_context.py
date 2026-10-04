"""Check a selected context manifest; not an authentication system.

An application must authorize the caller and source selection BEFORE
passing a manifest here. A matching digest detects a changed manifest,
not an authorized identity, trustworthy source, or correct statement.
"""

from copy import deepcopy
from hashlib import sha256
import json


def checked_context(manifest):
    """Recheck declared scope, provenance, status and content digest."""
    if not isinstance(manifest, dict):
        raise ValueError("context must be a Store.context() manifest")
    owner, domain = manifest.get("owner"), manifest.get("domain")
    if not all(isinstance(value, str) and value.strip()
               for value in (owner, domain)):
        raise ValueError("explicit owner and domain are required")
    records = manifest.get("records")
    if not isinstance(records, list):
        raise ValueError("records must be an explicitly selected list")
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each selected record must be an object")
        if not all(isinstance(record.get(key), str)
                   and record[key].strip()
                   for key in ("id", "text", "source", "kind")):
            raise ValueError("record needs an ID, text, source and kind")
        if record["id"] in seen:
            raise ValueError("duplicate context ID")
        seen.add(record["id"])
        if (record.get("owner"), record.get("domain")) != (
                owner, domain):
            raise PermissionError("record outside declared scope")
        if record.get("status") != "current":
            raise ValueError("obsolete or unreviewed context rejected")
        if record["kind"] not in {
            "preference", "report", "evidence", "inference"
        }:
            raise ValueError("unknown context kind")
    payload = {"owner": owner, "domain": domain,
               "records": deepcopy(records)}
    encoded = json.dumps(payload, sort_keys=True,
                         ensure_ascii=False).encode()
    digest = sha256(encoded).hexdigest()
    if manifest.get("sha256") != digest:
        raise ValueError("context manifest hash does not match")
    return {**payload, "sha256": digest}
