# Archived response-geometry measurements

`CI_V2_RAW_RESPONSE_GEOMETRY.csv` is the primary table. The source was validated as exactly **1,024 unique cells**: 32 question IDs × 2 edit directions (`signed`, `rotated_90`) × 4 wording variants (`original`, `reworded`, `formal`, `terse`) × 4 instruction templates (`generic`, `math_only`, `format_only`, `math_format`). `question_id` is an opaque identifier, not the original question text.

Important columns:

- `attenuation`: a recorded functional-response statistic. **Not answer correctness.**
- `prompt_tokens`: observed input length, useful for diagnosing length confounds.
- `cosine`, `raw_logit_displacement`, `tangent_norm`: other archived response-geometry fields; not all are analyzed in this paper.

`ci_v2_wording_means.csv` is a derived summary. Recompute means from the raw table rather than treating the derived file as independent evidence.

Main SHA-256 for the raw CSV:

`303c7a42509d2480107591bfd3c5c3467f657233aa272fba546fa73a2d374f77`

The reanalysis script checks uniqueness, question count and factor coverage, and recomputes the paired bootstrap. It does **not** reproduce the model-side experiment. The original historical weight edit's complete training/selection provenance has not been independently reconstructed here.

