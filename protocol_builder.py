# src/protocol_builder.py
#
# ==============================================================================
# PROTOCOL BUILDER -- the main orchestrator for our part of the project
# ==============================================================================
# Reads the teammates' output files:
#   - individualParts_sampleOutput.csv  (parts table from structure.get_table)
#   - pcr_SampleOutput.csv              (PCR summary from structure.get_pcr_info)
#   - sample.txt  OR  the teammates' PCR protocol text                (optional)
#
# Produces:
#   - A combined full protocol document covering Steps 1..N
#     (PCR by teammates + cloning + transformation + colony verification +
#     fluorescence check -- the last 4 are our responsibility)
#
# Usage from Python:
#   from src.protocol_builder import build_full_protocol
#   build_full_protocol(
#       parts_csv="individualParts_sampleOutput.csv",
#       pcr_csv="pcr_SampleOutput.csv",
#       pcr_protocol_text_path="sample.txt",   # optional
#       output_path="full_protocol.md",
#   )
#
# Owner: [YOUR NAME]
# Last updated: 2026-04-21
# ==============================================================================

import csv
import os
from datetime import date
from typing import Optional

from expression_mode import classify_from_parts_csv
from cloning import get_cloning_template
from transformation import get_transformation_template
from colony_verification import get_colony_verification_template
from fluorescence_check import get_fluorescence_check_template


# ==============================================================================
# Helpers for reading the teammates' CSVs
# ==============================================================================

