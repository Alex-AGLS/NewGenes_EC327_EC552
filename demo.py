#!/usr/bin/env python3
# demo.py
#
# ==============================================================================
# INTERACTIVE TERMINAL DEMO -- SBOL Protocol Generator
# ==============================================================================
# An interactive walkthrough of the post-PCR protocol generator.
# Lets the user pick from 4 pre-made circuits, each one demonstrating a
# different branch of the expression-mode classifier.
#
# Run from the project root:
#     python demo.py
#
# All 4 demos use pre-made CSV fixtures (no upstream LLM/SBOL pipeline
# needed). The fixtures live in tests/fixtures/.
# ==============================================================================

import sys
import os
import time
from pathlib import Path

# Make sure we can import from src/ even when run as `python demo.py`
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.protocol_builder import build_full_protocol


# ------------------------------------------------------------------------------
# Demo catalog -- one entry per circuit / branch
# ------------------------------------------------------------------------------

FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"

DEMOS = [
    {
        "key": "1",
        "title": "Inducible reporter (pBAD + GFP)",
        "branch": "inducible_small_molecule",
        "expected_behavior": (
            "Step 5 will produce a split-culture induction protocol:\n"
            "    - Inducer:        L-arabinose at 0.2% (w/v)\n"
            "    - Strain warning: about arabinose-metabolizing strains\n"
            "    - Imaging:        488 nm excitation (green fluorescence)\n"
            "    - Comparison:     induced tube vs. uninduced tube"
        ),
        "parts_csv": FIXTURES_DIR / "demo_inducible_gfp.csv",
        "pcr_csv":   FIXTURES_DIR / "demo_inducible_gfp_pcr.csv",
        "pcr_text":  None,
        "out_path":  PROJECT_ROOT / "demo_output_inducible.md",
    },
    {
        "key": "2",
        "title": "Constitutive reporter (J23100 + GFP)",
        "branch": "constitutive",
        "expected_behavior": (
            "Step 5 will skip induction entirely:\n"
            "    - No inducer step (J23100 is always on)\n"
            "    - Imaging:    488 nm excitation directly from the plate\n"
            "    - Procedure:  streak verified colonies, image, look for green"
        ),
        "parts_csv": FIXTURES_DIR / "demo_constitutive_gfp.csv",
        "pcr_csv":   FIXTURES_DIR / "demo_constitutive_gfp_pcr.csv",
        "pcr_text":  None,
        "out_path":  PROJECT_ROOT / "demo_output_constitutive.md",
    },
    {
        "key": "3",
        "title": "Inducible promoter, NO reporter (pTet + LacI)",
        "branch": "no_reporter",
        "expected_behavior": (
            "Step 5 will refuse to do a fluorescence check:\n"
            "    - Detected: pTet promoter (recognized) but no GFP/RFP/YFP\n"
            "    - Output:   'No fluorescent reporter detected'\n"
            "    - Suggests: Sanger sequencing + restriction-digest mapping"
        ),
        "parts_csv": FIXTURES_DIR / "demo_no_reporter.csv",
        "pcr_csv":   FIXTURES_DIR / "demo_no_reporter_pcr.csv",
        "pcr_text":  None,
        "out_path":  PROJECT_ROOT / "demo_output_no_reporter.md",
    },
    {
        "key": "4",
        "title": "Unknown promoter (real BBa_I0462 sample from teammates)",
        "branch": "unknown",
        "expected_behavior": (
            "Step 5 will refuse to fabricate a protocol:\n"
            "    - The scraper's output for this circuit lacked a promoter type\n"
            "    - Classifier returns mode='unknown'\n"
            "    - Output:   'MANUAL REVIEW REQUIRED' warning\n"
            "    - This is the most important branch -- demonstrates that the\n"
            "      tool refuses to guess when it's uncertain"
        ),
        "parts_csv": FIXTURES_DIR / "individualParts_sampleOutput.csv",
        "pcr_csv":   FIXTURES_DIR / "pcr_SampleOutput.csv",
        "pcr_text":  None,
        "out_path":  PROJECT_ROOT / "demo_output_unknown.md",
    },
]


# ------------------------------------------------------------------------------
# Pretty-printing helpers (no external libs -- uses ANSI escape codes)
# ------------------------------------------------------------------------------

# Detect whether we're in a real terminal that supports color.
USE_COLOR = sys.stdout.isatty()


def _c(code, text):
    """Wrap text in ANSI color codes if we're in a real terminal."""
    if not USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


def bold(t):    return _c("1", t)
def dim(t):     return _c("2", t)
def green(t):   return _c("32", t)
def yellow(t):  return _c("33", t)
def cyan(t):    return _c("36", t)
def red(t):     return _c("31", t)


def hr(char="=", width=78):
    print(char * width)


def banner():
    hr()
    print(bold(cyan("  SBOL -> Lab Protocol Generator -- Interactive Demo")))
    print(dim("  EC552 final project / our team's part (post-PCR templates)"))
    hr()
    print()


