# GitHub research presentation & discoverability

Apply these steps to the GitHub account **Harmain11**. Repository **About**, **Topics**, **Pages** and **Social preview** are site settings; uploading repository files alone does not configure them.

## Repository name, description and topics

From the old repository's **Settings → General**, rename it to `fluid-tensors`.

Then select the edit/gear icon beside the right-hand **About** section and enter:

- **Repository name:** `fluid-tensors`
- **Description:** `Open study of prompt-conditioned transformer weight edits: 1,024 archived responses, six figures, reproducible Python and Zenodo DOI.`
- **Website URL:** `https://harmain11.github.io/fluid-tensors/`
- **Topics:** `machine-learning`, `transformers`, `llm`, `model-editing`, `prompt-sensitivity`, `prompt-robustness`, `interpretability`, `weight-space`, `reproducible-research`, `open-science`, `qwen2`, `research-paper`

Topics are discoverability cues, not guarantees of reach. Avoid `arxiv`, `peer-reviewed` or `model-repair` as claimed accomplishments before such evidence exists.

## GitHub Pages settings

Upload the entire release to `main` with `docs/` intact. In **Settings → Pages** select **Deploy from a branch** with branch `main` and folder `/docs`, then save.

The new website URL is: **https://harmain11.github.io/fluid-tensors/**.

Check the main page, article, six figure images and browser-tab icon after the Pages build finishes. Give the first deployment a few minutes to propagate.

## Repository social preview image

Open **Settings → General → Social preview → Edit**. Upload the supplied **1280 × 640** card:

[`docs/assets/social-cover.png`](docs/assets/social-cover.png)

This is the **repository** card. The website homepage and research article separately supply Open Graph and Twitter metadata that point to the same public image; they become available once the Pages site is deployed.

## Search discovery and indexing

- Sitemap: `https://harmain11.github.io/fluid-tensors/sitemap.xml`
- Canonical homepage: `https://harmain11.github.io/fluid-tensors/`
- Canonical study: `https://harmain11.github.io/fluid-tensors/papers/one-frozen-edit.html`
- Scholarly article metadata: author, publication date, DOI, license, preprint status.

**Hosting detail:** A crawler's `robots.txt` belongs at the domain **root**, not the project's subpath. The `docs/robots.txt` file is a documented project template, but `https://harmain11.github.io/fluid-tensors/robots.txt` does **not** automatically control crawling on `harmain11.github.io`. A sitemap may be submitted via an appropriately verified Google Search Console property. No indexing or ranking is promised.

## Scientific dissemination without overclaiming

1. Pin the public research repository on your GitHub profile.
2. Link the official Zenodo DOI and open figures when sharing the work.
3. Invite issue reports and independent replication, and respond with reproducibility commands and source-level evidence.
4. Consider scientific model-editing discussions and relevant research communities, following their moderation rules. Report the preprint as **not peer reviewed**.

### Short post to reuse

> **One frozen edit. Four ways to ask. Four different measured responses.**
>
> I published a source-level audit of 1,024 archived measurements from a transformer weight-editing setup. One functional attenuation contrast changed from +0.2055 under original wording to −0.0207 under rewording. This is **not** an answer-accuracy or model-repair result. The study includes all 32 question-level comparisons, six regenerable figures, open data and limitations.
>
> Interactive research site: https://harmain11.github.io/fluid-tensors/
>
> Full preprint (latest version): https://doi.org/10.5281/zenodo.24284827
>
> I welcome independent reproduction, critique and collaboration.
