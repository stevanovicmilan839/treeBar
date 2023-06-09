#!/usr/bin/env python
from __future__ import annotations

import os

BASE_DIR = os.path.dirname(__file__)
BWIPP_PATH = os.path.join(
    BASE_DIR, "src", "treepoem", "postscriptbarcode", "barcode.ps"
)
BARCODE_TYPES_PATH = os.path.join(BASE_DIR, "src", "treepoem", "data.py")


def main() -> None:
    print(f"Loading barcode types from {BWIPP_PATH}")
    all_barcode_types = load_barcode_types()

    print(f"Writing out {BARCODE_TYPES_PATH}")
    write_out_barcode_types(all_barcode_types)

    print("Done")


def load_barcode_types() -> list[tuple[str, str]]:
    barcode_types: list[tuple[str, str]] = []
    type_code: str | None = None
    description: str | None = None
    with open(BWIPP_PATH) as fp:
        for line in fp:
            if line.startswith("% --BEGIN ENCODER ") and line.endswith("--\n"):
                type_code = line[len("% --BEGIN ENCODER ") : -len("--\n")]
            elif line.startswith("% --DESC: "):
                description = line[len("% --DESC: ") :].strip()
            elif line.startswith("% --END ENCODER ") and line.endswith("--\n"):
                assert isinstance(type_code, str)
                assert isinstance(description, str)
                barcode_types.append((type_code, description))
                type_code = description = None

    return sorted(barcode_types)


def write_out_barcode_types(all_barcode_types: list[tuple[str, str]]) -> None:
    with open(BARCODE_TYPES_PATH, "w") as fp:
        fp.write("from __future__ import annotations\n")
        fp.write("\n")
        fp.write("\n")
        fp.write("class BarcodeType:\n")
        fp.write("    def __init__(self, type_code: str, description: str) -> None:\n")
        fp.write("        self.type_code = type_code\n")
        fp.write("        self.description = description\n")
        fp.write("\n\n")
        fp.write("# All supported barcode types, extracted from barcode.ps\n")
        fp.write("barcode_types: dict[str, BarcodeType] = {\n")
        for type_code, description in all_barcode_types:
            fp.write(
                f"    {type_code!r}: BarcodeType({type_code!r}, {description!r}),\n"
            )
        fp.write("}\n")


if __name__ == "__main__":
    main()
