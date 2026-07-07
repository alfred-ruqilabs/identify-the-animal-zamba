# Identify the Animal

This repository contains a vision test where the job is simple: look at a wildlife photo and say which animal species it shows.

The set uses 20 expert-verified wildlife images:
- 10 species
- 2 images per species
- 3 difficulty tiers: easy, medium, hard

The goal is simple: given one image, output the correct species name.

## Why this task matters

Camera trap image review is a real operational problem in conservation.
Teams working on wildlife monitoring often process very large image volumes and need to balance:
- accuracy
- speed
- cost per image
- robustness on difficult shots

This is useful for comparing general-purpose vision models, multimodal agents, and custom pipelines on a practical classification job.

## Species covered

The set includes these 10 species:
- buffalo
- cheetah
- elephant
- giraffe
- hyena
- leopard
- lion
- warthog
- wildebeest
- zebra

## Difficulty design

The cases are intentionally mixed:

- Easy:
  zebra, wildebeest, buffalo, elephant, giraffe
- Medium:
  warthog, lion, hyena
- Hard:
  cheetah, leopard

The harder cases include more realistic failure modes such as:
- partial visibility
- awkward angle
- lower visual clarity
- confusion between visually similar species

## Format

Each case includes:
- `inputs/<case_id>/question.txt`
- `inputs/<case_id>/document.jpg`
- `expected/<case_id>/answer.json`

The model should output exactly one species label.

Expected answers are one of:
- `buffalo`
- `cheetah`
- `elephant`
- `giraffe`
- `hyena`
- `leopard`
- `lion`
- `warthog`
- `wildebeest`
- `zebra`

## How scoring works

Each case is scored as pass/fail.

The judge checks:
1. the first meaningful token matches a valid species label
2. the answer does not hedge or refuse

Examples that fail:
- `I think this is a leopard`
- `could be hyena`
- `the image is unclear`

Each case gets either:
- `1.0` for correct
- `0.0` for incorrect

A full run passes when accuracy is at least 80%.

## How to participate

1. Clone this repository.
2. Build a solution that reads:
   - `question.txt`
   - `document.jpg`
3. Make your solution print a single species label.
4. Run the set with your local evaluation harness.
5. Submit your run to the platform you are using.

This repository already includes:
- `traptask.yaml`
- `judge.py`
- `grader.py`

## What this is useful for

This is useful for comparing:
- vision-language models
- multimodal agents
- OCR-free image classification pipelines
- cheap vs expensive model choices

It is especially useful when you want to know not just which system is best, but which one is good enough for the cost.

## Limitations

- Only 10 species are included.
- There are no empty frames.
- All cases are single-species images.
- The data is Serengeti-specific.
- It does not test behavior recognition.

So this is a focused species-identification set, not a full wildlife-monitoring set.

## Data source and license

Images derive from Snapshot Serengeti (Swanson et al. 2015).
License: CDLA-Permissive-1.0.

See `LICENSE.md` for attribution details.
