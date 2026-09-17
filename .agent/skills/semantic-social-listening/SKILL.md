---
name: semantic-social-listening
description: Semantic and sentiment analysis of social media posts and comments. Parses spreadsheets (.xlsx) containing textual entries, runs local NLP heuristics, groups topics, and generates neutral landscape reports.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Semantic Social Listening Skill

This skill provides the knowledge and local scripts to parse, extract, analyze, and report on textual comment databases (e.g. scraped comments, posts, tweets) stored in Excel format.

---

## 1. Column Mapping Protocols

Social media scrapers and spreadsheet exports vary. The skill maps textual entries and engagement data dynamically using synonyms:

| Normalized Metric | Synonyms and Column Headers |
|-------------------|-----------------------------|
| **Text Content**  | Comentário, Comentarios, Texto, Post, Conteúdo, Text, Comment, Content, Body, Tweet |
| **Likes / Claps** | Curtidas, Likes, Reações, Reactions, Claps, Upvotes |
| **Author**        | Autor, Usuário, Username, Author, User, Profile |
| **Date**          | Data, Date, Timestamp, Publicado em, Created At |

---

## 2. Text Pre-Processing & Heuristics

To perform semantic and sentiment analysis at zero cost and high speed, the analysis must run locally:

### 2.1 Stopword Filtering
Before extracting frequencies, strip noise words. Stopwords are defined in both **Portuguese** and **English**:
* **Portuguese:** *a, o, que, e, do, da, em, um, para, é, com, não, uma, os, as, no, na, por, mais, ao, aos, se, umas, uns, como, mas, ou, foi, etc.*
* **English:** *the, a, an, and, of, to, in, is, that, it, for, on, with, as, this, with, at, by, an, be, etc.*

### 2.2 Local Sentiment Lexicon Heuristics
The classification engine evaluates text sentiment based on matching positive/negative keyword roots in a predefined local dictionary (avoiding slow and costly API connections).
* **Positive terms:** *bom, ótimo, adorei, amei, excelente, perfeito, top, maravilhoso, parabéns, melhor, incrível, sensacional, legal, valeu, obrigada, obrigado, super, gostei, sucesso*
* **Negative terms:** *ruim, péssimo, horrível, erro, bug, falha, odeio, chato, quebrado, lento, lixo, estragado, difícil, caro, absurdo, decepção, decepcionado, pior, não funciona*

*Sentiment calculation:*
$$\text{Score} = \text{Count}(\text{Positive terms}) - \text{Count}(\text{Negative terms})$$
* $\text{Score} > 0 \rightarrow$ **Positivo**
* $\text{Score} < 0 \rightarrow$ **Negativo**
* $\text{Score} == 0 \rightarrow$ **Neutro**

### 2.3 Semantic Topic Extraction
Identify main themes by calculating the frequency of n-grams (single words, 2-word combinations/bigrams) from comments, weighted by comment engagement (likes) if available.

---

## 3. Usage of `analyze_listening.py`

Execute the analysis script to parse Excel files and compile reports:

```bash
python .agent/skills/semantic-social-listening/scripts/analyze_listening.py --xlsx <caminho_da_planilha> --out <caminho_do_relatorio_md>
```

### Options:
* `--xlsx`: Absolute or relative path to the `.xlsx` data source.
* `--out`: Target path for the compiled `.md` markdown report.
* `--stopwords`: (Optional) Path to a custom text file with line-separated stopwords.
