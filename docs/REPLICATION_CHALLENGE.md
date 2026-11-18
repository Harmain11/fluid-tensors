# Independent replication challenge

## One frozen edit. Four ways to ask. Can the result survive independent scrutiny?

The historical study measures **functional attenuation**, not final-answer correctness. It reports **1,024 archived observations** in one Qwen2.5-1.5B context: 32 questions × two edit directions × four wordings × four instruction templates. For the historically selected signed direction, the math-plus-format minus generic attenuation contrast averaged **+0.205542** for original wording and **−0.020673** for reworded prompts. The 32-question paired original-minus-reworded difference was **+0.226216**, with a descriptive 95% question-bootstrap interval **[+0.184256, +0.274149]** (20,000 resamples). Under original wording, the historical 90-degree rotated direction gave **−0.023924**.

**Limitations:** The edit was historically selected; wording, token length, and positions changed together; uncertainty is conditional on that selection; only one model/edit context is covered. The original archived paper did not independently recreate the model-side run; a separate November 18 same-model GPU confirmation now exists, but independent external-model or external-lab replication remains open. The reported data do not demonstrate improved mathematical reasoning accuracy, general model repair, or an isolated causal circuit.

## Update: November 18, 2026 — within-model confirmation completed

A distinct GPU run has now repeated the original 32-question decisive contrast (128/128 measurements matched in the recorded environment) and tested 64 further GSM8K-train question identities under raw and explicitly token-count-matched inputs, with a norm-matched orthogonal control. Its matched signed direction mean contrast was **+0.193491** (95% question-bootstrap interval **[+0.166896, +0.219002]**, positive **62/64**); the matched orthogonal control mean was **+0.004060** (interval crossed zero). All **1,152** recorded cells passed numerical checks. The [full supplemental package](https://github.com/Harmain11/fluid-tensors/tree/main/paper1-confirmation-2026-11-18) contains the dated PDF, raw GPU ZIP, verifier, figures and limitations.

This closes the planned **same-model, new-question** confirmation. It does **not** close independent model-family, independent-laboratory, unseen-pretraining-data, or math-answer accuracy replication. The 64 identities are from GSM8K train, and the input matching uses explicit newline-token IDs that can change formatting. Those are legitimate directions for future replication.

### Level A — Independent archive replay (CPU, no GPU)

Clone the repository, install requirements, run reproduce_deposit.py and make_study_figures.py. Validate source hashes and full factorial coverage; recompute question-level differences, four wording means, the 20,000-resample uncertainty interval and all six figures. If anything differs, report numerical deltas and environment details. Passing Level A checks only the *preserved numbers*, not the underlying causal intervention.

### Level B — Model-side rerun

Using the [versioned provenance supplement](https://github.com/Harmain11/fluid-tensors/releases/tag/v1.1.0), attempt to reconstruct the exact base model/tokenizer revision, signed weight edit, 90-degree rotated direction, prompts, inference settings and scoring. State the model revision, GPU/precision, seeds, checkpoints/adapter hashes and any inaccessible or ambiguous steps. A blocked, partial, or negative attempt is a useful research outcome.

### Level C — Prospective falsification

Freeze a new task set and independent edit-selection rule before evaluation. Compare length- and position-matched paraphrases, no-edit/sham edit and multiple random/rotated controls. Include independent models and seeds. Measure raw attenuation and blinded final-answer correctness as **distinct outcomes**, with appropriate paired uncertainty and all negative results.

### Where to share results

Use the [replication report template](https://github.com/Harmain11/fluid-tensors/issues/new/choose), [GitHub Discussions](https://github.com/Harmain11/fluid-tensors/discussions), or a pull request containing a reproducible report. Specify A/B/C and link raw data and scripts when licensing permits. We explicitly welcome criticism and unsuccessful replications.

Sources: [Zenodo Version 2 and full supplement](https://doi.org/10.5281/zenodo.24284827) · [GitHub v1.1.0 provenance release](https://github.com/Harmain11/fluid-tensors/releases/tag/v1.1.0) · [paper](https://harmain11.github.io/fluid-tensors/papers/one-frozen-edit.html). Working preprint, not peer reviewed.
