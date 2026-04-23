# src/templates/colony_verification.py
#
# ==============================================================================
# COLONY VERIFICATION (COLONY PCR) TEMPLATE
# ==============================================================================
# After transformation, pick individual colonies and verify the correct
# insert is present by running PCR directly on a small portion of each
# colony. Values verified against published colony-PCR protocols.
#
# Style: raw f-string, matches structure.py's approach.
#
# Owner: [YOUR NAME]
# Last updated: 2026-04-21
# ==============================================================================


def get_colony_verification_template(step_num: int, circuit_id: str) -> str:
    """Return a protocol text for colony PCR verification.

    Args:
        step_num:    Step number in overall protocol.
        circuit_id:  The composite part's BioBrick ID (for labeling colonies).

    Returns:
        A multi-line string.
    """

    # VERIFIED: colony PCR cycling conditions below are representative of
    # standard Taq-based colony PCR, as published by multiple sources.
    # Source: Promega Colony PCR technical guide,
    #   "The extension time should be at least 1 minute/kilobase of
    #    target. Typically, anything smaller than 1kb uses a 1-minute
    #    extension."
    #   https://www.promega.com/-/media/files/resources/product-guides/subcloning-notebook/screening_recombinants_row.pdf
    # Also: Addgene Plasmids 101 on Colony PCR,
    #   "A standard Taq polymerase is sufficient."
    #   https://blog.addgene.org/plasmids-101-colony-pcr
    #
    # Annealing temperature 55 C is generic and depends on the specific
    # primer pair; noted in the template as a placeholder to adjust.

    return (
        f"## Step {step_num}: Colony PCR verification\n"
        f"\n"
        f"After overnight growth, pick single colonies and verify by\n"
        f"colony PCR that they contain the correct insert\n"
        f"(circuit {circuit_id}).\n"
        f"\n"
        f"### Procedure\n"
        f"\n"
        f"  1. Label 4-8 PCR tubes (one per colony to be screened),\n"
        f"     plus one tube as a no-template negative control.\n"
        f"  2. For each tube, prepare 20 uL of PCR master mix containing:\n"
        f"       - 1X Taq reaction buffer\n"
        f"       - 200 uM of each dNTP\n"
        f"       - 0.5 uM forward verification primer\n"
        f"       - 0.5 uM reverse verification primer\n"
        f"       - 1.25 U Taq DNA polymerase\n"
        f"     (Or use a commercial 2X Taq master mix per manufacturer's\n"
        f"      instructions -- this is easier for teaching labs.)\n"
        f"  3. With a sterile pipette tip, touch a well-separated colony.\n"
        f"     First streak a small patch onto a fresh labeled LB-antibiotic\n"
        f"     plate (your master plate), THEN swirl the same tip in the\n"
        f"     corresponding PCR tube to suspend cells.\n"
        f"  4. Cap tubes and run the following thermocycler program:\n"
        f"       - 95 C for 5 minutes (initial denaturation + cell lysis)\n"
        f"       - 30 cycles of:\n"
        f"           95 C for 30 seconds (denaturation)\n"
        f"           55 C for 30 seconds (annealing -- adjust for your primers)\n"
        f"           72 C for 1 minute per kb of expected product\n"
        f"       - 72 C for 5 minutes (final extension)\n"
        f"       - Hold at 4 C\n"
        f"  5. Run 5 uL of each reaction on a 1% agarose gel alongside a\n"
        f"     DNA ladder. A band at the expected size for {circuit_id}\n"
        f"     (its full sequence length plus any vector flanking region)\n"
        f"     indicates a successful clone.\n"
        f"  6. Note which colonies on the master plate gave positive bands;\n"
        f"     those are your verified clones for the next step.\n"
        f"\n"
        f"*Sources (standard colony-PCR protocol):*\n"
        f"*Promega subcloning notebook and Addgene Plasmids 101 (Colony PCR), accessed 2026-04-21.*\n"
        f"*URLs:*\n"
        f"*  https://blog.addgene.org/plasmids-101-colony-pcr*\n"
        f"*  https://www.promega.com/-/media/files/resources/product-guides/subcloning-notebook/screening_recombinants_row.pdf*\n"
    )