def _read_pcr_csv(pcr_csv_path: str) -> dict:
    """Read the teammates' pcr_SampleOutput.csv.

    Expected format:
        part,forward primer,reverse primer,temperature,time
        BBa_I0462,aatgtttagcgtgggcatgc,gcgttcaccgacaaacaaca,81.31,56.16

    Returns a dict of the first data row with safely-parsed values,
    or an empty dict if the file is missing / malformed. Missing fields
    are tolerated so the downstream templates still render.
    """
    result = {
        "part": None,
        "forward_primer": None,
        "reverse_primer": None,
        "temperature": None,
        "time": None,
    }
    if not os.path.exists(pcr_csv_path):
        return result

    with open(pcr_csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result["part"]           = (row.get("part") or "").strip() or None
            result["forward_primer"] = (row.get("forward primer") or "").strip() or None
            result["reverse_primer"] = (row.get("reverse primer") or "").strip() or None

            # temperature / time are floats in the sample; be defensive
            try:
                result["temperature"] = float(row.get("temperature", ""))
            except (ValueError, TypeError):
                result["temperature"] = None
            try:
                result["time"] = float(row.get("time", ""))
            except (ValueError, TypeError):
                result["time"] = None

            break  # only read the first data row
    return result


def _read_pcr_protocol_text(txt_path: Optional[str]) -> str:
    """Read the teammates' PCR protocol text file (if provided).

    Falls back to a brief placeholder if the file is missing.
    """
    if txt_path and os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read().strip()
    return ""


# ==============================================================================
# Section builders
# ==============================================================================

def _build_header(circuit_id: str, classification: dict) -> str:
    """Top-of-document header with metadata."""
    promoter_line = "(promoter not detected)"
    expr = classification["expression"]
    if expr["mode"] != "unknown":
        promoter_line = (
            f"{expr.get('friendly_name') or '?'} "
            f"({expr.get('promoter_id') or '?'})"
        )

    reporter_line = "(no fluorescent reporter detected)"
    if classification["reporter"]:
        r = classification["reporter"]
        reporter_line = (
            f"{r['friendly_name']} "
            f"(emission ~{r['emission_nm']} nm, {r['color']})"
        )

    return (
        f"# Lab Protocol: {circuit_id}\n"
        f"\n"
        f"**Generated:** {date.today().isoformat()}  \n"
        f"**Assembly method:** single-insert cloning (after PCR amplification)  \n"
        f"**Detected promoter:** {promoter_line}  \n"
        f"**Detected reporter:** {reporter_line}  \n"
        f"**Expression mode:** {expr['mode']}  \n"
        f"\n"
        f"---\n"
    )


def _build_parts_table(classification: dict) -> str:
    """Render the parts table from the classifier's 'parts' field."""
    parts = classification["parts"]
    if not parts:
        return (
            "## Parts list\n"
            "\n"
            "(No parts found in the parts table CSV.)\n"
            "\n"
        )

    lines = [
        "## Parts list",
        "",
        "| # | BioBrick ID | Type |",
        "|---|-------------|------|",
    ]
    for i, (part_id, part_type) in enumerate(parts, start=1):
        displayed_type = part_type if part_type else "(unknown)"
        lines.append(f"| {i} | {part_id} | {displayed_type} |")
    lines.append("")
    return "\n".join(lines)


def _build_pcr_section(step_num: int, pcr_info: dict, pcr_text: str) -> str:
    """Show the PCR step produced by the teammates.

    Prefers showing the full text of their sample.txt (so the full NEB-style
    procedure is preserved). Falls back to a summary from the CSV if sample.txt
    is missing.
    """
    header = f"## Step {step_num}: PCR amplification (generated upstream)\n\n"

    if pcr_text:
        return header + pcr_text + "\n"

    # Fallback summary from the CSV
    part = pcr_info.get("part") or "(unknown)"
    forward = pcr_info.get("forward_primer") or "(unknown)"
    reverse = pcr_info.get("reverse_primer") or "(unknown)"
    temp = pcr_info.get("temperature")
    time_val = pcr_info.get("time")

    temp_str = f"{temp:.2f} C" if isinstance(temp, float) else "(unknown)"
    time_str = f"{time_val:.2f} seconds" if isinstance(time_val, float) else "(unknown)"

    return (
        f"{header}"
        f"PCR amplify the composite part {part} using the following primers\n"
        f"and thermocycler settings (computed by primer3 in the upstream step):\n"
        f"\n"
        f"  - Forward primer: {forward}\n"
        f"  - Reverse primer: {reverse}\n"
        f"  - Annealing / melting temperature: {temp_str}\n"
        f"  - Extension time: {time_str}\n"
        f"\n"
        f"For the full reaction mix and cycling program, use NEB's Q5\n"
        f"High-Fidelity DNA Polymerase protocol (M0491) as the reference.\n"
        f"\n"
        f"*Source: upstream PCR design step (request_primer.py + structure.py).*\n"
    )


def _build_disclaimer() -> str:
    return (
        "\n"
        "---\n"
        "\n"
        "## Disclaimer\n"
        "\n"
        "This protocol was auto-generated from an SBOL structural\n"
        "description using deterministic templates based on published\n"
        "laboratory protocols. It has NOT been validated experimentally.\n"
        "Before attempting in a real laboratory:\n"
        "\n"
        "  - A qualified biologist must review all steps for correctness\n"
        "    in the specific experimental context.\n"
        "  - Parts are assumed available as purified DNA in a local\n"
        "    part library.\n"
        "  - PCR primer sequences were computed algorithmically and are\n"
        "    not guaranteed to be optimal.\n"
        "  - All safety procedures of the host institution take\n"
        "    precedence.\n"
        "\n"
        "Template sources are cited inline and in the References section\n"
        "of the source code.\n"
    )


# ==============================================================================
# Main entry point
# ==============================================================================

def build_full_protocol(
    parts_csv: str,
    pcr_csv: Optional[str] = None,
    pcr_protocol_text_path: Optional[str] = None,
    output_path: Optional[str] = None,
) -> str:
    """Build the full multi-step lab protocol and return it as a string.

    Args:
        parts_csv:              Path to individualParts_sampleOutput.csv
                                (required).
        pcr_csv:                Path to pcr_SampleOutput.csv (optional but
                                recommended -- needed for the PCR section).
        pcr_protocol_text_path: Path to sample.txt from structure.py
                                (optional; if present, its full text is
                                included verbatim as the PCR step).
        output_path:            If provided, write the full protocol to
                                this file as well as returning it.

    Returns:
        The full protocol as a single string (Markdown-formatted text).
    """

    # Run the classifier on the parts table
    classification = classify_from_parts_csv(parts_csv)
    circuit_id = classification["circuit_id"] or "(unnamed_circuit)"

    # Read the teammates' PCR outputs if available
    pcr_info = _read_pcr_csv(pcr_csv) if pcr_csv else {}
    pcr_text = _read_pcr_protocol_text(pcr_protocol_text_path)

    # ---- Build the document, step by step ------------------------------------
    sections = []
    sections.append(_build_header(circuit_id, classification))
    sections.append(_build_parts_table(classification))

    step = 1
    sections.append(_build_pcr_section(step, pcr_info, pcr_text)); step += 1
    sections.append(get_cloning_template(step, circuit_id)); step += 1

    # Transformation: propagate strain warning from the promoter (if any)
    expr = classification["expression"]
    strain_warning = expr.get("strain_warning") if expr["mode"] != "unknown" else None
    sections.append(
        get_transformation_template(step, strain_warning=strain_warning)
    ); step += 1

    sections.append(get_colony_verification_template(step, circuit_id)); step += 1

    # Fluorescence check: branches inside the template based on expression mode
    sections.append(
        get_fluorescence_check_template(
            step_num=step,
            expression_decision=expr,
            reporter=classification["reporter"],
        )
    )

    sections.append(_build_disclaimer())

    full_text = "\n".join(sections)

    if output_path:
        # Make sure the output directory exists
        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)

    return full_text


# ==============================================================================
# CLI entry point (so the teammates can run this from their main script)
# ==============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Build a full lab protocol from SBOL-pipeline outputs."
    )
    parser.add_argument(
        "--parts", required=True,
        help="Path to individualParts_sampleOutput.csv"
    )
    parser.add_argument(
        "--pcr", default=None,
        help="Path to pcr_SampleOutput.csv (optional)"
    )
    parser.add_argument(
        "--pcr-text", default=None,
        help="Path to the PCR protocol text file (sample.txt) (optional)"
    )
    parser.add_argument(
        "--out", default="full_protocol.md",
        help="Where to write the combined protocol (default: full_protocol.md)"
    )
    args = parser.parse_args()

    text = build_full_protocol(
        parts_csv=args.parts,
        pcr_csv=args.pcr,
        pcr_protocol_text_path=args.pcr_text,
        output_path=args.out,
    )
    print(f"[ok] Wrote full protocol to {args.out} ({len(text)} characters).")
