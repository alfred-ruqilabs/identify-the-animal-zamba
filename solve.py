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
                if col in {"filepath", "detection_category", "detection_conf", "x1", "y1", "x2", "y2"}:
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
    inputs = json.loads(os.environ["INPUTS"])
    outputs = json.loads(os.environ["OUTPUTS"])
    image_path = Path(inputs["document.jpg"]) if "document.jpg" in inputs else Path(inputs["document.jpeg"])
    outputs_dir = Path(next(iter(outputs.values()))).parent if outputs else Path('.')
    outputs_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="zamba-input-") as tmp_in, tempfile.TemporaryDirectory(prefix="zamba-out-") as tmp_out:
        tmp_in = Path(tmp_in)
        tmp_out = Path(tmp_out)
        local_img = tmp_in / image_path.name
        shutil.copy2(image_path, local_img)

        cmd = [
            "zamba",
            "image",
            "predict",
            "--data-dir",
            str(tmp_in),
            "--model",
            os.environ.get("ZAMBA_MODEL", "speciesnet"),
            "--save-dir",
            str(tmp_out),
            "--overwrite",
            "--yes",
        ]
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
        csv_path = tmp_out / "zamba_predictions.csv"
        with csv_path.open(newline="") as f:
            rows = list(csv.DictReader(f))
        answer = pick_label(rows)
        print(answer)


if __name__ == "__main__":
    main()
