# Identify the Animal — Zamba Solution

This repository contains a Zamba-based solution for the Trapstreet task `identify-the-animal`.

Goal:
- read one wildlife photo
- classify the animal
- print exactly one label

Current approach:
- run `zamba image predict`
- use the `speciesnet` image model
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

Zamba is built for animal classification from camera images.
That makes it a better fit than a generic chat-style agent.

This solution is designed to optimize for more than accuracy:
- score
- latency
- cost
- stable exact-label output

## Setup

Requires:
- Python 3.11+
- `uv`

Install deps:

```bash
uv sync
```

## Run locally

```bash
tp run identify-the-animal
```

## Submit

```bash
tp auth login
tp submit
```

## Notes

- This solution records per-case token/cost metrics only when available from the underlying stack.
- Zamba may output a larger taxonomy than the task expects, so this repo includes a mapping layer into the task's 10 labels.
