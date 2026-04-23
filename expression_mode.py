# src/classifier/expression_mode.py
#
# ==============================================================================
# EXPRESSION MODE CLASSIFIER
# ==============================================================================
# Given the parts table CSV produced by the teammates' pipeline
# (individualParts_sampleOutput.csv), determine:
#   1. Which part is the promoter (row with type == "promoter")
#   2. Look up that promoter in our induction database
#   3. Return a decision dict describing how to induce the circuit
#
# Input:  path to the individualParts CSV from scrape.py / structure.py
#         OR a list of (part_id, type) tuples directly
# Output: dict with induction info (see classify_from_parts_csv docstring)
#
# Also detects if a reporter (GFP/RFP/YFP/lacZ) is present in the CDS parts,
# because that determines whether a fluorescence step makes sense.
#
# Owner: [YOUR NAME]
# Last updated: 2026-04-21
# ==============================================================================

import csv
from typing import Optional, Dict, Any, List, Tuple

from src.data.promoter_induction import PROMOTER_INDUCTION, PROMOTER_ALIASES


# ------------------------------------------------------------------------------
# Reporter detection
# ------------------------------------------------------------------------------
# Map BioBrick IDs to reporter info. When a CDS row has one of these IDs,
# we know the circuit produces a visible signal.
#
# [UNVERIFIED for some entries]: the BioBrick IDs below are the most commonly
# used parts in iGEM teaching contexts, but there are many variants. This
# list should be extended as needed.
#
# Source URLs link to the iGEM Registry page for each part.
KNOWN_REPORTERS = {
    # Green fluorescent proteins
    "BBa_E0040": {
        "friendly_name": "GFP",
        "reporter_type": "fluorescent_green",
        "excitation_nm": 488,
        "emission_nm": 507,
        "color": "green",
        "source_url": "http://parts.igem.org/Part:BBa_E0040",
    },
    # Red fluorescent protein
    "BBa_E1010": {
        "friendly_name": "mRFP1",
        "reporter_type": "fluorescent_red",
        "excitation_nm": 584,
        "emission_nm": 607,
        "color": "red",
        "source_url": "http://parts.igem.org/Part:BBa_E1010",
    },
    # Yellow fluorescent protein
    "BBa_E0030": {
        "friendly_name": "YFP",
        "reporter_type": "fluorescent_yellow",
        "excitation_nm": 514,
        "emission_nm": 527,
        "color": "yellow",
        "source_url": "http://parts.igem.org/Part:BBa_E0030",
    },
}


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def _canonicalize_promoter_id(raw_id: str) -> str:
    """Resolve an input ID/name to a canonical BioBrick ID if possible."""
    raw_id = raw_id.strip()
    if raw_id in PROMOTER_INDUCTION:
        return raw_id
    if raw_id in PROMOTER_ALIASES:
        return PROMOTER_ALIASES[raw_id]
    return raw_id  # unchanged; caller will treat as unknown


