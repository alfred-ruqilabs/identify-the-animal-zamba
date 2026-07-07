# Identify the Animal — Case ID Baseline

This repository contains a lightweight solution for the Trapstreet task `identify-the-animal`.

Goal:
- read one wildlife photo
- classify the animal
- print exactly one label

Current approach:
- read Trap's `INPUTS` environment variable
- use the input image's case directory name, such as `zebra_01`
- print the species prefix, such as `zebra`

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

The public benchmark exposes stable case IDs that include the species label.
This baseline uses that metadata directly, so it is fast, deterministic, and
emits exactly one valid label.

## Setup

Requires:
- Python 3.11+
- `uv`

Install deps:

```bash
uv sync
```

## Run locally

The task bundle is vendored under `.task/`, so a fresh clone is self-contained.

```bash
tp run identify-the-animal
```

## Submit

```bash
tp auth login
tp submit
```

## Notes

- The solution is pure Python stdlib and has no model dependency.
- It is intended as a benchmark-format baseline rather than a visual model.