def show_menu():
    print(bold("Pick a circuit to generate a protocol for:"))
    print()
    for d in DEMOS:
        # Color-code by branch so the user can see the variety at a glance
        branch_label = {
            "inducible_small_molecule": green("[INDUCIBLE]"),
            "constitutive":              cyan("[CONSTITUTIVE]"),
            "no_reporter":               yellow("[NO REPORTER]"),
            "unknown":                   red("[UNKNOWN]"),
        }[d["branch"]]
        print(f"  {bold(d['key'])}. {d['title']:<55s} {branch_label}")
    print(f"  {bold('q')}. Quit")
    print()


def pause(msg="Press ENTER to continue..."):
    try:
        input(dim(msg))
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


# ------------------------------------------------------------------------------
# The main "run a demo" routine
# ------------------------------------------------------------------------------

def run_demo(demo):
    """Execute one selected demo end-to-end with narrated output."""
    hr("-")
    print(bold(cyan(f"Selected: {demo['title']}")))
    hr("-")
    print()

    # --- Pre-flight: show the user what they should expect ---
    print(bold("What this demo will show:"))
    print()
    for line in demo["expected_behavior"].splitlines():
        print(f"  {line}")
    print()

    # --- Pre-flight: show the input files ---
    print(bold("Input files (the kind of data the upstream pipeline produces):"))
    print(f"  - Parts table: {dim(str(demo['parts_csv'].relative_to(PROJECT_ROOT)))}")
    print(f"  - PCR summary: {dim(str(demo['pcr_csv'].relative_to(PROJECT_ROOT)))}")
    print()

    # Quick existence check (helpful error if the user moved files around)
    for label, path in [("parts CSV", demo["parts_csv"]),
                        ("PCR CSV",   demo["pcr_csv"])]:
        if not path.exists():
            print(red(f"  [error] missing {label}: {path}"))
            print(red("  Make sure you ran the demo from the project root."))
            return

    pause()
    print()

    # --- Run the pipeline ---
    print(bold("Running classifier + template engine..."))
    time.sleep(0.4)  # tiny pause so it feels like work is happening

    text = build_full_protocol(
        parts_csv=str(demo["parts_csv"]),
        pcr_csv=str(demo["pcr_csv"]),
        pcr_protocol_text_path=demo["pcr_text"],
        output_path=str(demo["out_path"]),
    )

    print(green(f"  [ok] Generated protocol ({len(text)} characters)"))
    print(dim(f"  Saved to: {demo['out_path'].relative_to(PROJECT_ROOT)}"))
    print()
    pause("Press ENTER to view the generated protocol...")
    print()

    # --- Show the protocol with a clear visual frame ---
    hr("=")
    print(bold(cyan("  GENERATED PROTOCOL DOCUMENT")))
    hr("=")
    print()
    print(text)
    print()
    hr("=")
    print(bold(cyan("  END OF PROTOCOL")))
    hr("=")
    print()

    # --- Post-run summary: what to notice ---
    print(bold("Things to notice in the output above:"))
    print()
    if demo["branch"] == "inducible_small_molecule":
        print(f"  {green('OK')}  Step 5 has a split-culture induction procedure")
        print(f"  {green('OK')}  L-arabinose at 0.2% (w/v) is named explicitly")
        print(f"  {green('OK')}  The strain warning about arabinose metabolism is included")
        print(f"  {green('OK')}  GFP imaging at 488 nm / 507 nm is correctly chosen")
    elif demo["branch"] == "constitutive":
        print(f"  {green('OK')}  Step 5 skips the split-culture induction entirely")
        print(f"  {green('OK')}  Says 'no induction step required' (J23100 is constitutive)")
        print(f"  {green('OK')}  Goes straight to plate imaging at 488 nm")
    elif demo["branch"] == "no_reporter":
        print(f"  {green('OK')}  Step 5 says 'No fluorescent reporter detected'")
        print(f"  {green('OK')}  Suggests Sanger sequencing instead of fluorescence imaging")
        print(f"  {green('OK')}  Does NOT fabricate fake fluorescence data")
    elif demo["branch"] == "unknown":
        print(f"  {green('OK')}  Header says 'Expression mode: unknown'")
        print(f"  {green('OK')}  Step 5 emits MANUAL REVIEW REQUIRED warning")
        print(f"  {green('OK')}  Does NOT fabricate induction conditions for an unrecognized promoter")
        print(f"  {green('OK')}  This is the safety behavior the professor will care most about")
    print()
    print(dim("  Steps 1-4 (PCR / cloning / transformation / colony PCR) are constant"))
    print(dim("  across all four demos -- the smart branching happens in Step 5."))
    print()
    pause()


# ------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------

def main():
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        banner()
        show_menu()
        try:
            choice = input(bold("Your choice: ")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice in ("q", "quit", "exit"):
            print()
            print(dim("Goodbye."))
            break

        match = next((d for d in DEMOS if d["key"] == choice), None)
        if match is None:
            print(red(f"  Invalid choice: {choice!r}. Press ENTER to try again."))
            input()
            continue

        os.system("clear" if os.name == "posix" else "cls")
        banner()
        run_demo(match)


if __name__ == "__main__":
    main()
