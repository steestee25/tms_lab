"""Rebuild got1..4_nostops.csv for Lab 2.1 (one row per chapter: Name, Chapter, Text).

Input: the text of the first 4 books of A Song of Ice and Fire, from the Kaggle dataset
"Game of Thrones Book Dataset" (files '1 - A Game of Thrones.txt' ... '4 - A Feast for Crows.txt').
Output: got1_nostops.csv ... got4_nostops.csv, to put in the course Drive folder (the books are
copyrighted: do not commit the texts or the CSV files to the public repository).

Usage:  python build_got_csv.py <folder with the 4 .txt files> <output folder>

Chapters are split at the titles (the name of the point-of-view character); 'Alayne' counts as
Sansa and 'Cat of the Canals' as Arya; the pages before the prologue are 'Intro', the appendix is
one 'Appendix' document. Text: lowercase, letters only, NLTK English stop words removed.
"""
import re, sys, collections, pandas as pd, nltk
src, out = sys.argv[1], sys.argv[2]
nltk.download('stopwords', quiet=True)
STOP = set(nltk.corpus.stopwords.words('english'))
FIX = {'DAFNERYS': 'DAENERYS', 'CALTELYN': 'CATELYN', 'CATIELYN': 'CATELYN', 'ALAYNE': 'SANSA', 'CAT OF THE CANALS': 'ARYA'}
FILES = ['1 - A Game of Thrones.txt', '2 - A Clash of Kings.txt', '3 - A Storm of Swords.txt', '4 - A Feast for Crows.txt']
APPENDIX_START = {1: None, 2: 'APPENDIX', 3: 'THE KING ON THE IRON THRONE', 4: 'APPENDIX'}

def clean(text):
    words = re.findall(r"[a-z]+", text.lower().replace('’', "'"))
    return ' '.join(w for w in words if w not in STOP)

for b, name in enumerate(FILES, 1):
    t = open(f'{src}/{name}', encoding='utf-8', errors='replace').read().replace('\r', '')
    t = re.sub(r'(?m)^Page \d+\s*$', '', t)                     # page numbers of the PDF
    lines = t.split('\n')
    heads = []                                                   # (line index, title)
    for i, l in enumerate(lines):
        s = l.strip()
        if re.fullmatch(r"Chapter \d+", s):                      # book 3: 'Chapter N' then the name
            j = i + 1
            while not lines[j].strip(): j += 1
            heads.append((j, lines[j].strip().upper())); continue
        if (re.fullmatch(r"[A-Z][A-Z'’\ufffd ]{2,}", s) or s == 'Epilogue') and not (heads and heads[-1][0] == i):
            heads.append((i, s.upper().replace('\ufffd', "'").replace('’', "'")))
    # documents: Intro = everything before the prologue; Appendix = from its start to the end
    docs, intro_end = [], next(i for i, h in heads if h == 'PROLOGUE')
    docs.append(('Intro', '\n'.join(lines[:intro_end])))
    app = APPENDIX_START[b]
    for k, (i, h) in enumerate(heads):
        if i < intro_end: continue
        if app and h == app:
            docs.append(('Appendix', '\n'.join(lines[i + 1:]))); break
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        h = FIX.get(h, h)
        docs.append((h.title().replace("'S", "'s"), '\n'.join(lines[i + 1:end])))
    df = pd.DataFrame(docs, columns=['Name', 'Raw'])
    df = df[df.Raw.str.strip().str.len() > 0]
    df['Chapter'] = df.groupby('Name').cumcount() + 1
    df['Text'] = df.Raw.apply(clean)
    df[['Name', 'Chapter', 'Text']].reset_index(drop=True).to_csv(f'{out}/got{b}_nostops.csv')
    print(name, len(df), 'documents')
