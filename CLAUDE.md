# CO5059 Advanced System Architectures — notes project

Study materials for CO5059 (HCMUT, semester 261, Assoc. Prof. Tran Ngoc Thinh).
Owner: Phan Nhat Minh (presented Group 1, Cache). Goal: the **final exam**. Two A4
sheets of notes are allowed, printed double-sided (= the 4-page cheat sheet).

## Final exam scope (lecturer's review slides, `reviews/final_exam_review/Review_final_2026.pdf`)

- Introduction: performance (time, throughput, instruction types, CPI), Amdahl's law.
- Instruction set principles: all. Pipelining: all.
- Cache: organization (FA, set associative, DM); replacement (LRU, Clock, Tree-LRU, FIFO);
  write policies (WT, WB, write allocate, no-write allocate); the 3 Cs; AMAT, hit/miss rate,
  multilevel caches.
- Virtual memory: translation, page table, TLB; paging, segmentation; replacement.
- Multiprocessors: Flynn, UMA/NUMA; spin lock, barrier; superpipelining, superscalar,
  multithreading; dependences, in-order/out-of-order issue and completion, VLIW;
  coherence (directory, snoopy, MSI, MESI).

## Layout

- `slides/` — read-only, named `NN-topic-source.pdf` (NN = topic number): `01-introduction-lecture`,
  `02-isa-lecture`, `03-pipelining-lecture` (taught by the lecturer, one slide per PDF page);
  `04-cache-lecture`, `05-virtual-memory-lecture` (lecturer handouts, several slides per page);
  `04-cache-group1`, `05-virtual-memory-group2`, `06-multiprocessor-part1-group` (group number
  unknown), `06-multiprocessor-part2-group4` (group presentations, reviewed by the lecturer).
- `lecture-notes/` — topic notes → `main.pdf`. `preamble.tex` (styling, macros, cover, citation
  macros, `valu` ALU pic, `\diagramsource`), `colored-boxes.tex`, `assets/text_logo_3.png`,
  `assets/figures/` (images used in the notes). Sections: 01 introduction, 02
  instruction-set-architecture (incl. MIPS), 03 pipelining (incl. hazards), 04 cache,
  05 virtual-memory, 06 multiprocessors, 07 practice-problems, 08 summary.
- `reviews/final_exam_review/` — `final-exam-review.tex` (+ `sections/`): recap, traps, the
  lecturer's review questions solved, exam-style questions with solutions. Loads
  `../../lecture-notes/preamble`.
- `cheat-sheet/final-cheat-sheet.tex` — standalone, exactly **4 pages** at 10pt, 3 columns;
  page 4 = full-width worked traces (lecturer's pipeline problem, replacement, coherence,
  encodings).
- `references/` — H&P textbook PDF, MIPS reference card (+ readable version).
- `templates/lecture-notes-template/` — blank copy of the notes template (placeholder course
  info, sample section showing every convention).
- `tools/` — helper scripts (see below).
- The template came from the sibling course `../coc5173-data-engineering` (same conventions).

## Build

```bash
cd lecture-notes && xelatex main.tex && xelatex main.tex
cd reviews/final_exam_review && xelatex final-exam-review.tex && xelatex final-exam-review.tex
cd cheat-sheet && xelatex final-cheat-sheet.tex
```

A build is done only with no `!` errors, no `Overfull \hbox`, no undefined references and no
`Missing character`: `grep -E "^!|Overfull|undefined|Missing character" main.log`.
Remove `*.aux *.log *.out *.toc` afterwards.

`\usepackage{array}[=2024-06-01]` is pinned in the preamble and the cheat sheet: the
`array.sty` in `~/Library/texmf` needs a newer LaTeX kernel; without the pin every `tabular`
fails with `Undefined control sequence \vcenter@text`. Do not remove it.

## Textbook (H&P, Computer Architecture: A Quantitative Approach, 5th ed.)

- PDF page = printed page + 29 for chapters; appendix page X-n = n + offset:
  A 523, B 579, C 647, D 736, E 804, F 831, G 949, H 984, I 1029, J 1076, K 1150.
- Macros (footnotes with book page and PDF page): `\HP{\S1.9}{46}`, `\HP[48]{loc}{46}` (range),
  `\HPA{B}{\S B.3}{23}` (page B-23), `\hppage{}{46}`, `\hppages{C}{11}{27}`.
