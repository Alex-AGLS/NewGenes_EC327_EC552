# This part: Post-PCR protocol templates + expression-mode classifier

Part of the **SBOL -> Lab Protocol Generator**.

## What this handles

Templates-&-Output-Instructions branch code produces:
- `individualParts_sampleOutput.csv` — the parts table (from `structure.get_table`)
- `pcr_SampleOutput.csv` — PCR primer/temp/time summary (from `structure.get_pcr_info`)
- `sample.txt` — the PCR protocol text (optional)

This code takes those outputs and adds **four more protocol steps** on top,
producing one combined lab protocol document:

| Step | What it is | Where |
|------|------------|-------|
| 1 | PCR amplification | (already done by teammates) |
| 2 | Clone PCR product into a vector | `src/templates/cloning.py` |
| 3 | Transformation into E. coli | `src/templates/transformation.py` |
| 4 | Colony PCR verification | `src/templates/colony_verification.py` |
| 5 | Functional / fluorescence check | `src/templates/fluorescence_check.py` |

Step 5 is the interesting one — it **branches** based on the promoter in
the circuit:
- **Constitutive promoter** (e.g. J23100) → image colonies directly
- **Inducible promoter** (e.g. pTet, pBAD, pLac, pLux) → split-culture
  induction experiment with the right chemical, concentration, and warnings
- **No reporter present** → skip fluorescence, suggest sequencing instead
- **Unknown promoter** → emit a "manual review required" warning (no guessing)

The branching logic is in `src/classifier/expression_mode.py`, driven by
`src/data/promoter_induction.py` (a hand-curated, cited lookup table).

## Folder layout

```
my_part/
├── src/
│   ├── data/
│   │   └── promoter_induction.py       <- Induction data (keyed by BioBrick ID)
│   ├── classifier/
│   │   └── expression_mode.py          <- Reads parts CSV, picks induction mode
│   ├── templates/
│   │   ├── cloning.py                  <- Step 2
│   │   ├── transformation.py           <- Step 3
│   │   ├── colony_verification.py      <- Step 4
│   │   └── fluorescence_check.py       <- Step 5 (branches on mode)
│   └── protocol_builder.py             <- Reads everything, writes final doc
├── tests/
│   ├── fixtures/
│   │   ├── individualParts_sampleOutput.csv   (from teammates' actual run)
│   │   └── pcr_SampleOutput.csv               (from teammates' actual run)
│   └── test_with_sample_data.py        <- 18 tests, all pass
└── README.md
```

No external dependencies. Python 3.8+. Same style as the teammates' code
(plain text, raw f-strings, CSV as intermediate format -- no Jinja2).

## How to run

From the `my_part/` folder:

### Option 1 — Run all tests
```bash
python -m tests.test_with_sample_data
```
Expected output: `All 18 tests passed.`

### Option 2 — Generate a protocol from the sample files (CLI)
```bash
python -m src.protocol_builder \
    --parts tests/fixtures/individualParts_sampleOutput.csv \
    --pcr   tests/fixtures/pcr_SampleOutput.csv \
    --out   full_protocol.md
```
Expected output:
```
[ok] Wrote full protocol to full_protocol.md (~6600 characters).
```
Then open `full_protocol.md` in a Markdown viewer (or just `cat` it) and
inspect the 5 protocol steps.

### Option 3 — Use from Python (for integrating with teammates' `structure.py`)
```python
from src.protocol_builder import build_full_protocol

build_full_protocol(
    parts_csv="individualParts_sampleOutput.csv",
    pcr_csv="pcr_SampleOutput.csv",
    pcr_protocol_text_path="sample.txt",    # optional
    output_path="full_protocol.md",
)
```

## Integration with the teammates' code

Their `structure.py` already has a `__main__` block that calls
`get_table(...)` and `get_pcr_info(...)`. To integrate our part, they just
need to add one line at the end:

```python
if __name__ == '__main__':
    get_table("BBa_I0462.xml", "parts_table.csv")
    get_pcr_info("data.json", "sample.txt", "summary.csv")

    # --- new line: build the full protocol ---
    from src.protocol_builder import build_full_protocol
    build_full_protocol(
        parts_csv="parts_table.csv",
        pcr_csv="summary.csv",
        pcr_protocol_text_path="sample.txt",
        output_path="full_protocol.md",
    )
```

(Filenames assume they're in the same directory as the `src/` folder. If
not, adjust `sys.path` or use full paths.)

## How to test if it works

**Quick smoke test** — just run:
```bash
python -m tests.test_with_sample_data
```
This runs all 18 tests including an end-to-end integration test against
the actual `BBa_I0462` sample the teammates uploaded. If any test fails,
the error message will point at which template or classifier branch
needs attention.

