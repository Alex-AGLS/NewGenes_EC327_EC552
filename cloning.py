# src/templates/cloning.py
#
# ==============================================================================
# CLONING / LIGATION TEMPLATE
# ==============================================================================
# The PCR step (done by teammates) produces a LINEAR DNA fragment.
# To propagate it in E. coli it must be circularized -- usually by ligating
# it into a destination plasmid. This step is simplified for teaching:
# we assume the PCR primers included BsaI sites so a single Golden Gate
# reaction suffices, OR the user uses classical restriction/ligation.
#
# Style: raw f-string, matches structure.py's approach in the teammates' code.
#
# Owner: [YOUR NAME]
# Last updated: 2026-04-21
# ==============================================================================


def get_cloning_template(step_num: int, circuit_id: str) -> str:
    """Return a protocol text for cloning the PCR product into a vector.

    Args:
        step_num:    Integer step number in the overall protocol.
        circuit_id:  The composite part's BioBrick ID (e.g. "BBa_I0462").

    Returns:
        A multi-line string (plain text with Markdown-style headers).
    """

    # VERIFIED: Golden Gate reaction composition for single-insert cloning.
    # Source: NEB E1601 manual,
    #   "A 20 µl reaction containing T4 DNA Ligase Buffer (1X),
    #    75 ng pGGAselect (Golden Gate destination plasmid, CamR),
    #    75 ng each of 5 plasmids carrying fragments ...
    #    and 1 µl Golden Gate Enzyme Mix (BsaI-HFv2) containing T4 DNA
    #    Ligase and BsaI-HFv2 is incubated for 30 cycles of 37°C for
    #    1 minute, 16°C for 1 minute, then at 60°C for 5 minutes."
    #   https://www.neb.com/en/-/media/nebus/files/manuals/manuale1601.pdf
    #
    # NOTE: For a SINGLE insert (our case), NEB states cycling is not
    # strictly needed -- an isothermal 37 C incubation works. See
    # NEB FAQ at the URL above, "Can the Golden Gate Assembly reactions
    # be scaled down?"

    return (
        f"## Step {step_num}: Clone PCR product into a destination vector\n"
        f"\n"
        f"The PCR product from the previous step is linear DNA and cannot\n"
        f"propagate in E. coli on its own. Clone it into a circular\n"
        f"destination vector (e.g. pSB1C3 or pGGAselect).\n"
        f"\n"
        f"### Option A: Golden Gate Assembly (recommended if primers include BsaI sites)\n"
        f"\n"
        f"Combine on ice in a PCR tube (20 uL total reaction volume):\n"
        f"\n"
        f"  - 75 ng destination plasmid (e.g. pGGAselect)\n"
        f"  - 75 ng of the PCR-amplified {circuit_id} insert\n"
        f"  - 2 uL T4 DNA Ligase Buffer (10X) [1X final]\n"
        f"  - 1 uL NEBridge Golden Gate Enzyme Mix (BsaI-HFv2)\n"
        f"  - Nuclease-free water to 20 uL\n"
        f"\n"
        f"Thermocycler program (single-insert cloning):\n"
        f"  - 37 C for 60 minutes (isothermal digestion + ligation)\n"
        f"  - 60 C for 5 minutes (enzyme inactivation)\n"
        f"  - Hold at 4 C\n"
        f"\n"
        f"### Option B: Classical restriction / ligation (BioBrick-standard)\n"
        f"\n"
        f"If the PCR primers included BioBrick prefix/suffix sites\n"
        f"(EcoRI, XbaI, SpeI, PstI), digest the insert and the destination\n"
        f"vector with the appropriate enzyme pair, then ligate using\n"
        f"T4 DNA Ligase at 16 C for 30 minutes or overnight.\n"
        f"\n"
        f"*Source: NEB E1601 Golden Gate Assembly Protocol, accessed 2026-04-21.*\n"
        f"*URL: https://www.neb.com/en/-/media/nebus/files/manuals/manuale1601.pdf*\n"
    )
