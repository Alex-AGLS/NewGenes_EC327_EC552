# src/data/promoter_induction.py
#
# ==============================================================================
# PROMOTER INDUCTION DATA TABLE (keyed by BioBrick ID)
# ==============================================================================
# Maps each supported promoter's BioBrick ID to its induction requirements.
#
# Why BioBrick IDs? The teammates' parser (extract_xml.py) outputs parts by
# their "DisplayId" (e.g. "BBa_R0040"). So this classifier keys by the same
# ID to avoid name-translation headaches.
#
# CITATION POLICY:
# Every VERIFIED value has a source URL in its comment.
# Every UNVERIFIED value is flagged with [UNVERIFIED] and the reason.
# A teammate should resolve [UNVERIFIED] tags before the demo.
#
# Last updated: 2026-04-21
# Curator: [YOUR NAME HERE]
# ==============================================================================

CONSTITUTIVE = None


# Keyed by canonical BioBrick ID.
PROMOTER_INDUCTION = {

    # ==========================================================================
    # BBa_R0040 -- pTet promoter, aTc inducible
    # ==========================================================================
    "BBa_R0040": {
        "friendly_name": "pTet",
        "mode": "inducible_small_molecule",

        # VERIFIED: aTc is the preferred inducer. <50 ng/mL gives full induction.
        # Source: iGEM Part BBa_R0040 page, citing original publication,
        #   "concentrations of <50 ng/ml as required for the full induction"
        #   http://parts.igem.org/Part:BBa_R0040
        # Also: Applied Microbiology and Biotechnology 2021,
        #   "tunable by varying the anhydrotetracycline concentration
        #    from 10 to 200 ng/mL"
        #   https://link.springer.com/article/10.1007/s00253-021-11473-x
        "inducer": "anhydrotetracycline (aTc)",
        "inducer_concentration": "100 ng/mL",

        # [UNVERIFIED] 4 hours is a reasonable midpoint, but real protocols
        # range from 1 hour to overnight depending on goal. Confirm with
        # professor or teaching-lab SOP.
        "induction_hours": 4,

        "strain_warning": None,

        "source_url": "http://parts.igem.org/Part:BBa_R0040",
    },


    # ==========================================================================
    # BBa_I0500 / BBa_K206000 -- pBAD promoter, arabinose inducible
    # ==========================================================================
    "BBa_I0500": {
        "friendly_name": "pBAD (araC-pBAD)",
        "mode": "inducible_small_molecule",

        # VERIFIED: 0.2% L-arabinose is the canonical maximum-induction dose.
        # Source: Nature Communications 2023,
        #   "In E. coli, where the addition of 0.2% arabinose results
        #    in maximal induction of PBAD"
        #   https://www.nature.com/articles/s42003-023-05363-3
        "inducer": "L-arabinose",
        "inducer_concentration": "0.2% (w/v)",

        # [UNVERIFIED] See pTet note.
        "induction_hours": 4,

        # VERIFIED: strain must NOT metabolize arabinose.
        # Source: VectorBuilder pBAD documentation,
        #   "host strains that are mutant for L-arabinose catabolism
        #    (such as TOP10 or LMG194) should be used to avoid inconsistent
        #    expression due to depletion of L-arabinose"
        #   https://en.vectorbuilder.com/resources/vector-system/pBAD.html
        "strain_warning": (
            "Use a strain that cannot metabolize arabinose "
            "(e.g., TOP10 or LMG194). Wild-type strains deplete "
            "the inducer over time, causing inconsistent induction."
        ),

        "source_url": "http://parts.igem.org/Part:BBa_I0500",
    },


    # ==========================================================================
    # BBa_R0010 -- pLac promoter, IPTG inducible
    # ==========================================================================
    "BBa_R0010": {
        "friendly_name": "pLac",
        "mode": "inducible_small_molecule",

        # VERIFIED: 1 mM IPTG is the standard textbook induction concentration.
        # Source: NCBI PMC "Dynamics of transcription driven by the tetA
        #   promoter" (standard protocol):
        #   "IPTG (1 mM) was added in the medium"
        #   https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3458540/
        "inducer": "IPTG",
        "inducer_concentration": "1 mM",

        # [UNVERIFIED] See pTet note.
        "induction_hours": 4,

        # [UNVERIFIED] Some strains (JM109, DH5-alpha) contain lacIq for
        # tighter repression. Didn't add a warning because it's an
        # optimization, not a safety issue.
        "strain_warning": None,

        "source_url": "http://parts.igem.org/Part:BBa_R0010",
    },


    # ==========================================================================
    # BBa_R0062 -- pLux promoter, AHL inducible (quorum sensing)
    # ==========================================================================
    # Including this because BBa_I0462 (in the sample data) uses the pLux
    # quorum-sensing system.
    "BBa_R0062": {
        "friendly_name": "pLux (luxR-dependent)",
        "mode": "inducible_small_molecule",

        # [UNVERIFIED] AHL concentration is typical for lab demonstrations.
        # pLux requires co-expression of LuxR (usually via constitutive
        # promoter on the same plasmid). Teaching-lab standard is 10-100 nM.
        # Source (informal, iGEM context):
        #   http://parts.igem.org/Part:BBa_R0062
        # TODO: confirm with an authoritative primary source if available.
        "inducer": "3-oxohexanoyl-homoserine-lactone (3OC6-HSL / AHL)",
        "inducer_concentration": "100 nM",

        # [UNVERIFIED] See pTet note.
        "induction_hours": 4,

        # [UNVERIFIED] pLux requires LuxR protein to be present. If the
        # circuit doesn't include a LuxR-expressing part, induction will
        # fail. Flagging this so the template can warn the user.
        "strain_warning": (
            "pLux requires LuxR protein to be present. Verify the "
            "circuit includes a constitutively-expressed luxR "
            "(BBa_C0062) or equivalent, otherwise induction will fail."
        ),

        "source_url": "http://parts.igem.org/Part:BBa_R0062",
    },


    # ==========================================================================
    # Constitutive promoters -- no induction needed
    # ==========================================================================

    "BBa_J23100": {
        "friendly_name": "J23100 (strong constitutive)",
        "mode": "constitutive",
        "inducer": CONSTITUTIVE,
        "source_url": "http://parts.igem.org/Part:BBa_J23100",
    },

    "BBa_J23106": {
        "friendly_name": "J23106 (medium constitutive)",
        "mode": "constitutive",
        "inducer": CONSTITUTIVE,
        "source_url": "http://parts.igem.org/Part:BBa_J23106",
    },
}


# ==============================================================================
# Alias map for friendly names -> BioBrick IDs
# ==============================================================================
# Lets us accept "pTet" or "pBAD" as input even though the canonical
# key is BBa_R0040 / BBa_I0500.
PROMOTER_ALIASES = {
    # pTet
    "pTet":     "BBa_R0040",
    "pTET":     "BBa_R0040",
    "ptet":     "BBa_R0040",
    "pLtetO-1": "BBa_R0040",  # [UNVERIFIED] commonly conflated in teaching

    # pBAD
    "pBAD":    "BBa_I0500",
    "PBAD":    "BBa_I0500",
    "pbad":    "BBa_I0500",
    "ParaBAD": "BBa_I0500",

    # pLac
    "pLac": "BBa_R0010",
    "pLAC": "BBa_R0010",
    "plac": "BBa_R0010",

    # pLux
    "pLux":    "BBa_R0062",
    "pLUX":    "BBa_R0062",
    "pluxR":   "BBa_R0062",

    # Constitutive
    "J23100":  "BBa_J23100",
    "J23106":  "BBa_J23106",
    "pJ23100": "BBa_J23100",
    "pJ23106": "BBa_J23106",
}
