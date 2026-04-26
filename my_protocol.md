# Lab Protocol: BBa_I0462

**Generated:** 2026-04-22  
**Assembly method:** single-insert cloning (after PCR amplification)  
**Detected promoter:** (promoter not detected)  
**Detected reporter:** (no fluorescent reporter detected)  
**Expression mode:** unknown  

---

## Parts list

| # | BioBrick ID | Type |
|---|-------------|------|
| 1 | BBa_B0034 | ribosome binding site |
| 2 | BBa_C0062 | (unknown) |
| 3 | BBa_B0015 | terminator |

## Step 1: PCR amplification (generated upstream)

PCR amplify the composite part BBa_I0462 using the following primers
and thermocycler settings (computed by primer3 in the upstream step):

  - Forward primer: aatgtttagcgtgggcatgc
  - Reverse primer: gcgttcaccgacaaacaaca
  - Annealing / melting temperature: 81.31 C
  - Extension time: 56.16 seconds

For the full reaction mix and cycling program, use NEB's Q5
High-Fidelity DNA Polymerase protocol (M0491) as the reference.

*Source: upstream PCR design step (request_primer.py + structure.py).*

## Step 2: Clone PCR product into a destination vector

The PCR product from the previous step is linear DNA and cannot
propagate in E. coli on its own. Clone it into a circular
destination vector (e.g. pSB1C3 or pGGAselect).

### Option A: Golden Gate Assembly (recommended if primers include BsaI sites)

Combine on ice in a PCR tube (20 uL total reaction volume):

  - 75 ng destination plasmid (e.g. pGGAselect)
  - 75 ng of the PCR-amplified BBa_I0462 insert
  - 2 uL T4 DNA Ligase Buffer (10X) [1X final]
  - 1 uL NEBridge Golden Gate Enzyme Mix (BsaI-HFv2)
  - Nuclease-free water to 20 uL

Thermocycler program (single-insert cloning):
  - 37 C for 60 minutes (isothermal digestion + ligation)
  - 60 C for 5 minutes (enzyme inactivation)
  - Hold at 4 C

### Option B: Classical restriction / ligation (BioBrick-standard)

If the PCR primers included BioBrick prefix/suffix sites
(EcoRI, XbaI, SpeI, PstI), digest the insert and the destination
vector with the appropriate enzyme pair, then ligate using
T4 DNA Ligase at 16 C for 30 minutes or overnight.

*Source: NEB E1601 Golden Gate Assembly Protocol, accessed 2026-04-21.*
*URL: https://www.neb.com/en/-/media/nebus/files/manuals/manuale1601.pdf*

## Step 3: Transformation into E. coli

Introduce the circularized plasmid from the previous step into
chemically competent E. coli cells via heat-shock transformation.

### Procedure

  1. Thaw a 50 uL aliquot of NEB 5-alpha Competent E. coli
     (or equivalent) on ice for about 10 minutes.
  2. Add 1-5 uL of the ligation / assembly reaction
     (containing 100 pg to 1 ug of DNA) to the cells.
     Mix by flicking the tube 4-5 times. DO NOT VORTEX.
  3. Incubate on ice for exactly 30 minutes. Do not mix.
  4. Heat-shock at exactly 42 C for exactly 30 seconds. Do not mix.
  5. Return the tube to ice for 5 minutes. Do not mix.
  6. Add 950 uL of room-temperature SOC outgrowth medium.
  7. Incubate at 37 C for 60 minutes with shaking at 250 rpm.
  8. Spread 50-100 uL onto an LB agar plate containing
     the selection antibiotic at (see vector datasheet).
     Plate the remainder as backup if needed.
  9. Incubate plates inverted at 37 C overnight (16-18 hours).

*Source: NEB High Efficiency Transformation Protocol (C2987),*
*accessed 2026-04-21.*
*URL: https://www.neb.com/en-us/protocols/high-efficiency-transformation-protocol-c2987*

## Step 4: Colony PCR verification

After overnight growth, pick single colonies and verify by
colony PCR that they contain the correct insert
(circuit BBa_I0462).

### Procedure

  1. Label 4-8 PCR tubes (one per colony to be screened),
     plus one tube as a no-template negative control.
  2. For each tube, prepare 20 uL of PCR master mix containing:
       - 1X Taq reaction buffer
       - 200 uM of each dNTP
       - 0.5 uM forward verification primer
       - 0.5 uM reverse verification primer
       - 1.25 U Taq DNA polymerase
     (Or use a commercial 2X Taq master mix per manufacturer's
      instructions -- this is easier for teaching labs.)
  3. With a sterile pipette tip, touch a well-separated colony.
     First streak a small patch onto a fresh labeled LB-antibiotic
     plate (your master plate), THEN swirl the same tip in the
     corresponding PCR tube to suspend cells.
  4. Cap tubes and run the following thermocycler program:
       - 95 C for 5 minutes (initial denaturation + cell lysis)
       - 30 cycles of:
           95 C for 30 seconds (denaturation)
           55 C for 30 seconds (annealing -- adjust for your primers)
           72 C for 1 minute per kb of expected product
       - 72 C for 5 minutes (final extension)
       - Hold at 4 C
  5. Run 5 uL of each reaction on a 1% agarose gel alongside a
     DNA ladder. A band at the expected size for BBa_I0462
     (its full sequence length plus any vector flanking region)
     indicates a successful clone.
  6. Note which colonies on the master plate gave positive bands;
     those are your verified clones for the next step.

*Sources (standard colony-PCR protocol):*
*Promega subcloning notebook and Addgene Plasmids 101 (Colony PCR), accessed 2026-04-21.*
*URLs:*
*  https://blog.addgene.org/plasmids-101-colony-pcr*
*  https://www.promega.com/-/media/files/resources/product-guides/subcloning-notebook/screening_recombinants_row.pdf*

## Step 5: Functional verification

No fluorescent reporter (GFP, RFP, or YFP) was detected in
this circuit. A visual fluorescence check cannot be performed.

Instead, verify the clones by:
  - Sanger sequencing of the insert region using standard
    vector primers (e.g. M13F/M13R or VF2/VR for pSB1C3).
  - Restriction-digest mapping if a diagnostic enzyme pair
    is available.
  - Any functional assay specific to the gene of interest
    (e.g. enzyme activity, growth phenotype, resistance test).

*Note: This template was auto-generated. A qualified biologist
should design an appropriate functional assay for this circuit.*


---

## Disclaimer

This protocol was auto-generated from an SBOL structural
description using deterministic templates based on published
laboratory protocols. It has NOT been validated experimentally.
Before attempting in a real laboratory:

  - A qualified biologist must review all steps for correctness
    in the specific experimental context.
  - Parts are assumed available as purified DNA in a local
    part library.
  - PCR primer sequences were computed algorithmically and are
    not guaranteed to be optimal.
  - All safety procedures of the host institution take
    precedence.

Template sources are cited inline and in the References section
of the source code.
