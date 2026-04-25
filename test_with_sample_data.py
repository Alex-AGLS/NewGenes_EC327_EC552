# tests/test_with_sample_data.py
#
# ==============================================================================
# END-TO-END TESTS USING THE TEAMMATES' ACTUAL SAMPLE FILES
# ==============================================================================
# Runs the full pipeline against the real BBa_I0462 output produced by the
# teammates' structure.py, and checks that our code produces a sensible
# result.
#
# Run with:
#   python -m tests.test_with_sample_data
# or (if you have pytest):
#   python -m pytest tests/test_with_sample_data.py -v
#
# The sample fixtures are in tests/fixtures/ (copies of the files the
# teammates uploaded).
# ==============================================================================

import os
import sys
from pathlib import Path

# Let this file be runnable both from the project root and from inside tests/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from expression_mode import (
    classify_expression_mode,
    classify_from_parts_csv,
    KNOWN_REPORTERS,
)
from cloning import get_cloning_template
from transformation import get_transformation_template
from colony_verification import get_colony_verification_template
from fluorescence_check import get_fluorescence_check_template
from protocol_builder import build_full_protocol


FIXTURES = Path(__file__).resolve().parent / "fixtures"
PARTS_CSV =  Path("individualParts_sampleOutput.csv")
PCR_CSV   =  Path("pcr_SampleOutput.csv")


# ==============================================================================
# 1. Basic unit tests: classifier with known IDs
# ==============================================================================

def test_classify_pTet_by_biobrick_id():
    result = classify_expression_mode("BBa_R0040")
    assert result["mode"] == "inducible_small_molecule"
    assert "anhydrotetracycline" in result["inducer"]
    assert result["inducer_concentration"] == "100 ng/mL"
    assert result["promoter_id"] == "BBa_R0040"
    print("  [PASS] test_classify_pTet_by_biobrick_id")


def test_classify_pBAD_has_strain_warning():
    result = classify_expression_mode("BBa_I0500")
    assert result["mode"] == "inducible_small_molecule"
    assert result["inducer"] == "L-arabinose"
    assert result["strain_warning"] is not None
    assert "metabolize arabinose" in result["strain_warning"]
    print("  [PASS] test_classify_pBAD_has_strain_warning")


def test_classify_pLux_has_luxR_warning():
    result = classify_expression_mode("BBa_R0062")
    assert result["mode"] == "inducible_small_molecule"
    assert "AHL" in result["inducer"] or "HSL" in result["inducer"]
    assert result["strain_warning"] is not None
    assert "LuxR" in result["strain_warning"]
    print("  [PASS] test_classify_pLux_has_luxR_warning")


def test_classify_constitutive_promoter():
    result = classify_expression_mode("BBa_J23100")
    assert result["mode"] == "constitutive"
    assert result["inducer"] is None
    print("  [PASS] test_classify_constitutive_promoter")


def test_classify_friendly_alias_resolves():
    # Users (or the parser) might pass "pTet" instead of the canonical ID
    result = classify_expression_mode("pTet")
    assert result["mode"] == "inducible_small_molecule"
    assert result["promoter_id"] == "BBa_R0040"  # canonicalized
    print("  [PASS] test_classify_friendly_alias_resolves")


def test_classify_none_returns_unknown():
    result = classify_expression_mode(None)
    assert result["mode"] == "unknown"
    print("  [PASS] test_classify_none_returns_unknown")


def test_classify_unknown_promoter_is_graceful():
    result = classify_expression_mode("BBa_MADEUP")
    assert result["mode"] == "unknown"
    assert "not in the supported library" in result["notes"]
    print("  [PASS] test_classify_unknown_promoter_is_graceful")


# ==============================================================================
# 2. End-to-end classifier test against the teammates' sample file
# ==============================================================================

