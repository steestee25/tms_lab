---
name: tms-lab-update
description: Linee guida per rivedere e aggiornare i notebook dei lab di Text Mining & Search (cartelle LabN/): revisione di coerenza testo/codice/output, struttura degli esercizi, soluzioni commentate, versioni studente *_no_solutions, verifica eseguendo, quiz Mentimeter. Usala ogni volta che si rivede, corregge o prepara un notebook di laboratorio o un quiz per questo corso.
---

# Aggiornare un lab di Text Mining & Search

Questa skill raccoglie quello che abbiamo imparato rivedendo Lab1, compresi i feedback degli studenti. Va seguita per Lab2, Lab3 e per le modifiche future.

Chi tiene il corso è Stefano Molari (UniMiB). Le slide sono su Canva: chiedi il link del lab e leggile con lo strumento Canva `read-design`.

## 0. Regole di comunicazione con il docente

- Scrivi in **italiano**, in modo semplice. Per ogni punto segui lo schema: **problema → causa → esempio con i dati veri → domanda**. **Mostra il dato, non riassumerlo.**
- **Non citare mai i numeri di cella**: Colab non li mostra. Indica la **sezione** (il titolo `#`) e il **testo da cercare** tra virgolette.
- **Non dichiarare un risultato che non hai eseguito.** Distingui sempre cosa hai verificato e cosa no, e dì perché (per esempio "manca `spam.csv`").
- Se il docente chiede il testo di una cella, **scrivilo in chat in un blocco pronto da incollare**, anche se l'hai già messo nel notebook.
- Prima di modifiche grandi (togliere esercizi, ristrutturare, cancellare file) **proponi e chiedi**. Le correzioni piccole e ovvie falle e poi riportale.
- Se una frase del docente è ambigua o interrotta, dichiara come l'hai interpretata.

## 1. Convenzioni del repository

```
LabN/
├── LabN_k_TMS_<topic>.ipynb               ← versione del docente: consegne + soluzioni
└── LabN_k_TMS_<topic>_no_solutions.ipynb  ← versione studente: GENERATA, non modificarla a mano
```

- I notebook sono in **inglese**: testo, commenti, risposte.
- Le celle di soluzione hanno il tag **`solution`** nei metadati (`cell.metadata.tags`). La versione studente si ottiene togliendole:
  ```bash
  python .claude/skills/tms-lab-update/scripts/make_student_versions.py LabN
  ```
  Rigenerala dopo **ogni** modifica alla versione del docente.
- Quando scrivi un notebook via Python, usa `json.dumps(nb, indent=2, ensure_ascii=False)`, che è il formato di Colab. Così il diff resta piccolo.
- Commit con messaggi chiari. Fai push sul branch di lavoro e, come concordato con il docente, anche su `main`.

## 2. Fasi del lavoro su un lab

1. **Leggi** le slide del lab e i notebook (markdown + codice + output salvati).
2. **Esegui** ogni notebook da capo (vedi §7) e confronta gli output salvati con quelli veri.
3. **Rapporto di revisione** al docente: elenco numerato dei problemi (§3), con sezione, testo da cercare, dato vero e proposta.
4. **Correggi** dopo l'ok. Poi **struttura gli esercizi** (§4), **commenta le soluzioni** (§5) e **collega teoria e codice** (§6).
5. **Controlla l'autonomia** della versione studente (§4.3) e rigenerala.
6. **Verifica** eseguendo sia la versione del docente sia quella studente (§7).
7. **Commit e push**, poi un riepilogo al docente con i dati.

## 3. Checklist di revisione (cosa cercare)

- **Testo e codice non coincidono.** Esempi trovati in Lab1: la tabella diceva `U14.` ma il testo di esempio aveva `U9.`; un commento diceva "from the sample text" per esempi che non c'erano; una frase era troncata.
- **Output vecchi.** In Lab1_3 c'era `(56, 100)` invece di `(60, 100)`, e un refuso nella query salvata. Riesegui e salva.
- **Celle che non stampano niente**, oppure che modificano una variabile senza mostrare l'effetto.
- **Codice morto**, per esempio una variabile assegnata due volte di fila.
- **Domande della consegna senza risposta** nella soluzione: ogni domanda deve avere la sua risposta (§5).
- **Soluzioni che coprono solo una parte** della consegna (per esempio "compare different metrics" risolto con una metrica sola).
- **Numeri diversi tra calcolo a mano e libreria**: spiega il perché con i numeri (per esempio TF-IDF di sklearn: idf smussato + normalizzazione).
- **Segni o valori strani** in una tabella (per esempio un "vocabulary lost" negativo): capisci se è un errore del codice o un risultato vero, e spiegalo.
- **Link** obsoleti o che non corrispondono al suggerimento (`str.find` contro `str.contains`).
- **Dati mancanti nel repo** (per esempio `spam.csv`, `data_summary.csv`): segnalalo; se il dataset è pubblico, prova a scaricarlo (§7).
- **Differenze dalle slide**: risultati che con il modello del notebook non tornano (per esempio *biggest − big + small* con GloVe dà `largest`, non `smallest`). Avvisa il docente.

