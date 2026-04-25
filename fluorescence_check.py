# src/templates/fluorescence_check.py
#
# ==============================================================================
# FLUORESCENCE / FUNCTIONAL VERIFICATION TEMPLATE
# ==============================================================================
# The final step -- verify the circuit actually does what it was designed
# to do. This template has THREE branches, selected by the expression-mode
# classifier:
#
#   1. constitutive  -> image colonies directly on plate
#   2. inducible     -> split-culture induction + compare induced vs uninduced
#   3. no reporter   -> skip fluorescence, just say "verify by sequencing"
#
# Also has an "unknown" fallback when the promoter can't be classified.
#
# Style: raw f-string, matches structure.py's approach in teammates' code.
# NO Jinja2 dependency -- keeps the integration simple.
#
# Owner: [YOUR NAME]
# Last updated: 2026-04-21
# ==============================================================================


def get_fluorescence_check_template(
    step_num: int,
    expression_decision: dict,
    reporter: dict = None,
    antibiotic: str = "the selection antibiotic",
    antibiotic_concentration: str = "(see vector datasheet)",
) -> str:
    """Return a protocol text for functional / fluorescence verification.

    Args:
        step_num:             Step number in overall protocol.
        expression_decision:  Dict returned by classify_expression_mode().
                              Must contain 'mode' key.
        reporter:             Dict with reporter info (see KNOWN_REPORTERS in
                              expression_mode.py), or None if no reporter in
                              the circuit.
        antibiotic:           Selection antibiotic for the liquid culture.
        antibiotic_concentration: Concentration string.

    Returns:
        A multi-line string. Picks one of four branches based on inputs.
    """

    # --- Branch 1: No reporter in circuit -------------------------------------
    # If the circuit doesn't contain a fluorescent reporter (GFP/RFP/YFP),
    # we can't do a visual test. Tell the user to verify by sequencing
    # instead.
    if reporter is None:
        return (
            f"## Step {step_num}: Functional verification\n"
            f"\n"
            f"No fluorescent reporter (GFP, RFP, or YFP) was detected in\n"
            f"this circuit. A visual fluorescence check cannot be performed.\n"
            f"\n"
            f"Instead, verify the clones by:\n"
            f"  - Sanger sequencing of the insert region using standard\n"
            f"    vector primers (e.g. M13F/M13R or VF2/VR for pSB1C3).\n"
            f"  - Restriction-digest mapping if a diagnostic enzyme pair\n"
            f"    is available.\n"
            f"  - Any functional assay specific to the gene of interest\n"
            f"    (e.g. enzyme activity, growth phenotype, resistance test).\n"
            f"\n"
            f"*Note: This template was auto-generated. A qualified biologist\n"
            f"should design an appropriate functional assay for this circuit.*\n"
        )

    # --- Branch 2: Unknown expression mode (promoter not in library) ---------
    # The classifier couldn't figure out how to induce this circuit. Emit
    # a warning and punt the decision to the user. This prevents silent
    # incorrect output.
    mode = expression_decision.get("mode")
    if mode == "unknown":
        return (
            f"## Step {step_num}: Functional verification (MANUAL REVIEW REQUIRED)\n"
            f"\n"
            f"**WARNING:** The promoter in this circuit could not be\n"
            f"classified automatically. {expression_decision.get('notes', '')}\n"
            f"\n"
            f"A qualified biologist should determine the appropriate\n"
            f"induction conditions (if any) before running a fluorescence\n"
            f"check. Do not rely on the default protocol below without\n"
            f"review.\n"
            f"\n"
            f"Detected reporter: {reporter['friendly_name']} "
            f"(emission ~{reporter['emission_nm']} nm, {reporter['color']}).\n"
        )

    # --- Branch 3: Constitutive promoter -------------------------------------
    # Simple case: promoter is always on. Just grow the verified colonies
    # and look for the reporter signal directly.
    if mode == "constitutive":
        return (
            f"## Step {step_num}: Fluorescence verification "
            f"(constitutive expression)\n"
            f"\n"
            f"The promoter in this circuit is constitutive -- it is always\n"
            f"active. No induction step is required. Simply grow the\n"
            f"verified colonies and check for reporter expression.\n"
            f"\n"
            f"### Procedure\n"
            f"\n"
            f"  1. Pick 2-3 verified colonies from the master plate and\n"
            f"     streak each onto a fresh LB agar plate containing\n"
            f"     {antibiotic} at {antibiotic_concentration}.\n"
            f"  2. Incubate at 37 C for 16-18 hours.\n"
            f"  3. Examine colonies under a blue/UV transilluminator or\n"
            f"     a fluorescence imager using excitation at approximately\n"
            f"     {reporter['excitation_nm']} nm and emission filtering\n"
            f"     around {reporter['emission_nm']} nm.\n"
            f"\n"
            f"### Expected result\n"
            f"\n"
            f"  - Positive: visible {reporter['color']} fluorescence from\n"
            f"    the colonies, indicating correct assembly and expression\n"
            f"    of {reporter['friendly_name']}.\n"
            f"  - Negative: no fluorescence despite a correct colony-PCR\n"
            f"    band -- suggests a mutation in the CDS or an assembly\n"
            f"    error at the junction. Re-verify by sequencing.\n"
            f"\n"
            f"*Reporter data source: iGEM Parts Registry.*\n"
            f"*URL: {reporter.get('source_url', 'http://parts.igem.org')}*\n"
        )

    # --- Branch 4: Inducible (small-molecule) promoter -----------------------
    # The interesting case: split-culture induction experiment.
    # All the values below come from the expression_decision dict,
    # which itself was sourced from src/data/promoter_induction.py.
    if mode == "inducible_small_molecule":
        inducer = expression_decision["inducer"]
        inducer_conc = expression_decision["inducer_concentration"]
        hours = expression_decision["induction_hours"]
        promoter_name = expression_decision.get("friendly_name", "the promoter")
        strain_warning = expression_decision.get("strain_warning")

        warning_block = ""
        if strain_warning:
            warning_block = (
                f"\n"
                f"**Strain note:** {strain_warning}\n"
            )

        return (
            f"## Step {step_num}: Fluorescence verification "
            f"(inducible expression)\n"
            f"\n"
            f"The promoter in this circuit ({promoter_name}) is induced by\n"
            f"{inducer}. To verify correct function we run a split-culture\n"
            f"induction experiment comparing induced vs. uninduced samples.\n"
            f"{warning_block}\n"
            f"### Procedure\n"
            f"\n"
            f"  1. Pick a verified colony from the master plate and\n"
            f"     inoculate 5 mL of LB + {antibiotic} "
            f"({antibiotic_concentration}).\n"
            f"     Grow overnight at 37 C with shaking at 250 rpm.\n"
            f"  2. In the morning, dilute the overnight 1:100 into fresh\n"
            f"     LB + {antibiotic}. Grow at 37 C with shaking until\n"
            f"     OD600 reaches approximately 0.4 (mid-log phase).\n"
            f"  3. Split the culture equally into two sterile tubes:\n"
            f"       - Tube A (UNINDUCED): add an equal volume of sterile\n"
            f"         water as a vehicle control.\n"
            f"       - Tube B (INDUCED): add {inducer} to a final\n"
            f"         concentration of {inducer_conc}.\n"
            f"  4. Continue incubating both tubes at 37 C with shaking\n"
            f"     for {hours} hours.\n"
            f"  5. For each tube, pellet 1 mL of culture at 12,000 rpm\n"
            f"     for 1 minute. Resuspend each pellet in 100 uL of PBS.\n"
            f"  6. Image both samples under excitation at\n"
            f"     ~{reporter['excitation_nm']} nm, with emission filtering\n"
            f"     around {reporter['emission_nm']} nm, using a blue/UV\n"
            f"     transilluminator or a fluorescence plate reader.\n"
            f"\n"
            f"### Expected result\n"
            f"\n"
            f"  - Positive: Tube B (induced) shows strong {reporter['color']}\n"
            f"    fluorescence while Tube A (uninduced) shows little or none.\n"
            f"    This confirms both correct assembly of the reporter\n"
            f"    ({reporter['friendly_name']}) and functional response\n"
            f"    of the {promoter_name} promoter.\n"
            f"  - Negative: no difference between tubes -- suggests the\n"
            f"    circuit is either broken, always-on (loss of repression),\n"
            f"    or the host strain is incompatible with {inducer}.\n"
            f"    Re-verify by sequencing and consider the strain note\n"
            f"    above.\n"
            f"\n"
            f"*Inducer data source: {expression_decision.get('notes', '')}*\n"
            f"*Reporter data source: iGEM Parts Registry.*\n"
            f"*URL: {reporter.get('source_url', 'http://parts.igem.org')}*\n"
        )

    # --- Defensive fallback --------------------------------------------------
    # Should never be reached if expression_decision is well-formed.
    # Emit an unmistakable error block rather than silently returning nothing.
    return (
        f"## Step {step_num}: Functional verification (ERROR)\n"
        f"\n"
        f"**INTERNAL ERROR:** the expression classifier returned an\n"
        f"unrecognized mode '{mode}'. This is a bug in\n"
        f"src/classifier/expression_mode.py. Please report.\n"
    )
