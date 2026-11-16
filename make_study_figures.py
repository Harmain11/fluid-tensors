#!/usr/bin/env python3
"""Rebuild six figures from archived CI V2.1 numeric cells.

All plots describe a source-table reanalysis, not new model inference or
correct-answer outcomes.  The 32 question IDs are the inference units.
Run: python make_study_figures.py
"""

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np


EXPECTED_SOURCE_SHA256 = "303c7a42509d2480107591bfd3c5c3467f657233aa272fba546fa73a2d374f77"
SEED = 20261116
BOOTSTRAP_DRAWS = 20000
VARIANTS = ("original", "reworded", "formal", "terse")
TEMPLATES = ("generic", "math_only", "format_only", "math_format")
DIRECTIONS = ("signed", "rotated_90")
TEAL, NAVY, BLUE, CORAL = "#148a89", "#15344a", "#789cb7", "#c56b53"
PAPER_BG = "#ffffff"


def load_matrix(csv_path):
    source_hash = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    if source_hash != EXPECTED_SOURCE_SHA256:
        raise ValueError(f"Unexpected source SHA-256: {source_hash}")
    with csv_path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    data = {}
    for row in rows:
        key = tuple(row[field] for field in ("question_id", "direction", "variant", "template"))
        if key in data:
            raise ValueError(f"Duplicate factorial cell: {key}")
        if not all(math.isfinite(float(row[field])) for field in
                   ("prompt_tokens", "attenuation", "cosine", "raw_logit_displacement", "tangent_norm")):
            raise ValueError(f"Non-finite source record at {key}")
        if int(row["prompt_tokens"]) <= 0:
            raise ValueError(f"Invalid token count at {key}")
        data[key] = row
    questions = sorted({key[0] for key in data})
    if len(questions) != 32 or len(data) != 1024:
        raise ValueError("Expected 32 question units and 1,024 factorial cells")
    for q in questions:
        for d in DIRECTIONS:
            for v in VARIANTS:
                for t in TEMPLATES:
                    if (q, d, v, t) not in data:
                        raise ValueError(f"Missing cell {(q, d, v, t)}")
    for q in questions:
        for v in VARIANTS:
            for t in TEMPLATES:
                if (data[(q, "signed", v, t)]["prompt_tokens"] !=
                        data[(q, "rotated_90", v, t)]["prompt_tokens"]):
                    raise ValueError("Prompt token counts differ across edit directions")
    return data, questions, source_hash


def cell(data, q, d, v, t, field="attenuation"):
    return float(data[(q, d, v, t)][field])


def contrast(data, q, d, v):
    return cell(data, q, d, v, "math_format") - cell(data, q, d, v, "generic")


def bootstrap_means(values, seed):
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    selections = rng.integers(0, len(values), size=(BOOTSTRAP_DRAWS, len(values)))
    return values[selections].mean(axis=1)


def configure():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 13,
        "axes.titleweight": "semibold",
        "axes.edgecolor": "#a5b4bd",
        "axes.labelcolor": NAVY,
        "xtick.color": "#5c7080",
        "ytick.color": "#5c7080",
        "figure.facecolor": PAPER_BG,
        "axes.facecolor": PAPER_BG,
        "savefig.facecolor": PAPER_BG,
        "svg.fonttype": "none",
    })


