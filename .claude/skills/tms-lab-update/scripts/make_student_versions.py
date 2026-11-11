"""Build the student notebooks (*_no_solutions.ipynb) from the notebooks with the solutions.

Every cell with the tag 'solution' in its metadata is removed; everything else is copied as it is.

Usage (from the repository root):
    python .claude/skills/tms-lab-update/scripts/make_student_versions.py Lab1
    python .claude/skills/tms-lab-update/scripts/make_student_versions.py Lab2 Lab3
"""
import json
import sys
from pathlib import Path


def build(folder: Path) -> None:
    sources = sorted(p for p in folder.glob('*.ipynb') if not p.stem.endswith('_no_solutions'))
    if not sources:
        print(f'{folder}: no notebooks found')
        return
    for src in sources:
        nb = json.loads(src.read_text(encoding='utf-8'))
        before = len(nb['cells'])
        nb['cells'] = [c for c in nb['cells'] if 'solution' not in c['metadata'].get('tags', [])]
        dst = src.with_name(f'{src.stem}_no_solutions.ipynb')
        dst.write_text(json.dumps(nb, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'{src.name}: {before} cells -> {dst.name}: {len(nb["cells"])} cells')


if __name__ == '__main__':
    folders = sys.argv[1:] or ['.']
    for name in folders:
        build(Path(name))