def test_end_to_end_classification_on_BBa_I0462():
    """Run the classifier on the actual sample the teammates uploaded."""
    assert PARTS_CSV.exists(), f"Fixture missing: {PARTS_CSV}"

    result = classify_from_parts_csv(str(PARTS_CSV))

    # The sample data is for BBa_I0462
    assert result["circuit_id"] == "BBa_I0462", (
        f"Expected circuit_id=BBa_I0462, got {result['circuit_id']}"
    )

    # The parts list should contain BBa_B0034, BBa_C0062, BBa_B0015
    part_ids = [p[0] for p in result["parts"]]
    assert "BBa_B0034" in part_ids, f"Missing BBa_B0034 in {part_ids}"
    assert "BBa_C0062" in part_ids, f"Missing BBa_C0062 in {part_ids}"
    assert "BBa_B0015" in part_ids, f"Missing BBa_B0015 in {part_ids}"

    # NOTE: The sample CSV has no row with type='promoter' (the scraper
    # didn't classify any of these as a promoter). So the expression mode
    # must gracefully be "unknown" -- NOT crash or guess.
    assert result["expression"]["mode"] == "unknown", (
        "Expected 'unknown' mode for a parts list with no promoter type, "
        f"got {result['expression']['mode']}"
    )

    # The sample has no reporter (BBa_B0034 is RBS, BBa_C0062 is LuxR,
    # BBa_B0015 is terminator -- none are GFP/RFP/YFP)
    assert result["reporter"] is None, (
        f"Expected no reporter in BBa_I0462 sample, got {result['reporter']}"
    )

    print("  [PASS] test_end_to_end_classification_on_BBa_I0462")


# ==============================================================================
# 3. Template rendering tests: each template should produce valid text
# ==============================================================================

def test_cloning_template_contains_key_elements():
    text = get_cloning_template(step_num=2, circuit_id="BBa_I0462")
    assert "Step 2" in text
    assert "BBa_I0462" in text
    assert "Golden Gate" in text or "ligation" in text.lower()
    # Must cite a source
    assert "Source" in text or "source" in text
    print("  [PASS] test_cloning_template_contains_key_elements")


def test_transformation_template_has_heat_shock():
    text = get_transformation_template(step_num=3)
    assert "Step 3" in text
    assert "42" in text  # heat shock temperature
    assert "30 seconds" in text  # heat shock time
    assert "SOC" in text
    print("  [PASS] test_transformation_template_has_heat_shock")


def test_transformation_template_with_strain_warning():
    text = get_transformation_template(
        step_num=3,
        strain_warning="Do not use arabinose-metabolizing strains."
    )
    assert "arabinose-metabolizing" in text
    print("  [PASS] test_transformation_template_with_strain_warning")


def test_colony_verification_contains_cycling():
    text = get_colony_verification_template(step_num=4, circuit_id="BBa_I0462")
    assert "Step 4" in text
    assert "BBa_I0462" in text
    assert "95 C" in text or "95C" in text
    assert "Taq" in text
    assert "agarose" in text.lower() or "gel" in text.lower()
    print("  [PASS] test_colony_verification_contains_cycling")


def test_fluorescence_check_no_reporter_branch():
    """Circuit has no reporter -> template should say so, not fake fluorescence."""
    expression = {"mode": "constitutive", "notes": ""}
    text = get_fluorescence_check_template(
        step_num=5,
        expression_decision=expression,
        reporter=None,
    )
    assert "No fluorescent reporter" in text
    assert "sequencing" in text.lower()
    # Must NOT claim there's a fluorescence signal
    assert "fluorescence visible" not in text.lower()
    print("  [PASS] test_fluorescence_check_no_reporter_branch")


def test_fluorescence_check_constitutive_branch():
    """Constitutive + reporter -> direct imaging, no induction step."""
    expression = {
        "mode": "constitutive",
        "friendly_name": "J23100",
        "promoter_id": "BBa_J23100",
        "inducer": None, "inducer_concentration": None,
        "induction_hours": None, "strain_warning": None,
        "notes": "constitutive"
    }
    reporter = {
        "part_id": "BBa_E0040",
        "friendly_name": "GFP",
        "reporter_type": "fluorescent_green",
        "excitation_nm": 488,
        "emission_nm": 507,
        "color": "green",
        "source_url": "http://parts.igem.org/Part:BBa_E0040",
    }
    text = get_fluorescence_check_template(5, expression, reporter)
    assert "constitutive" in text
    assert "488" in text
    assert "green" in text
    # The constitutive branch must NOT ask for a split-culture
    assert "Split the culture" not in text
    print("  [PASS] test_fluorescence_check_constitutive_branch")


def test_fluorescence_check_inducible_branch():
    """Inducible + reporter -> split-culture with named inducer."""
    expression = classify_expression_mode("BBa_I0500")  # pBAD
    reporter = {
        "part_id": "BBa_E0040",
        "friendly_name": "GFP",
        "reporter_type": "fluorescent_green",
        "excitation_nm": 488,
        "emission_nm": 507,
        "color": "green",
        "source_url": "http://parts.igem.org/Part:BBa_E0040",
    }
    text = get_fluorescence_check_template(5, expression, reporter)
    assert "L-arabinose" in text
    assert "0.2%" in text
    assert "Split the culture" in text
    # Strain warning should propagate into the fluorescence step too
    assert "arabinose" in text.lower()
    print("  [PASS] test_fluorescence_check_inducible_branch")


