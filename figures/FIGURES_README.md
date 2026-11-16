# Figure captions, estimands, provenance and reuse

These plots accompany Harmain Dastgir's working research study, *One Frozen Edit, Four Ways to Ask: Prompt-Conditioned Functional Effects in a Transformer* (16 November 2026). The study has **not** been peer reviewed.

**Read the metric carefully.** The recorded outcome is a historical response-geometry metric called `attenuation`. These figures are **not** mathematical-answer accuracy, calibrated probabilities, causal-pathway evidence or results of new GPU inference. All values were recalculated from `../data/CI_V2_RAW_RESPONSE_GEOMETRY.csv`, whose SHA-256 is:

`303c7a42509d2480107591bfd3c5c3467f657233aa272fba546fa73a2d374f77`

The matrix has 1,024 complete factorial cells: 32 question identifiers × two directions (`signed`, `rotated_90`) × four wording variants (`original`, `reworded`, `formal`, `terse`) × four instruction templates (`generic`, `math_only`, `format_only`, `math_format`). Because each question appears in 32 cells, the **question**, not the cell, is the resampling unit.

## Four main-paper figures

### Figure 1 — Wording-conditioned signed-edit contrasts

Filename: `figure01_wording_mean_with_ci.png`.

For each question *q* and wording *v*, calculate `attenuation(q, signed, v, math_format) − attenuation(q, signed, v, generic)`, then average across the 32 questions. The mean contrasts, in wording order, are +0.205542, −0.020673, −0.045819 and −0.002337. Whiskers depict a separately seeded, 20,000-draw *question-resampling* percentile 95% interval for each wording mean. These are descriptive intervals conditional on the archived questions, the historical edit and the selected templates. They do not measure answer correctness or edit-transfer uncertainty.

### Figure 2 — Historical direction versus rotated control

Filename: `figure02_direction_control.png`.

Use the same within-question `math_format − generic` attenuation contrast but aggregate separately over signed versus 90°-rotated directions. Under original wording, signed = +0.205542 and rotated = −0.023924. The rotated direction is a **single archival control**, not a distribution of independent random controls; its response cannot establish a unique or causally identified neural circuit.

### Figure 3 — All 32 paired question contrasts

Filename: `figure03_question_level_paired_effects.png`.

Per question, subtract the signed/reworded contrast from the signed/original contrast. Every stored question has a positive difference (32/32); the mean is +0.226216, median +0.241814 and range +0.008832 to +0.712422. The figure sorts effect sizes from smallest to largest to display heterogeneity. **Q01–Q32 are rank labels, not the original archived question IDs.** To map a value to a source question ID use `QUESTION_LEVEL_CONTRASTS.csv`.

### Figure 4 — Complete instruction-by-wording response maps

Filename: `figure04_factorial_response_heatmaps.png`.

Each heatmap cell is the 32-question mean of the **raw attenuation** field for a specific direction, wording and instruction template. Both direction panels share a centered diverging color scale. This figure presents *absolute recorded attenuation averages*, unlike Figures 1–3, which show `math_format − generic` contrasts. It does **not** show accuracy or demonstrate independent replication among cells.

## Two supplemental diagnostic figures

### Figure S1 — Bootstrap variability of the paired mean

Filename: `figureS1_bootstrap_distribution.png`.

Sample 32 question identifiers with replacement for each of 20,000 draws using NumPy seed 20261116, and recompute the mean of the original-minus-reworded paired signed-edit contrasts. The 2.5th and 97.5th percentiles are +0.184256 and +0.274149, with the observed mean +0.226216. This is within-archive sampling variability, not a model- or edit-selection-adjusted confidence claim.

### Figure S2 — Prompt-token diagnostic and confound

Filename: `figureS2_prompt_token_diagnostics.png`.

The left panel shows archived mean recorded prompt tokens for each wording × instruction cell; the right shows the additional input tokens in `math_format` versus `generic`. These template differences are +14 tokens under original, +15 under reworded, +15 under formal and +14 under terse. Recorded counts were confirmed equal across edit directions for the same question/wording/template. The extra tokens and altered positions remain an important **unresolved confound** because this historical study did not use length- and position-matched controls.

## Recompute and audit

From the repository root:

```bash
python -m pip install -r requirements.txt
python reproduce_deposit.py
python make_study_figures.py
```

- `make_study_figures.py` requires an **exact SHA-256 match** to the frozen CSV and rejects duplicate, missing and non-finite cells. It verifies the 32 × 2 × 4 × 4 factorial matrix and the principal contrasts before plotting.
- `FIGURE_STATISTICS.json` lists the means, full heatmaps, resampling inputs, question distribution, token lengths and design boundaries.
- `QUESTION_LEVEL_CONTRASTS.csv` preserves all source question IDs with their three paired contrast columns.
- No notebook runtime, API key or model checkpoint is required. This reproduces the **numerical reanalysis and figures**, **not** the original edit-generation process or inference.

The author licenses the original figures and numerical data under **CC BY 4.0**. The accompanying Python source code is under MIT; see `../LICENSES.md`.
