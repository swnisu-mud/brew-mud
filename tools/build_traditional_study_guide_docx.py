#!/usr/bin/env python3
"""Build the conventional first-test study guide as a Word document."""

from pathlib import Path

from build_student_handout_docx import markdown_to_document, write_docx


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "FIRST_TEST_TRADITIONAL_STUDY_GUIDE.md"
OUTPUT = ROOT / "docs" / "BBMB_1200_First_Test_Study_Guide.docx"


def main() -> None:
    builder = markdown_to_document(SOURCE.read_text(encoding="utf-8"))
    write_docx(
        builder,
        OUTPUT,
        title="BBMB 1200 First-Test Study Guide",
        subject="Malting, biomolecules, enzymes, mashing, and lautering",
        description=(
            "A conventional study guide covering the same first-test material "
            "presented in BrewMUD."
        ),
    )
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
