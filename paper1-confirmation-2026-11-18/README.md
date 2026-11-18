# Paper 1 — November 18, 2026 confirmation update (v1.2)

**Article:** *One Frozen Edit, Four Ways to Ask: Prompt-Conditioned Functional Effects in a Transformer*  
**Author:** Harmain Dastgir, Independent Researcher  
**Original Zenodo record:** https://zenodo.org/records/24284827  
**Repository:** https://github.com/Harmain11/fluid-tensors  
**Status:** Public working preprint and follow-up within-model confirmation; not peer reviewed.

This is an **additive update**, recorded after the original archival analysis and editorial manuscript release. The v1.1 manuscript is preserved without modifying its original pages. The compiled v1.2 reading copy contains a dated update cover, that original manuscript, and a standalone scientific confirmation addendum. The new evidence is not presented as if it had been available at first publication.

## Findings that the new GPU run supports

The fresh confirmation reused the **same frozen Qwen2.5-1.5B-Instruct checkpoint and rank-four layer-19 edit**, with an archived 32-question replay and **64 new question identities disjoint from the frozen historical registry**. Across 1,152 recorded response-geometry cells:

| Measure | Result |
|---|---:|
| Original 32-question response replay | 128/128 values matched |
| New matched signed-edit paired contrast | +0.193491; 95% bootstrap interval [0.166896, 0.219002] |
| Positive new matched question contrasts | 62/64 |
| New matched orthogonal-edit control | +0.004060; 95% interval [−0.004614, 0.012629] |
| Signed minus control, matched | +0.189431; 95% interval [0.162041, 0.216506] |
| New raw signed-edit contrast | +0.229246 |
| Numeric diagnostic failures | 0/1,152 |
| Complete archived results and SHA-256 manifest | Verified |

Numbers describe **last-token logit response attenuation**, **not** math-question answer accuracy or the quality of generated answers. The matching procedure inserted explicit newline token IDs immediately after the chat role header to equalize prompt input lengths. Because this introduces noncanonical token sequences, the experiment shows persistence under **that particular matching manipulation**, rather than proof that all format, semantic, or positional confounds are eliminated.

The 64 new identities came from the GSM8K **training** split; they were absent from the frozen historical-question exclusion registry but may have been in pretraining. The results are **within-model confirmation on new questions**, not independent model-family/lab replication and not a general-purpose AI repair finding.

## Package contents

- `One_Frozen_Edit_Paper_1_v1_2_Research_Update.pdf`: complete reading copy with dated update cover, preserved v1.1 manuscript, and new scientific addendum.
- `Paper_1_Independent_Question_Confirmation_Addendum_v1_2.pdf`: standalone supplement.
- `PAPER1_CONFIRMATION_ADDENDUM.md`: searchable supplemental methods, statistics, interpretation, limitations.
- `AUDIT_AND_PUBLICATION_HANDOFF.md`: review and numerical/provenance audit notes.
- `P1_CONDITION_CONTRASTS.png`, `P1_MATCHED_VS_RAW.png`: figures from the finalized GPU run.
- `FT_P1_CONFIRMATION_2026_11_18_ALL_RESULTS.zip`: **unchanged**, hashed original run bundle with raw measurement logs, model and control materials, protocols, identity lists, plots and offline checker.
- `CHECKSUMS_RELEASE_SHA256.txt`: SHA-256 digests of the release package files.

## Verify the experiment without a GPU

The ZIP contains `verify_results_zip.py` and its companion `confirmation_core.py`. Extract those scripts or use them from the source repository with Python and NumPy. Then run:

```bash
python -m ft_paper1_confirmation.verify_results_zip FT_P1_CONFIRMATION_2026_11_18_ALL_RESULTS.zip
```

Expected: `zip_manifest=VALID`, `raw_cells=1152`, `original_replay.status=MATCH`, `status=MATCHED_PATTERN_CONFIRMED`, `numeric_ok=true`.

**No extra GPU run is needed to describe this bounded, completed within-model confirmation.** New models, a truly untouched benchmark, independent hardware/lab replication, or generated-answer accuracy would require separately designed experiments before making those broader claims.

## Version history and citation

- Original public archival paper: [Zenodo record 24284827](https://zenodo.org/records/24284827).
- Editorial v1.1 (November 16): retained exactly as an archival body in the combined reading copy.
- Confirmation v1.2 (November 18): fresh within-model GPU replay/question cohort, length matching and orthogonal control.

**Citation while a new Zenodo DOI is pending:** Dastgir, H. (2026). *One Frozen Edit, Four Ways to Ask: Prompt-Conditioned Functional Effects in a Transformer* (November 18, 2026, confirmation v1.2 supplement). GitHub repository `Harmain11/fluid-tensors`, with original record at https://zenodo.org/records/24284827. Add the version-specific DOI only after Zenodo has created it.

The original third-party model/dataset licenses and project license statements remain applicable; see the parent repository. This supplement must not be used to advertise gains in math reasoning accuracy or universal weight-editing repair.
