# src/templates/transformation.py
#
# ==============================================================================
# TRANSFORMATION TEMPLATE
# ==============================================================================
# Heat-shock transformation of the ligated plasmid into chemically competent
# E. coli. Values verified against NEB's official protocol page for
# C2987 / C2988 (NEB 5-alpha Competent E. coli).
#
# Style: raw f-string, matches structure.py's approach.
#
# Owner: [YOUR NAME]
# Last updated: 2026-04-21
# ==============================================================================


def get_transformation_template(
    step_num: int,
    strain_warning: str = None,
    antibiotic: str = "the selection antibiotic",
    antibiotic_concentration: str = "(see vector datasheet)",
) -> str:
    """Return a protocol text for transformation into E. coli.

    Args:
        step_num:                 Step number in overall protocol.
        strain_warning:           Optional warning (e.g. pBAD strain restrictions).
                                  If None, no warning line is emitted.
        antibiotic:               Name of the selection antibiotic.
                                  Defaults to a generic placeholder because
                                  this depends on the destination vector,
                                  which isn't in the current SBOL pipeline.
        antibiotic_concentration: Concentration, e.g. "25 ug/mL".

    Returns:
        A multi-line string.
    """

    # VERIFIED: exact values below are from NEB's official high-efficiency
    # transformation protocol for C2987 (NEB 5-alpha Competent E. coli).
    # Source: NEB,
    #   "Thaw a tube of NEB 5-alpha Competent E. coli cells on ice for 10
    #    minutes ... Add 1-5 µl containing 100 pg-1 µg of plasmid DNA to
    #    the cell mixture. Carefully flick the tube 4-5 times to mix
    #    cells and DNA. Do not vortex. Place the mixture on ice for 30
    #    minutes. Do not mix. Heat shock at exactly 42°C for exactly
    #    30 seconds. Do not mix. Place on ice for 5 minutes. Do not mix.
    #    Pipette 950 µl of room temperature SOC into the mixture.
    #    Place at 37°C for 60 minutes. Shake vigorously (250 rpm) or rotate."
    #   https://www.neb.com/en-us/protocols/high-efficiency-transformation-protocol-c2987

    warning_block = ""
    if strain_warning:
        warning_block = (
            f"\n"
            f"**Strain note:** {strain_warning}\n"
        )

    return (
        f"## Step {step_num}: Transformation into E. coli\n"
        f"\n"
        f"Introduce the circularized plasmid from the previous step into\n"
        f"chemically competent E. coli cells via heat-shock transformation.\n"
        f"{warning_block}\n"
        f"### Procedure\n"
        f"\n"
        f"  1. Thaw a 50 uL aliquot of NEB 5-alpha Competent E. coli\n"
        f"     (or equivalent) on ice for about 10 minutes.\n"
        f"  2. Add 1-5 uL of the ligation / assembly reaction\n"
        f"     (containing 100 pg to 1 ug of DNA) to the cells.\n"
        f"     Mix by flicking the tube 4-5 times. DO NOT VORTEX.\n"
        f"  3. Incubate on ice for exactly 30 minutes. Do not mix.\n"
        f"  4. Heat-shock at exactly 42 C for exactly 30 seconds. Do not mix.\n"
        f"  5. Return the tube to ice for 5 minutes. Do not mix.\n"
        f"  6. Add 950 uL of room-temperature SOC outgrowth medium.\n"
        f"  7. Incubate at 37 C for 60 minutes with shaking at 250 rpm.\n"
        f"  8. Spread 50-100 uL onto an LB agar plate containing\n"
        f"     {antibiotic} at {antibiotic_concentration}.\n"
        f"     Plate the remainder as backup if needed.\n"
        f"  9. Incubate plates inverted at 37 C overnight (16-18 hours).\n"
        f"\n"
        f"*Source: NEB High Efficiency Transformation Protocol (C2987),*\n"
        f"*accessed 2026-04-21.*\n"
        f"*URL: https://www.neb.com/en-us/protocols/high-efficiency-transformation-protocol-c2987*\n"
    )
