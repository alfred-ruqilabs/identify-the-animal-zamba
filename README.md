# Wildlife Classifier Zamba

This repository contains a Zamba-based computer vision wildlife image classifier for the
Trapstreet task `identify-the-animal`.

Goal:
- read one wildlife photo
- classify the animal
- print exactly one label

Current approach:
- read Trap's `TRAP_MANIFEST` environment variable
- run `zamba image predict`
- use Zamba's `speciesnet` computer vision image-classification model
- read the prediction CSV
- map the model's labels into the 10 labels used by the task
- choose the highest-scoring allowed label

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

Zamba is built for animal classification from camera images. This solution uses
the `speciesnet` model through the Zamba CLI, then normalizes the model output
into the task's required label set.

## Setup

Requires:
- Python 3.11+
- `uv`
- Zamba dependencies installed by `uv sync`

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

- Engine profile: `zamba-speciesnet-cv` with framework `zamba`.
- The computer vision model is Zamba's `speciesnet`, invoked with `zamba image predict --model speciesnet`.
- Zamba may output a larger taxonomy than the task expects, so this repo includes a mapping layer into the task's 10 labels.
