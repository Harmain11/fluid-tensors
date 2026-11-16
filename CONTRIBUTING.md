# Contributing to Fluid Tensors

We welcome independent checks, negative results, alternative explanations, methodological critiques, and new experiments. This is a working preprint, not a peer-reviewed demonstration of model repair.

## Start here

- Read the [paper and limitations](README.md) and [independent replication challenge](docs/REPLICATION_CHALLENGE.md).
- Download the frozen evidence and original-run provenance supplement from [Zenodo Version 2](https://doi.org/10.5281/zenodo.24284827) or the [GitHub v1.1.0 release](https://github.com/Harmain11/fluid-tensors/releases/tag/v1.1.0).
- Run the CPU-only reanalysis from a fresh clone with these commands in order: python -m pip install -r requirements.txt; python reproduce_deposit.py; python make_study_figures.py.
- Open an Issue for reproducibility problems or a Discussion for new protocols. Pull requests should explain their hypothesis, exact commands, datasets, and changes.

## Three different evidence levels

1. **A — Archive replay (CPU):** verify checksums, complete table coverage, recalculated statistics, and regenerated plots from stored measurements. No model inference is involved.
2. **B — Independent model-side replication:** reconstruct the model, weight intervention, inference, and scoring pipeline independently; this has not yet been confirmed by an outside researcher.
3. **C — Prospective controls:** prespecified held-out tasks, length- and position-matched prompts, random/rotated/sham edit baselines, independent edit selection, other models, and blinded final-answer accuracy.

## How to report a result

Include OS, hardware, Python and dependency versions, exact model/tokenizer revisions, checkpoints and hashes, seeds, prompts/templates, commands or notebook commit, intervention-selection rules, scoring definitions, raw question-level results, controls, effect sizes, and uncertainty. State **reproduced**, **partly reproduced**, **diverged**, or **blocked** with specific details. Share negative results too.

Do not overwrite the frozen 1,024-cell source archive, interpret attenuation as mathematical answer accuracy, or claim that unmatched prompt conditions establish semantic causality. Keep historical and new experimental results separated. Do not commit private information, secrets, or third-party data/weights without redistribution rights. Discuss major methodological changes before a pull request; provide tests where possible. Authorship is based on substantive scientific contributions and is not guaranteed by participating.

Contact: Harmain Dastgir, Independent Researcher — harmainmughal215@gmail.com.
