"""Build the student notebooks (*_no_solutions.ipynb) from the notebooks with the solutions.

Every cell with the tag 'solution' in its metadata is removed; everything else is copied as it is.
Run it from this folder after every change to the notebooks with the solutions:

    python make_student_versions.py
"""
import json

NOTEBOOKS = [
    'Lab1_1_TMS_text_preprocessing',
    'Lab1_2_TMS_document_representation',
    'Lab1_3_TMS_word_embeddings',
]

for name in NOTEBOOKS:
    nb = json.load(open(f'{name}.ipynb', encoding='utf-8'))
    before = len(nb['cells'])
    nb['cells'] = [c for c in nb['cells'] if 'solution' not in c['metadata'].get('tags', [])]
    with open(f'{name}_no_solutions.ipynb', 'w', encoding='utf-8') as f:
        f.write(json.dumps(nb, indent=2, ensure_ascii=False))
    print(f'{name}: {before} cells -> {len(nb["cells"])} cells')