def save(fig, output, name):
    fig.savefig(output / name, dpi=240, bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "figures")
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parent / "data/CI_V2_RAW_RESPONSE_GEOMETRY.csv")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    data, questions, source_hash = load_matrix(args.data)
    configure()
    per_question = {
        d: {v: np.array([contrast(data, q, d, v) for q in questions])
            for v in VARIANTS} for d in DIRECTIONS
    }
    means = {d: {v: float(np.mean(per_question[d][v])) for v in VARIANTS}
             for d in DIRECTIONS}
    paired = per_question["signed"]["original"] - per_question["signed"]["reworded"]
    bs = bootstrap_means(paired, SEED)
    ci = [float(x) for x in np.quantile(bs, [0.025, 0.975])]
    expected = (0.20554245016147377, -0.020673286310999125, 0.2262157364724729)
    observed = (means["signed"]["original"], means["signed"]["reworded"], float(np.mean(paired)))
    if not all(abs(a - b) < 1e-12 for a, b in zip(expected, observed)):
        raise ValueError(f"Unexpected primary results: {observed}")

    # Figure 1: signed-edit wording means with descriptive question bootstrap intervals.
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    x = np.arange(4)
    vals = [means["signed"][v] for v in VARIANTS]
    ci_each = [np.percentile(bootstrap_means(per_question["signed"][v], SEED + 1 + i), [2.5, 97.5])
               for i, v in enumerate(VARIANTS)]
    yerr = np.array([[vals[i] - ci_each[i][0] for i in range(4)],
                     [ci_each[i][1] - vals[i] for i in range(4)]])
    ax.bar(x, vals, color=[TEAL, BLUE, BLUE, BLUE], width=0.64, zorder=3)
    ax.errorbar(x, vals, yerr=yerr, fmt="none", ecolor=NAVY, capsize=5,
                linewidth=1.5, zorder=5)
    for i, y in enumerate(vals):
        label_y = ci_each[i][1] + 0.012 if y >= 0 else ci_each[i][0] - 0.014
        ax.text(i, label_y, f"{y:+.3f}", ha="center", va="center",
                color=NAVY, fontweight="bold")
    ax.axhline(0, color=NAVY, linewidth=1.1)
    ax.set_xticks(x, [v.title() for v in VARIANTS])
    ax.set_ylabel("Mean signed-edit contrast (math + format minus generic)")
    ax.set_title("Figure 1  |  Wording conditions alter a fixed edit's measured response", pad=14)
    ax.grid(axis="y", color="#e8eff2", zorder=0)
    ax.set_ylim(-0.15, 0.32)
    fig.text(0.5, 0.01, "Error bars: descriptive 95% question-bootstrap intervals (32 questions per wording); not answer accuracy.",
             ha="center", fontsize=8.5, color="#657680")
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    save(fig, args.output_dir, "figure01_wording_mean_with_ci.png")

    # Figure 2: direction control, same 32 questions and wording families.
    fig, ax = plt.subplots(figsize=(9.2, 4.0))
    width = 0.36
    ax.bar(x - width / 2, [means["signed"][v] for v in VARIANTS], width,
           color=TEAL, label="Historical signed edit", zorder=3)
    ax.bar(x + width / 2, [means["rotated_90"][v] for v in VARIANTS], width,
           color=CORAL, label="90° rotated direction", zorder=3)
    ax.set_xticks(x, [v.title() for v in VARIANTS])
    ax.axhline(0, color=NAVY, linewidth=1.1)
    ax.set_ylabel("Mean contrast (math + format minus generic)")
    ax.set_title("Figure 2  |  Direction specificity in the archived control", pad=14)
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", color="#e8eff2", zorder=0)
    fig.text(0.5, 0.01, "One historical intervention and one rotated control; this is not a test of independently learned edits.",
             ha="center", fontsize=8.5, color="#657680")
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    save(fig, args.output_dir, "figure02_direction_control.png")

    # Figure 3: every question is its own paired observation.
    fig, ax = plt.subplots(figsize=(8.5, 7.0))
    ordered = np.sort(paired)
    ypos = np.arange(len(ordered))
    ax.hlines(ypos, 0, ordered, color="#b7d2d9", linewidth=1.5, zorder=1)
    ax.scatter(ordered, ypos, color=TEAL, s=36, zorder=3)
    ax.axvline(0, color=NAVY, lw=1.1)
    ax.axvline(np.mean(paired), color=CORAL, lw=1.7, ls="--",
               label=f"32-question mean = {np.mean(paired):+.3f}")
    ax.set_yticks(ypos, [f"Q{i:02d}" for i in range(1, 33)], fontsize=8)
    ax.set_ylim(-1, 32)
    ax.set_xlabel("Question-level original minus reworded signed-edit contrast")
    ax.set_title("Figure 3  |  Paired evidence across all 32 questions", pad=14)
    ax.grid(axis="x", color="#e8eff2")
    ax.legend(frameon=False, loc="lower right")
    fig.text(0.5, 0.012, "Q01–Q32 are sorted effect ranks (not source question IDs); all 32 paired differences are positive.",
             ha="center", fontsize=8.5, color="#657680")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, args.output_dir, "figure03_question_level_paired_effects.png")

    # Figure 4: full 2 x 4 x 4 factorial response matrix averaged over questions.
    heat = {
        d: np.array([[np.mean([cell(data, q, d, v, t) for q in questions])
                      for t in TEMPLATES] for v in VARIANTS]) for d in DIRECTIONS
    }
    extent = max(np.max(np.abs(heat[d])) for d in DIRECTIONS)
    norm = TwoSlopeNorm(vcenter=0, vmin=-extent, vmax=extent)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8), sharex=True, sharey=True)
    for ax, d, title in zip(axes, DIRECTIONS, ("Historical signed edit", "90° rotated control")):
        image = ax.imshow(heat[d], cmap="RdBu", norm=norm, aspect="auto")
        ax.set_xticks(range(4), ["Generic", "Math", "Format", "Math +\nformat"])
        ax.set_yticks(range(4), [v.title() for v in VARIANTS])
        ax.set_title(title, fontsize=12, pad=12)
        for i in range(4):
            for j in range(4):
                value = heat[d][i, j]
                ax.text(j, i, f"{value:+.3f}", ha="center", va="center", fontsize=9,
                        color="white" if abs(value) > 0.62 * extent else NAVY)
    fig.subplots_adjust(left=0.11, right=0.85, top=0.79, bottom=0.19, wspace=0.19)
    colorbar_axis = fig.add_axes([0.875, 0.22, 0.018, 0.52])
    fig.colorbar(image, cax=colorbar_axis,
                 label="Mean archived attenuation (not answer accuracy)")
    fig.suptitle("Figure 4  |  The full wording-by-template response map", fontsize=14,
                 fontweight="semibold", y=0.995, color=NAVY)
    fig.text(0.43, 0.03, "Each cell averages 32 question measurements; cells share questions and are not independent replications.",
             ha="center", fontsize=8.5, color="#657680")
    save(fig, args.output_dir, "figure04_factorial_response_heatmaps.png")

    # Supplement S1: nonparametric bootstrap reuses questions as units.
    fig, ax = plt.subplots(figsize=(9.2, 4.1))
    ax.hist(bs, bins=48, color=BLUE, edgecolor="white", alpha=0.95)
    ax.axvline(np.mean(paired), color=TEAL, lw=2.0, label=f"Observed mean {np.mean(paired):+.3f}")
    ax.axvline(ci[0], color=CORAL, lw=1.8, ls="--")
    ax.axvline(ci[1], color=CORAL, lw=1.8, ls="--",
               label=f"95% percentile interval [{ci[0]:+.3f}, {ci[1]:+.3f}]")
    ax.axvline(0, color=NAVY, lw=1.0)
    ax.set_xlabel("Bootstrap mean of 32 paired question-level contrasts")
    ax.set_ylabel("Bootstrap draw count")
    ax.set_title("Supplementary Figure S1  |  Question-level uncertainty", pad=14)
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#e8eff2")
    fig.text(0.5, 0.01, "20,000 draws; seed 20261116. Reanalysis of stored cells, not a new model experiment.",
             ha="center", fontsize=8.5, color="#657680")
    fig.tight_layout(rect=(0, 0.055, 1, 1))
    save(fig, args.output_dir, "figureS1_bootstrap_distribution.png")

    # Supplement S2: prompt token exposure varies with wording and template.
    token_means = np.array([[np.mean([cell(data, q, "signed", v, t, "prompt_tokens")
                                      for q in questions]) for t in TEMPLATES] for v in VARIANTS])
    token_deltas = {v: [int(cell(data, q, "signed", v, "math_format", "prompt_tokens") -
                            cell(data, q, "signed", v, "generic", "prompt_tokens"))
                        for q in questions] for v in VARIANTS}
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.8), gridspec_kw={"width_ratios": [1.35, 1]})
    im = ax.imshow(token_means, cmap="Blues", vmin=max(0, token_means.min() - 8),
                   vmax=token_means.max() + 5, aspect="auto")
    ax.set_xticks(range(4), ["Generic", "Math", "Format", "Math +\nformat"])
    ax.set_yticks(range(4), [v.title() for v in VARIANTS])
    ax.set_title("Mean prompt tokens by condition", fontsize=11)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{token_means[i, j]:.1f}", ha="center", va="center", color=NAVY)
    fig.colorbar(im, ax=ax, shrink=0.78, label="Recorded mean tokens")
    dy = [float(np.mean(token_deltas[v])) for v in VARIANTS]
    ax2.barh(range(4), dy, color=[TEAL, BLUE, BLUE, BLUE], height=0.55)
    ax2.set_yticks(range(4), [v.title() for v in VARIANTS])
    ax2.invert_yaxis()
    ax2.set_xlim(0, max(dy) + 4)
    ax2.set_xlabel("Extra tokens: math + format vs generic")
    ax2.set_title("Template change alters token length", fontsize=11)
    for i, value in enumerate(dy):
        ax2.text(value + 0.25, i, f"+{value:.0f}", va="center", color=NAVY)
    fig.suptitle("Supplementary Figure S2  |  Length and position confounding", fontsize=14,
                 fontweight="semibold", y=1.02, color=NAVY)
    fig.text(0.5, -0.025, "Token counts do not isolate semantics from changed positions. No length-matched causal control was performed.",
             ha="center", fontsize=8.5, color="#657680")
    fig.tight_layout(rect=(0, 0.045, 1, 0.96), w_pad=2.5)
    save(fig, args.output_dir, "figureS2_prompt_token_diagnostics.png")

    # Machine-readable figure statistics keep the narrative independently auditable.
    source_stats = {
        "study": "prompt-conditioned frozen edit",
        "source_sha256": source_hash,
        "factorial_cells": len(data),
        "question_units": len(questions),
        "question_level_signs": dict(Counter("positive" if x > 0 else "zero" if x == 0 else "negative" for x in paired)),
        "paired_mean": float(np.mean(paired)),
        "paired_median": float(np.median(paired)),
        "paired_min": float(np.min(paired)),
        "paired_max": float(np.max(paired)),
        "paired_q1_q3": [float(x) for x in np.quantile(paired, [0.25, 0.75])],
        "paired_bootstrap_95pct": ci,
        "bootstrap_seed": SEED,
        "bootstrap_draws": BOOTSTRAP_DRAWS,
        "direction_wording_contrast_means": means,
        "full_attenuation_mean_heatmaps": {k: v.tolist() for k, v in heat.items()},
        "mean_prompt_tokens": token_means.tolist(),
        "delta_prompt_tokens_math_format_minus_generic": {
            v: {"mean": float(np.mean(values)), "min": int(np.min(values)),
                "max": int(np.max(values))} for v, values in token_deltas.items()
        },
        "wording_order": VARIANTS,
        "template_order": TEMPLATES,
        "scope": "Source-level reanalysis; no new model inference or answer-correctness measurement",
    }
    (args.output_dir / "FIGURE_STATISTICS.json").write_text(
        json.dumps(source_stats, indent=2) + "\n", encoding="utf-8"
    )
    with (args.output_dir / "QUESTION_LEVEL_CONTRASTS.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["question_id", "signed_original", "signed_reworded", "original_minus_reworded"])
        for index, q in enumerate(questions):
            writer.writerow([q, per_question["signed"]["original"][index],
                             per_question["signed"]["reworded"][index], paired[index]])
    print(json.dumps({"figures_generated": 6, "question_units": len(questions),
                      "paired_mean": float(np.mean(paired)), "paired_bootstrap_95pct": ci,
                      "paired_min_max": [float(np.min(paired)), float(np.max(paired))]}, indent=2))


if __name__ == "__main__":
    main()
