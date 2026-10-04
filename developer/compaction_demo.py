"""Offline teaching example: summaries can change the status of a claim.

Both summaries below are deliberately authored fixtures, not model output.
No model, embedding service, network connection, or real agent memory is used.
"""
from copy import deepcopy
import json


def example():
    original = {
        "id": "meeting-2026-10-02:17",
        "source": "synthetic meeting transcript, line 17",
        "date": "2026-10-02",
        "speaker": "Alice",
        "kind": "report",
        "text": "I think Jordan is trying to block the project, but I have not asked why.",
        "claim": "Jordan is trying to block the project",
        "uncertainty": "Alice's interpretation; motive unverified; Jordan has not responded",
        "scope": {"owner": "alice", "domain": "project-review"},
    }
    # A deliberately bad compression promotes an interpretation into a fact.
    lossy = {"text": "Jordan is blocking the project.", "kind": "evidence"}
    preserved = {
        "text": "Alice suspects Jordan is blocking the project; motive is unverified.",
        "claim": original["claim"],
        "kind": original["kind"],
        "speaker": original["speaker"],
        "date": original["date"],
        "source": original["source"],
        "source_ids": [original["id"]],
        "uncertainty": original["uncertainty"],
        "scope": deepcopy(original["scope"]),
    }
    return original, lossy, preserved


def check_summary(original, summary):
    """Check declared metadata; this does not establish that prose is accurate."""
    problems = []
    required = ("speaker", "date", "source", "kind", "uncertainty", "scope", "claim")
    for key in required:
        if key not in summary:
            problems.append("missing_" + key)
        elif summary[key] != original[key]:
            problems.append("changed_" + key)
    if original["id"] not in summary.get("source_ids", []):
        problems.append("missing_source_id")
    return problems


def demo():
    original, lossy, preserved = example()
    return {
        "demonstration_only": True,
        "original": original,
        "lossy_summary": lossy,
        "lossy_problems": check_summary(original, lossy),
        "source_aware_summary": preserved,
        "source_aware_problems": check_summary(original, preserved),
        "limitation": "Inspect the wording too: correct metadata can accompany misleading prose.",
    }


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
