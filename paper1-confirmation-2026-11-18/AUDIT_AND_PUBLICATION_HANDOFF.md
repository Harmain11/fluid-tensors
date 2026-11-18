# Paper 1 — Final Confirmation Audit and Publication Handoff

**Prepared for:** Harmain Dastgir, Independent Researcher  
**Date:** November 18, 2026  
**Proposed project status:** Experimental confirmation complete; archival publication update pending user review.

## A. What was independently checked

The user-supplied `FT_P1_CONFIRMATION_2026_11_18_ALL_RESULTS.zip` was inspected without modifying any original data.

1. The included SHA-256 manifest verified every archived file; no missing or duplicate ZIP members were accepted.
2. The embedded offline verifier was run against the ZIP and returned a valid manifest, 1,152 rows, matching archive replay, passing numerical gate, and the same primary statistic as the displayed study summary.
3. A second independent, direct read of all response JSONL rows reconstructed question-level contrasts from the four cells per question.
4. The 32-question original replay encompassed 128 exact matched measurements, **not** all 1,024 cells of the earlier full-factorial original research.
5. No overlap was found between the 64 new-question hashes and the 2,975 frozen excluded historical hashes or the original archived heldout hashes.
6. The source token diagnostics showed exactly equal model-input token counts within all four prompt conditions for every new question; 0–16 explicit newline token IDs were inserted per condition.
7. The direction geometry was validated (norm ratio 1.0; inter-direction cosine approximately zero).
8. All 1,152 recorded finite-difference and target-layer numerical quality flags were empty.

## B. Evidence ledger

| Evidence | Measurement | Disposition |
|---|---|---|
| Recorded full cells | 1,152/1,152 | Pass |
| Replay comparison | 128/128 values identical, max error 0 | Pass for same runtime |
| Frozen base-weight hash | `56c3c552a24bfae10426abad4e538cf81497b59ea97d277e70c404d0801441e5` | Match |
| Matched signed contrast | 0.193491 [0.166896, 0.219002] | Pass main criterion |
| Matched orthogonal contrast | 0.004060 [−0.004614, 0.012629] | Near-null direction control |
| Signed-minus-orthogonal contrast | 0.189431 [0.162041, 0.216506] | Positive secondary difference |
| Matched-minus-raw signed contrast | −0.035755 [−0.048599, −0.023462] | Formatting matters; report it |
| Positive matched pairs | 62/64 | Consistent direction across sample |
| Numerical failures | 0 | Pass |
| ZIP SHA-256 manifest | All 26 files matched | Pass |
| New data split | GSM8K train | Disclose potential pretraining exposure |
| New cohort overlap with archive | 0 hashes | Pass within archive scope |
| Overlap with later unpublished experiments | Unverified; no extra exclusion hashes | Must disclose |

## C. What is completed and what remains

**Completed (no new GPU run required for these items):**

- Original-response replay on the exact frozen model and checkpoint.
- Independent-question within-model confirmation on 64 additional identities.
- Explicit input-token-count matching, raw-prompt comparison, and orthogonal-edit control.
- Question-cluster bootstrap analysis and numerical-gate verification.
- Outlier influence and question-length sensitivity checks (post hoc).
- Reproducible archive, figures, hashes and statistical-audit trail.
- Research-specific addendum text containing complete methods, results and limitations.

**Still needed for archiving/publication (no new GPU run):**

1. Compare the current original Paper 1 manuscript against the addendum and ensure no wording claims accuracy improvement, generalized model repair, isolated circuits, or data independence beyond the verified scope.
2. Check any journal-review policy and decide whether this is a supplemental analysis or formal manuscript revision. Keep the November 18 date explicit.
3. Merge the confirmation results into the **existing** GitHub repository as an additive release or pull request, not a second, contradictory manuscript.
4. For the existing Zenodo publication, use a **new version** if adding or revising published files, preserving the original version-specific record and its DOI. If GitHub release integration automatically deposits to Zenodo, check whether a release already creates the intended linked new version before depositing separately.
5. Add a clear revision history and accessible metadata indicating what was discovered *after* the original deposit.

**Additional experimental work only if scope is expanded:**

- A fresh heldout dataset never used to select or tune the original intervention would reduce possible GSM8K training exposure and history-overlap concerns.
- A different GPU/software stack or independent researcher would strengthen external repeatability.
- A different model/edit pair would address generalization but requires new intervention characterization and a new protocol.
- Generated-answer correctness tests would be necessary before claiming improved reasoning or repair.

These are legitimate limitations; no wording or offline statistic can remove them without suitable new evidence. They should not be silently treated as remaining tasks for the already-finished narrow Paper 1 confirmation.

## D. Suggested GitHub package structure

Add the following to the current repository using its established naming conventions:

```text
paper1-confirmation-2026-11-18/
  PAPER1_CONFIRMATION_ADDENDUM.md
  AUDIT_AND_PUBLICATION_HANDOFF.md
  FT_P1_CONFIRMATION_2026_11_18_ALL_RESULTS.zip
```

The nested results ZIP already contains original/fresh raw measurements, plots, source, frozen protocol and question hashes, checksums and an offline verifier. Maintain this original ZIP **unchanged** to preserve its validated manifest. Provide a short README in the GitHub folder linking to the existing original Paper 1 record and explaining that the addendum is a later within-model confirmation.

## E. Publication wording to prefer / avoid

| Prefer | Avoid |
|---|---|
| "Within-model confirmation on additional GSM8K question identities" | "Independent cross-model replication" |
| "Prompt-conditioned final-token logit response geometry" | "Improved mathematical reasoning accuracy" |
| "Effect persists under explicit token-count matching" | "Prompt length has been ruled out as a cause" |
| "Norm-matched orthogonal edit shows a much weaker contrast" | "Unique circuit proven" |
| "New cohort excludes frozen historical identities" | "Completely unseen by the base model and all previous experiments" |

## F. Final go/no-go

**GO** for publishing a **versioned confirmation supplement** to the existing first paper, provided the manuscript is edited to match the evidence limitations above. **NO-GO** for claiming universal model repair, improved answer accuracy, or independently reproduced results across different models/hardware. No public repository or Zenodo record has been edited as part of this handoff.