def test_fluorescence_check_unknown_promoter_branch():
    """Unknown promoter -> emits MANUAL REVIEW warning."""
    expression = classify_expression_mode("BBa_MADEUP")
    reporter = {
        "part_id": "BBa_E0040",
        "friendly_name": "GFP",
        "reporter_type": "fluorescent_green",
        "excitation_nm": 488,
        "emission_nm": 507,
        "color": "green",
        "source_url": "http://parts.igem.org/Part:BBa_E0040",
    }
    text = get_fluorescence_check_template(5, expression, reporter)
    assert "MANUAL REVIEW" in text
    assert "WARNING" in text
    print("  [PASS] test_fluorescence_check_unknown_promoter_branch")


# ==============================================================================
# 4. Full integration test: produce a complete protocol document
# ==============================================================================

def test_build_full_protocol_from_fixtures():
    """Run the whole pipeline end-to-end against the teammates' sample data
    and check the output has all the expected sections."""
    assert PARTS_CSV.exists()
    assert PCR_CSV.exists()

    text = build_full_protocol(
        parts_csv=str(PARTS_CSV),
        pcr_csv=str(PCR_CSV),
        pcr_protocol_text_path=None,  # sample.txt not in fixtures
        output_path=None,
    )

    # All five steps present
    assert "Step 1" in text, "Missing PCR step"
    assert "Step 2" in text, "Missing cloning step"
    assert "Step 3" in text, "Missing transformation step"
    assert "Step 4" in text, "Missing colony verification step"
    assert "Step 5" in text, "Missing fluorescence/functional step"

    # Circuit ID present
    assert "BBa_I0462" in text

    # PCR info from the CSV is included
    assert "aatgtttagcgtgggcatgc" in text  # forward primer
    assert "gcgttcaccgacaaacaaca" in text  # reverse primer

    # Parts from the parts CSV are listed
    assert "BBa_B0034" in text
    assert "BBa_C0062" in text
    assert "BBa_B0015" in text

    # Disclaimer present
    assert "Disclaimer" in text
    assert "NOT been validated experimentally" in text

    # Expression mode should be "unknown" for this input (no promoter row)
    assert "unknown" in text.lower()

    print("  [PASS] test_build_full_protocol_from_fixtures")


def test_build_full_protocol_writes_file(tmp_path=None):
    """Also verify the file-writing mode works."""
    if tmp_path is None:
        import tempfile
        tmp_path = Path(tempfile.mkdtemp())
    out_file = Path(tmp_path) / "full_protocol.md"
    build_full_protocol(
        parts_csv=str(PARTS_CSV),
        pcr_csv=str(PCR_CSV),
        output_path=str(out_file),
    )
    assert out_file.exists()
    content = out_file.read_text()
    assert "BBa_I0462" in content
    assert len(content) > 1000  # sanity: output is a real document, not empty
    print(f"  [PASS] test_build_full_protocol_writes_file ({len(content)} chars)")


# ==============================================================================
# Runner (so the file runs without pytest installed)
# ==============================================================================

def run_all():
    tests = [
        # classifier
        test_classify_pTet_by_biobrick_id,
        test_classify_pBAD_has_strain_warning,
        test_classify_pLux_has_luxR_warning,
        test_classify_constitutive_promoter,
        test_classify_friendly_alias_resolves,
        test_classify_none_returns_unknown,
        test_classify_unknown_promoter_is_graceful,
        # end-to-end on sample
        test_end_to_end_classification_on_BBa_I0462,
        # templates
        test_cloning_template_contains_key_elements,
        test_transformation_template_has_heat_shock,
        test_transformation_template_with_strain_warning,
        test_colony_verification_contains_cycling,
        test_fluorescence_check_no_reporter_branch,
        test_fluorescence_check_constitutive_branch,
        test_fluorescence_check_inducible_branch,
        test_fluorescence_check_unknown_promoter_branch,
        # integration
        test_build_full_protocol_from_fixtures,
        test_build_full_protocol_writes_file,
    ]
    print(f"Running {len(tests)} tests...\n")
    failed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"  [FAIL] {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            import traceback
            print(f"  [ERROR] {t.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print()
    if failed == 0:
        print(f"All {len(tests)} tests passed.")
    else:
        print(f"{failed} of {len(tests)} tests failed.")
    return failed


if __name__ == "__main__":
    sys.exit(run_all())