**Visual test** — generate an actual protocol document:
```bash
python -m src.protocol_builder \
    --parts tests/fixtures/individualParts_sampleOutput.csv \
    --pcr   tests/fixtures/pcr_SampleOutput.csv \
    --out   full_protocol.md
cat full_protocol.md
```

**What you should see in the output:**
- A header with circuit ID `BBa_I0462`, mode `unknown` (because the scraper
  in the sample didn't flag any part as type=promoter — this is the
  graceful-failure case)
- A parts table with `BBa_B0034`, `BBa_C0062`, `BBa_B0015`
- Step 1 (PCR) with the actual primers from the CSV
  (`aatgtttagcgtgggcatgc` / `gcgttcaccgacaaacaaca`) and Tm `81.31 C`
- Steps 2, 3, 4 with the templated protocols (cloning, transformation,
  colony verification) — all values NEB-sourced and cited
- Step 5 says "MANUAL REVIEW REQUIRED" because the promoter is unknown —
  this is correct behavior, not a bug

**To test the interesting (inducible) branch**, try a modified fixture
with a known promoter. For example, create a test fixture where the
`type` column is `promoter` for a row with `BBa_R0040`:
```
Component,test_inducible_gfp
name,type,information
BBa_R0040,promoter,
BBa_B0034,ribosome binding site,
BBa_E0040,coding sequence,
BBa_B0015,terminator,
```
Run the CLI on it, and Step 5 will give you a split-culture aTc induction
protocol with strain notes.

## What needs manual review before the demo

Three `[UNVERIFIED]` items are flagged inline in the code:

1. **`induction_hours: 4`** for pTet, pBAD, pLac, pLux. A reasonable
   midpoint, but real protocols range from 1 hour to overnight.
   Confirm with the professor or the teaching-lab SOP.
2. **`pLtetO-1` aliased to `BBa_R0040` (pTet)**. Commonly treated as
   equivalent in teaching materials, but technically pLtetO-1 is a
   specific engineered variant.
3. **pLux induction concentration (100 nM AHL)**. Based on typical
   teaching-lab usage; if the professor has a specific reference they
   want used, update `promoter_induction.py` accordingly.

Everything else has VERIFIED citations to NEB protocols, the iGEM
Parts Registry, or published papers. Check any value with its `# Source:`
comment in the code.

## Output contract (for templates consuming classifier output)

`classify_from_parts_csv(csv_path)` returns:

```python
{
    "circuit_id": "BBa_I0462",          # top-level composite ID
    "expression": {
        "mode": "inducible_small_molecule" | "constitutive" | "unknown",
        "promoter_id": "BBa_R0040",
        "friendly_name": "pTet",
        "inducer": "anhydrotetracycline (aTc)",
        "inducer_concentration": "100 ng/mL",
        "induction_hours": 4,
        "strain_warning": None,
        "notes": "pTet (BBa_R0040) is induced by ..."
    },
    "reporter": {                       # None if no reporter detected
        "part_id": "BBa_E0040",
        "friendly_name": "GFP",
        "reporter_type": "fluorescent_green",
        "excitation_nm": 488,
        "emission_nm": 507,
        "color": "green",
        "source_url": "http://parts.igem.org/Part:BBa_E0040"
    },
    "parts": [                          # raw list of (id, type) tuples
        ("BBa_B0034", "ribosome binding site"),
        ("BBa_C0062", ""),
        ("BBa_B0015", "terminator"),
    ]
}
```

## Sources (also cited inline in code)

- **NEB E1601 Golden Gate Assembly Kit manual** — cloning step values  
  https://www.neb.com/en/-/media/nebus/files/manuals/manuale1601.pdf
- **NEB C2987 High Efficiency Transformation Protocol** — transformation
  values  
  https://www.neb.com/en-us/protocols/high-efficiency-transformation-protocol-c2987
- **Addgene Plasmids 101: Colony PCR** — colony verification values  
  https://blog.addgene.org/plasmids-101-colony-pcr
- **Promega subcloning notebook** — colony PCR cycling conditions  
  https://www.promega.com/-/media/files/resources/product-guides/subcloning-notebook/screening_recombinants_row.pdf
- **iGEM Parts Registry** — promoter/reporter BioBrick IDs, e.g. BBa_R0040  
  http://parts.igem.org/Part:BBa_R0040
- **Nature Communications 2023** — pBAD 0.2% L-arabinose induction  
  https://www.nature.com/articles/s42003-023-05363-3
- **NCBI PMC 3458540** — pLac 1 mM IPTG standard  
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3458540/
- **VectorBuilder pBAD documentation** — strain warning for pBAD  
  https://en.vectorbuilder.com/resources/vector-system/pBAD.html
- **Applied Microbiology and Biotechnology 2021** — pTet aTc range  
  https://link.springer.com/article/10.1007/s00253-021-11473-x