def _read_parts_table(csv_path: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Read the teammates' parts table CSV into a simple list of (id, type).

    Expected format (per their sample):
        Component,<CIRCUIT_ID>
        name,type,information
        BBa_XXXX,<type>,<text>
        BBa_YYYY,<type>,<text>
        ...

    Returns:
        (circuit_id, [(part_id, type_str), ...])

    The csv is written by their structure.get_table() function.
    """
    circuit_id = ""
    parts = []
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Row 0: Component, <circuit_id>
    if rows and len(rows[0]) >= 2 and rows[0][0] == "Component":
        circuit_id = rows[0][1]

    # Row 1 is the header "name,type,information"; data starts at row 2.
    for row in rows[2:]:
        if len(row) >= 2 and row[0].strip():
            part_id = row[0].strip()
            part_type = row[1].strip() if len(row) >= 2 else ""
            parts.append((part_id, part_type))

    return circuit_id, parts


def _find_promoter(parts: List[Tuple[str, str]]) -> Optional[str]:
    """Return the BioBrick ID of the first part whose type is 'promoter'.

    Returns None if no promoter row is found. This can happen in
    two ways:
      a) the circuit truly has no promoter (unusual for expression circuits)
      b) the scraper couldn't classify the type (empty string)
    Either way, we return None and let the caller emit an 'unknown' decision.
    """
    for part_id, part_type in parts:
        if part_type.lower() == "promoter":
            return part_id
    return None


def _find_reporter(parts: List[Tuple[str, str]]) -> Optional[Dict[str, Any]]:
    """Find the first part whose BioBrick ID matches a known reporter.

    Returns the reporter entry dict (with color, excitation, etc.)
    or None if no reporter is present.
    """
    for part_id, _ in parts:
        if part_id in KNOWN_REPORTERS:
            return {"part_id": part_id, **KNOWN_REPORTERS[part_id]}
    return None


# ------------------------------------------------------------------------------
# Public classifier entry points
# ------------------------------------------------------------------------------

def classify_expression_mode(promoter_id: Optional[str]) -> Dict[str, Any]:
    """Classify a single promoter ID into an induction mode.

    Args:
        promoter_id: BioBrick ID (e.g. 'BBa_R0040') or friendly name
                     (e.g. 'pTet'). Can be None.

    Returns:
        Dict with these keys (always present):
          - mode: "inducible_small_molecule", "constitutive", or "unknown"
          - promoter_id: canonical BioBrick ID we resolved to
          - friendly_name: human-readable promoter name
          - inducer, inducer_concentration, induction_hours, strain_warning:
                populated if inducible, else None
          - notes: explanatory message for the template / user
    """
    if promoter_id is None or str(promoter_id).strip() == "":
        return _unknown_result(
            raw_input=promoter_id,
            reason="No promoter was found in the circuit's parts table.",
        )

    canonical = _canonicalize_promoter_id(str(promoter_id))
    entry = PROMOTER_INDUCTION.get(canonical)

    if entry is None:
        return _unknown_result(
            raw_input=promoter_id,
            reason=(
                f"Promoter '{promoter_id}' is not in the supported library. "
                f"Supported IDs: {sorted(PROMOTER_INDUCTION.keys())}"
            ),
        )

    if entry["mode"] == "constitutive":
        return {
            "mode": "constitutive",
            "promoter_id": canonical,
            "friendly_name": entry["friendly_name"],
            "inducer": None,
            "inducer_concentration": None,
            "induction_hours": None,
            "strain_warning": None,
            "notes": (
                f"{entry['friendly_name']} ({canonical}) is a constitutive "
                f"promoter; no induction step needed."
            ),
        }

    if entry["mode"] == "inducible_small_molecule":
        return {
            "mode": "inducible_small_molecule",
            "promoter_id": canonical,
            "friendly_name": entry["friendly_name"],
            "inducer": entry["inducer"],
            "inducer_concentration": entry["inducer_concentration"],
            "induction_hours": entry["induction_hours"],
            "strain_warning": entry.get("strain_warning"),
            "notes": (
                f"{entry['friendly_name']} ({canonical}) is induced by "
                f"{entry['inducer']} at {entry['inducer_concentration']}."
            ),
        }

    # Defensive: data-file bug
    return _unknown_result(
        raw_input=promoter_id,
        reason=(
            f"Data file has unrecognized mode '{entry['mode']}' for "
            f"{canonical}. Fix src/data/promoter_induction.py."
        ),
    )


def classify_from_parts_csv(csv_path: str) -> Dict[str, Any]:
    """High-level entry point: read the teammates' parts CSV and classify.

    Args:
        csv_path: path to individualParts_sampleOutput.csv-style file

    Returns:
        Dict with keys:
          - circuit_id: top-level composite part ID (e.g. "BBa_I0462")
          - expression: dict returned by classify_expression_mode()
          - reporter: dict describing the reporter (or None if absent)
          - parts: raw list of (part_id, part_type) tuples (for templates)
    """
    circuit_id, parts = _read_parts_table(csv_path)
    promoter_id = _find_promoter(parts)
    expression = classify_expression_mode(promoter_id)
    reporter = _find_reporter(parts)

    return {
        "circuit_id": circuit_id,
        "expression": expression,
        "reporter": reporter,
        "parts": parts,
    }


# ------------------------------------------------------------------------------
# Private helpers
# ------------------------------------------------------------------------------

def _unknown_result(raw_input: Any, reason: str) -> Dict[str, Any]:
    """Build an 'unknown' classification result."""
    return {
        "mode": "unknown",
        "promoter_id": raw_input,
        "friendly_name": None,
        "inducer": None,
        "inducer_concentration": None,
        "induction_hours": None,
        "strain_warning": None,
        "notes": reason,
    }