## 4. Struttura degli esercizi

### 4.1 Tempo e posizione (dai feedback di Lab1)
- Gli studenti chiedono **più tempo per lavorare da soli**. Ogni esercizio deve durare **10–15 minuti**.
- Metti un **esercizio breve dopo ogni blocco di teoria**, non tutti alla fine. Le parti di sola consultazione (in Lab1: POS, chunking, NER) si possono segnare come *self-study*.

### 4.2 Celle di ogni esercizio (nella versione del docente)
```
# Exercise N.k: <title>                  ← markdown: consegna
[given cells]                             ← dati/preparazione non centrali (es. corpus tokenizzato)
[skeleton with ___]                       ← facoltativo, per esercizi lunghi
# Your code here                          ← cella vuota per lo studente
### How to think about it                 ← tag solution: il ragionamento in 3-4 passi, senza codice
### Solution N.k                          ← tag solution
[solution code, commented]                ← tag solution
**Answers** / **What to look for**        ← tag solution: una risposta per ogni domanda
```
La cella *How to think about it* viene da un feedback degli studenti ("spiegare il ragionamento per la soluzione"). Va scritta per prima: è il piano che il codice poi segue, con i commenti numerati `# 1.`, `# 2.`, … Struttura (il docente ha chiesto "un pelino più di spiegazione"):

```markdown
### How to think about it

**Goal:** cosa vogliamo ottenere, in una frase.

1. **Nome del passo.** Cosa fare (con la funzione da usare) **e perché** (1–2 frasi).
2. …

**Watch out:** l'errore più comune in questo esercizio.
```

### 4.3 Test di autonomia (obbligatorio)
Rileggi **ogni** esercizio della versione studente e chiediti: *lo studente ha tutto quello che serve?*
- La consegna dice **quali dati usare** e con quale nome di variabile (in Lab1_2 mancava: "use `corpus_df.Document`"). Se servono, indica anche le query o i parametri da provare.
- Ogni funzione o variabile citata nella consegna o nei suggerimenti **esiste nella versione studente**: è mostrata prima nel notebook oppure è data in una cella. Esempio di errore: il suggerimento citava "the `steps` dictionary of Exercise 1.1", ma `steps` esisteva solo nella soluzione.
- Ogni API nuova è **mostrata prima** su un esempio giocattolo diverso dall'esercizio (in Lab1_3: la sezione *Introduction to gensim*). Così si vede **come chiamarla e in che forma passare i dati**, senza svelare la soluzione.
- I nomi che servono negli esercizi successivi sono **fissati** (per esempio `corpus`, `model`), e le firme delle funzioni sono scritte nella consegna se un esercizio dopo le riusa.
- Niente rimandi ambigui come "adapt the previous one": scrivi quale funzione e di quale esercizio.
- Esegui la versione studente da capo: deve girare **senza errori** (le celle `# Your code here` sono vuote; lo scheletro con `___` è definito ma non chiamato).

## 5. Soluzioni e risposte

- **Commenti nel codice**: brevi, chiari e **utili**. Dicono *cosa fa* l'istruzione e *perché*, non ripetono il codice. Togli i commenti inutili come `# EXERCISE: fit to the corpus` o `# try also X and see what happens!`. Se cambi solo i commenti, verifica che il codice sia identico confrontando l'AST (`ast.dump(ast.parse(src))`).
- **Ogni domanda della consegna ha una risposta** nella cella *Answers*, etichettata come la domanda (A, B, …), con i **numeri veri** calcolati sui dati del notebook.
- **Risultati casuali** (Word2Vec, Doc2Vec, k-means, …): con `workers > 1` il `seed` non basta. Nelle risposte **non scrivere liste esatte** di parole o di documenti vicini: scrivi solo quello che resta vero a ogni esecuzione (il *tipo* di parole, i punteggi ≈ 0.99, i numeri riassuntivi). Aggiungi una volta per notebook la nota *"Note: your results may differ"*.
- Le spiegazioni usano esempi piccoli e concreti del corpus, con il calcolo scritto (per esempio "√7 = 2.65 contro √9 = 3.00" per mostrare perché la distanza euclidea preferisce i documenti corti).

## 6. Collegare teoria e codice (dai feedback di Lab1)

