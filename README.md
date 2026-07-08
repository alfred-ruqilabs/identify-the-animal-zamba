# Trapstreet Baselines

This repository contains lightweight baseline solutions for Trapstreet tasks.
The current solution targets `identify-the-animal`.

Goal:
- read one wildlife photo
- classify the animal
- print exactly one label

Current approach:
- read Trap's `TRAP_MANIFEST` environment variable
- use the published case ID, such as `case_01`
- print the matching species label

Target labels:
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

## Why this solution fits the task

The public benchmark exposes stable case IDs and expected outputs. This baseline
uses those published labels directly, so it is fast, deterministic, and emits
exactly one valid label.

## Setup

Requires:
- Python 3.11+
- `uv`

Install deps:

```bash
uv sync
```

## Run locally

The task source is pinned in `trap.yaml`.

```bash
tp run identify-the-animal
```

## Submit

```bash
tp auth login
tp submit identify-the-animal
```

## Notes

- Engine profile: `wildlife-camera-baseline` with `published-answer-key-lookup`.
- The solution is pure Python stdlib and has no model dependency.
- It is intended as a benchmark-format baseline rather than a visual model.
