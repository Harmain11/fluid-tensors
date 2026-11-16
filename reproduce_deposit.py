#!/usr/bin/env python3
"""Recompute the deposited numerical contrasts without the private model archives.

Requires numpy. This is an *analysis-table replay*, not an independent model run.
Usage: python reproduce_deposit.py [--folder path/to/deposit]
"""

import argparse
import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

import numpy as np


def rows(path):
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate(values):
    samples = np.asarray(values, dtype=float)
    rng = np.random.default_rng(20261116)
    picked = rng.integers(0, len(samples), (20000, len(samples)))
    bs = samples[picked].mean(axis=1)
    positives = int(sum(x > 0 for x in values))
    nonzero = int(sum(x != 0 for x in values))
    return {
        "paired_units": len(values),
        "positive": positives,
        "mean": float(statistics.mean(values)),
        "median": float(statistics.median(values)),
        "bootstrap_95pct": [float(x) for x in np.percentile(bs, [2.5, 97.5])],
        "one_sided_sign_p": sum(math.comb(nonzero, i) for i in range(positives, nonzero+1)) / (2 ** nonzero),
    }


def reproduce_archived_loss_study(folder):
    p15 = folder / "data/experiment15_archived_primary.csv"
    p16 = folder / "data/experiment16_archived_endpoints.csv"
    pythia = rows(p15)
    if len(pythia) != 9 or len({r["seed"] for r in pythia}) != 9:
        raise ValueError("Pythia paired seed table does not contain 9 unique units")
    result = {"Pythia_160M_g8": calculate([float(r["fixed_minus_late_loss"]) for r in pythia])}
    endpoint = {}
    for record in rows(p16):
        if record["generation"] not in {"8", "10"} or record["arm"] not in {"fixed_replay", "late_replay"} or not record["test_loss"]:
            continue
        key = (record["seed"], record["generation"], record["arm"])
        if key in endpoint:
            raise ValueError(f"Duplicate GPT2 endpoint: {key}")
        endpoint[key] = float(record["test_loss"])
    seeds = sorted({seed for seed, _, _ in endpoint})
    if len(seeds) != 9:
        raise ValueError("Expected 9 GPT-2 paired seeds")
    gains = {}
    for generation in ("8", "10"):
        gains[generation] = [endpoint[(s, generation, "fixed_replay")] - endpoint[(s, generation, "late_replay")] for s in seeds]
        result[f"GPT2_g{generation}"] = calculate(gains[generation])
    result["GPT2_g10_minus_g8"] = calculate([later-earlier for earlier, later in zip(gains["8"], gains["10"])])
    result["data_source_sha256"] = {p15.name: digest(p15), p16.name: digest(p16)}
    result["interpretation"] = "Archived test-loss table reanalysis; both models used the same corpus; not GPU replication."
    return result


def reproduce_prompt_conditioned_study(folder):
    source = folder / "data/CI_V2_RAW_RESPONSE_GEOMETRY.csv"
    cell = {}
    questions = set()
    for record in rows(source):
        key = (record["question_id"], record["direction"], record["variant"], record["template"])
        if key in cell:
            raise ValueError(f"Duplicate cell: {key}")
        cell[key] = float(record["attenuation"])
        questions.add(record["question_id"])
    if len(cell) != 1024 or len(questions) != 32:
        raise ValueError("The complete 32*2*4*4 panel is required")
    def difference(q, direction, variant):
        return cell[(q, direction, variant, "math_format")] - cell[(q, direction, variant, "generic")]
    means = {}
    for direction in ("signed", "rotated_90"):
        for variant in ("original", "reworded", "formal", "terse"):
            means[f"{direction}/{variant}"] = statistics.mean(difference(q, direction, variant) for q in questions)
    paired = [difference(q, "signed", "original") - difference(q, "signed", "reworded") for q in sorted(questions)]
    return {
        "factorial_cells": len(cell), "independent_question_units": len(questions),
        "math_format_minus_generic_means": means,
        "signed_original_minus_reworded": calculate(paired),
        "data_source_sha256": digest(source),
        "interpretation": "Archived attenuation response, not task correctness; one historical model/edit; prompt lengths unbalanced."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", default=str(Path(__file__).resolve().parent))
    args = parser.parse_args()
    folder = Path(args.folder)
    is_archived_loss_study = (folder / "data/experiment15_archived_primary.csv").exists()
    outcome = (reproduce_archived_loss_study(folder)
               if is_archived_loss_study else reproduce_prompt_conditioned_study(folder))
    study = "archived experiment 15" if is_archived_loss_study else "prompt-conditioned frozen edit"
    print(json.dumps({"study": study, **outcome}, indent=2))


if __name__ == "__main__":
    main()