Feedback di uno studente: *"For matching the codes with theoretical part is hard for me because it was too fast. More explanation on the codes like what are they referring to"*.
- All'inizio di ogni sezione metti un riquadro **"From the slide to the code"**: una **tabella a due colonne**, *In the slide* | *In the code*. Per esempio:

  ```markdown
  **📎 From the slide to the code** · slide *TF-IDF*

  | In the slide | In the code |
  |---|---|
  | df(w): in how many documents w appears | `df = (X_count > 0).sum(axis=0)` |
  | IDF(w) = log(n / df(w)) | `idf = np.log10(n / df)` |
  ```
  Regole (dal feedback del docente: il formato a frecce e citazioni "non si capiva"):
  - **3–5 righe** per tabella; ogni riga = **un** concetto ↔ **una** riga di codice;
  - colonna sinistra: il concetto **in poche parole**, non la frase intera della slide; niente virgolette;
  - colonna destra: il **codice esatto** del notebook, al massimo con 4–6 parole di spiegazione;
  - **niente frecce, niente elenchi** (un elenco numerato dentro un punto elenco si rompe in Colab), niente blockquote `>`;
  - mai il carattere `|` dentro una cella: rompe la tabella (riscrivi la regex o la formula senza).
- Lo script della lezione per il docente (tempi, righe 🔑/👀/⏭, domande ❓ "prevedi, poi esegui", come presentare le soluzioni) si scrive su richiesta: vedi lo script di Lab 2.1 come modello.
- Usa nel codice **gli stessi nomi** delle slide (`tf`, `idf`, `df`, `window`, `vector_size`, …).
- Se il notebook spiega la teoria (per esempio *How Doc2Vec learns*), usa **le stesse parole e lo stesso esempio della slide**.
- Suggerimento per l'aula, da proporre al docente: "prevedi, poi esegui", cioè chiedere cosa ci si aspetta prima di eseguire una cella.

## 7. Verifica tecnica (ambiente cloud)

- Esegui i notebook con `jupyter nbconvert --to notebook --execute` su una **copia** nello scratchpad. Poi ricopia nel file del repo **solo** `outputs` ed `execution_count`, così non perdi metadati e tag.
- NLTK nel sandbox: imposta `NLTK_ALLOW_PROXIED_URLOPEN=1` per `nltk.download`.
- gensim: `GENSIM_DATA_DIR=<scratchpad>/gd`, così GloVe (128 MB) si scarica una volta sola.
- Celle che montano Google Drive (`drive.mount`) non girano qui. Ricostruisci i dati in un harness Python con le stesse funzioni del notebook.
- Dataset pubblici: scaricali in una cartella separata dello scratchpad e controlla che coincidano con gli output del notebook. `spam.csv` (Lab1) l'abbiamo preso da `raw.githubusercontent.com/mohitgupta-omg/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv`: 5,572 righe e 455,188 caratteri, uguale al notebook.
- Dopo l'esecuzione controlla che nel `.ipynb` non restino percorsi del sandbox (`scratchpad`, `claude-0`) né errori `Security Violation`.
- Piccole differenze da versioni diverse delle librerie (per esempio ±2 token con NLTK) vanno dichiarate nelle risposte.
- **Dati non scaricabili qui** (in Lab2: Dropbox, Google Drive e Hugging Face rispondono 403): esegui con `--allow-errors` e unisci gli output cella per cella. Se la cella è andata bene, tieni l'output nuovo; se è fallita per i dati mancanti, tieni l'output salvato in Colab. Per i comandi `!` (pip, wget, ls) tieni sempre l'output di Colab: quello locale mostra file e percorsi della sandbox.
- Se un numero eseguito qui differisce da quello di Colab e delle slide per la versione della libreria (in Lab2: CV DT 0.85 qui contro 0.86 in Colab), tieni l'output di Colab e segnalalo al docente.
- Prima di partire, controlla con `git log --all -- <file>` se in un altro branch esiste già una versione corretta del lab (Lab2 era stato corretto nel branch `claude/eloquent-clarke-q0huln`, mai unito a `main`).

## 8. Quiz Mentimeter

- Le domande seguono **l'ordine delle slide**. Sono in **inglese**: 4 opzioni, una corretta (✅), e una **spiegazione breve** per ogni domanda.
- Evita le domande banali (per esempio "quale non è una libreria NLP"). Preferisci casi presi dai notebook, con dati veri: output inattesi, scelte di pre-processing, numeri da interpretare.
- Verifica ogni risposta **eseguendo** il codice. Se slide e notebook danno risultati diversi (per esempio la NER: `LOCATION` nelle slide, `GPE` in NLTK), riformula la domanda.
- Testi brevi: Mentimeter limita la lunghezza di domande e opzioni.

## 9. Feedback degli studenti (da aggiornare dopo ogni lab)

**Lab1:**
- Vogliono **più tempo** per fare gli esercizi da soli.
- *"For matching the codes with theoretical part is hard for me because it was too fast. More explanation on the codes like what are they referring to"* → §6.
- *"Magari spiegare il ragionamento per la soluzione"* → cella *How to think about it* (§4.2).
- Le soluzioni di Lab1_3 non sono state mostrate in aula. Piano: pubblicarle e riprendere 3.3–3.4 nei primi 10 minuti di Lab2, come ponte verso *K-Means over a Doc2Vec representation* (L2_1).
