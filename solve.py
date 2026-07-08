from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ALLOWED = [
    "buffalo",
    "cheetah",
    "elephant",
    "giraffe",
    "hyena",
    "leopard",
    "lion",
    "warthog",
    "wildebeest",
    "zebra",
]

ALIASES = {
    "buffalo": ["buffalo", "african buffalo", "cape buffalo"],
    "cheetah": ["cheetah"],
    "elephant": ["elephant", "african elephant"],
    "giraffe": ["giraffe"],
    "hyena": ["hyena", "spotted hyena"],
    "leopard": ["leopard"],
    "lion": ["lion"],
    "warthog": ["warthog"],
    "wildebeest": ["wildebeest", "gnu"],
    "zebra": ["zebra"],
}


def norm(s: str) -> str:
    return " ".join(s.lower().replace("_", " ").replace("-", " ").split())


def score_column(label: str, col: str) -> int:
    c = norm(col)
    best = 0
    for alias in ALIASES[label]:
        a = norm(alias)
        if c == a:
            best = max(best, 100)
        elif a in c:
            best = max(best, 60)
        elif any(tok in c for tok in a.split()):
            best = max(best, 20)
    return best


def pick_label(pred_rows: list[dict[str, str]]) -> str:
    best_label = None
    best_score = float("-inf")
    for row in pred_rows:
        for label in ALLOWED:
            candidates = []
            for col, raw in row.items():
                if col in {
                    "filepath",
                    "detection_category",
                    "detection_conf",
                    "x1",
                    "y1",
                    "x2",
                    "y2",
                }:
                    continue
                match_strength = score_column(label, col)
                if match_strength <= 0:
                    continue
                try:
                    prob = float(raw)
                except Exception:
                    continue
                candidates.append((match_strength, prob))
            if candidates:
                match_strength, prob = max(candidates, key=lambda x: (x[0], x[1]))
                combined = prob + match_strength / 1000.0
                if combined > best_score:
                    best_score = combined
                    best_label = label
    return best_label or "lion"


def main() -> None:
    manifest = json.loads(os.environ["TRAP_MANIFEST"])
    inputs_dir = Path(manifest["inputs_dir"])
    image_path = inputs_dir / "document.jpg"
    if not image_path.exists():
        image_path = inputs_dir / "document.jpeg"

    with tempfile.TemporaryDirectory(prefix="zamba-input-") as tmp_in, tempfile.TemporaryDirectory(
        prefix="zamba-out-"
    ) as tmp_out:
        tmp_in_path = Path(tmp_in)
        tmp_out_path = Path(tmp_out)
        local_img = tmp_in_path / image_path.name
        shutil.copy2(image_path, local_img)

        cmd = [
            "zamba",
            "image",
            "predict",
            "--data-dir",
            str(tmp_in_path),
            "--model",
            os.environ.get("ZAMBA_MODEL", "speciesnet"),
            "--save-dir",
            str(tmp_out_path),
            "--overwrite",
            "--yes",
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        csv_path = tmp_out_path / "zamba_predictions.csv"
        with csv_path.open(newline="") as f:
            rows = list(csv.DictReader(f))
        print(pick_label(rows))


if __name__ == "__main__":
    main()
