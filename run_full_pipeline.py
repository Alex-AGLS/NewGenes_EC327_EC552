#!/usr/bin/env python3
"""
run_full_pipeline.py -- end-to-end runner for the SBOL Protocol Generator.

Usage:
    python run_full_pipeline.py path/to/your.xml
    python run_full_pipeline.py demo_pBAD_GFP.xml
    python run_full_pipeline.py demo_J23100_GFP.xml -o my_output.md

The output protocol filename defaults to "protocol_<xml_basename>.md" if
not specified with -o.
"""

import sys
import os
import argparse
from pathlib import Path

from extract_xml import parse
from structure import get_table, get_pcr_info
from src.protocol_builder import build_full_protocol


def run(xml_path: str, output_path: str = None) -> str:
    """Run the full pipeline on a single SBOL XML file.

    Produces an .md protocol file. Returns the path it was written to.
    """
    xml = Path(xml_path)
    if not xml.exists():
        raise FileNotFoundError(f"SBOL XML not found: {xml_path}")

    # Default output name: protocol_<xml_stem>.md
    if output_path is None:
        output_path = f"protocol_{xml.stem}.md"

    # Use intermediate filenames keyed to the XML, so multiple runs
    # don't overwrite each other.
    stem = xml.stem
    json_path  = f"_intermediate_{stem}.json"
    parts_csv  = f"_intermediate_{stem}_parts.csv"
    pcr_csv    = f"_intermediate_{stem}_pcr.csv"
    pcr_text   = f"_intermediate_{stem}_pcr.txt"

    print(f"\n=== Running pipeline on {xml.name} ===\n")

    # --- Stage 1: SBOL XML -> JSON ---
    print(f"  [1/4] Parsing SBOL XML -> {json_path}")
    parse(str(xml), json_path)

    # --- Stage 2: JSON + scrape -> parts table CSV ---
    # NOTE: get_table reads the SBOL XML directly and uses scrape.py
    # to look up part types online. This step needs internet access.
    print(f"  [2/4] Scraping part info -> {parts_csv}")
    get_table(str(xml), parts_csv)

    # --- Stage 3: JSON -> PCR primers + protocol text ---
    print(f"  [3/4] Designing primers -> {pcr_csv}")
    get_pcr_info(json_path, pcr_text, pcr_csv)

    # --- Stage 4: Build the full multi-step protocol ---
    print(f"  [4/4] Building full protocol -> {output_path}")
    build_full_protocol(
        parts_csv=parts_csv,
        pcr_csv=pcr_csv,
        pcr_protocol_text_path=pcr_text,
        output_path=output_path,
    )

    print(f"\n[ok] Done. Output: {output_path}")
    return output_path


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("xml", help="Path to the SBOL XML file")
    p.add_argument("-o", "--output", default=None,
                   help="Output .md path (default: protocol_<xml_basename>.md)")
    p.add_argument("--show", action="store_true",
                   help="After generating, print the protocol to stdout")
    args = p.parse_args()

    out = run(args.xml, args.output)

    if args.show:
        print()
        with open(out) as f:
            print(f.read())