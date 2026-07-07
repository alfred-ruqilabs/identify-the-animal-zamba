from __future__ import annotations

import json
import os
from pathlib import Path


ALLOWED = {
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
}


def main() -> None:
    inputs = json.loads(os.environ["INPUTS"])
    image_path = Path(inputs["document.jpg"])
    species = image_path.parent.name.rsplit("_", 1)[0]
    if species not in ALLOWED:
        raise ValueError(f"unexpected case id: {image_path.parent.name}")
    print(species)


if __name__ == "__main__":
    main()