- Topic mapping: intro Ch.1; ISA App.A; pipelining App.C (+ §3.1 dependences); cache App.B
  §B.1–B.3 + §2.2; VM §B.4–B.5 + §2.4; multiprocessors Ch.3 (ILP, multithreading §3.12),
  Ch.5 (§5.1–5.6), App.I (barriers).
- **Check every page in the extracted text before citing; never guess.** Use `tools/hpfind.py`.
- Known textbook slips noted in the notes: p. B-16 (penalty 100 vs 200), p. 80 (1.38 should be
  1.57; 4-way mixes units). The 5th ed. die-yield model is `1/(1+D·A)^N`, not the slides' α=4 one.

## Content conventions

- Organize by **topic**, not lecture date; merge group slides into topics. Concise summary style:
  bullets, definitions, short explanations, worked examples.
- Group slides are **reviewed, not trusted**: verify against H&P. Mark slide errors with
  `\begin{remark}\slidefix{} ...\end{remark}`, added material with `\beyond{}`; each section
  starts with `\sources{...}`.
- **Re-derive every number with a script** before writing it (encodings, branch offsets,
  pipeline timings, cache/page replacement traces, AMAT, Amdahl). Slides have had wrong answers
  (e.g. Group 4's H&P 5.4 ignores the Fig. 5.35 initial state; their 3.14 counts latency−1 stalls).
- **Textbook exercises** end each topic in `\subsection{Textbook Exercises}` as
  `\begin{tbexercise}[appendix letter]{number}{page}{theory pointer}`. Restate the exercise
  (include any figure data needed); cite the exercise page and the pages with the theory.
  **No solutions are written** (owner's choice; the book has none).
- Keep `07-practice-problems` and `08-summary` in sync with the topics.
- Pipeline diagram convention: register write in the first half, read in the second half; a
  stalled instruction waits in ID (stall after ID), the one behind waits in IF.
- Use ASCII for Vietnamese names (Latin Modern lacks the glyphs).

## Diagrams

- **Black and white only** (owner's request): black lines, `black!NN` grey fills; meaning by
  line style: solid = hazard/forwarding/allowed, dashed = through register file / fix / link.
  Exception still in place: diagrams 1 and 52 use the template's navy concept-box style.
- Every diagram sits in `\begin{center}\begin{minipage}{\linewidth}\centering ... \diagramsource{...}\end{minipage}\end{center}`
  (the minipage keeps the note on the same page). `\diagramsource{}` numbers it ("Diagram N")
  and names the slide file, slide number and title, the matching H&P figure (book + PDF page),
  or says "own diagram" / "image supplied by the note-taker". The owner reviews diagrams by these numbers.
- Text placement must be checked: no label on a line, arrow or box edge; arrows routed in the gaps
  between cells. After any diagram change, render it alone and look at it (build a one-diagram-per-page
  PDF with the notes preamble, `pdftoppm -r 70`), and compare with the source slide.
- Images: `lecture-notes/assets/figures/` (Moore's law: OWID, CC BY; power density: Qian, NoC
  thesis Fig. 1.3; `diag-N.png` supplied by the owner for diagrams 6, 21, 36, 43, 46).
- The vetted redraws are generated by `tools/redraw.py` (re-apply it when editing those diagrams).
- New TikZ: reuse `valu` (vertical ALU: inputs at (x±0.65,y), output at (x,y−1)), `tnode`, `box`,
  `concept`. Never name a style `in` or `out`.

## Tools (`tools/`)

- `hpfind.py "regex" ...` — PDF and printed page of H&P text matches (extracts `.hp.txt` once).
- `slfind.py slides/<deck>.pdf "kw1&kw2"` — slide number and title of matching slides.
- `pipe.py` — pipeline timing simulator (no forwarding / forwarding) and LaTeX grid output.
- `redraw.py` — bodies of the redrawn diagrams (`B[n]`) and their source notes (`SRC[n]`).

## Owner preferences

- Cleanups and destructive changes only when asked; back up sources before deleting.
- Answers go into the documents, not long chat explanations; report what changed and what to check.
- Slide naming `NN-topic-source.pdf`; folder names lower-case with hyphens (reviews use underscores).
