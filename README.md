# CO5059 – Advanced System Architectures (Semester 261)

Study materials for the course: slides, topic notes enriched with the textbook, the final
exam review and the final cheat sheet.

```
slides/          Slides, named NN-topic-source.pdf (NN = topic number)
                   01-introduction-lecture, 02-isa-lecture, 03-pipelining-lecture,
                   04-cache-lecture, 04-cache-group1, 05-virtual-memory-lecture,
                   05-virtual-memory-group2, 06-multiprocessor-part1-group,
                   06-multiprocessor-part2-group4
lecture-notes/   Topic notes (not a lecture log), one document → main.pdf
  main.tex         entry point (cover, contents, \input of each section)
  preamble.tex     styling, macros, cover, textbook-citation macros (same template as CO5173)
  colored-boxes.tex  coloured definition / theorem / example / exercise boxes
  assets/          text_logo_3.png (HCMUT logo, cover)
    figures/       images used in the notes (sources in the note under each figure)
  sections/        01-introduction, 02-instruction-set-architecture, 03-pipelining,
                   04-cache, 05-virtual-memory, 06-multiprocessors,
                   07-practice-problems, 08-summary
reviews/final_exam_review/
                 Final exam review → final-exam-review.pdf (recap, traps, the lecturer's
                 review questions solved, exam-style questions with solutions), one file per
                 topic in sections/; Review_final_2026.pdf = the lecturer's review slides
cheat-sheet/     final-cheat-sheet.tex → 4 pages (2 A4 sheets, double-sided)
references/      Textbook (H&P 5th ed.) and the MIPS reference sheet (original + readable)
tools/           helper scripts: H&P page finder, slide finder, pipeline simulator, diagram generator
CLAUDE.md        project context and conventions for Claude Code
templates/lecture-notes-template/
                 Blank copy of the notes template (preamble with placeholder course
                 info, colored-boxes, logo, sample section showing each convention)
```

Topic order: introduction, ISA, pipelining (lectures 1–3, taught by the lecturer); cache,
virtual memory, multiprocessors (group presentations reviewed by the lecturer).

## Building

All documents use XeLaTeX (except `references/mips-reference-readable.tex`, pdfLaTeX).
Run twice for the contents and cross-references:

```bash
cd lecture-notes && xelatex main.tex && xelatex main.tex
cd reviews/final_exam_review && xelatex final-exam-review.tex && xelatex final-exam-review.tex
cd cheat-sheet && xelatex final-cheat-sheet.tex
```

`preamble.tex` and the cheat sheet load `\usepackage{array}[=2024-06-01]`: the `array.sty` in
`~/Library/texmf` needs a newer LaTeX kernel than the one installed, and without the pin
every `tabular` fails with `Undefined control sequence \vcenter@text`.

A build is clean only with no `!` errors, `Overfull \hbox`, undefined references or
`Missing character` in the log.

## Conventions

- Sections follow topics; group presentations are merged into their topic and checked
  against the textbook.
- `\sources{}` under each section heading lists the slides and textbook chapters used.
- Textbook citations are footnotes with the book page and the PDF page of
  `references/Computer Architecture - A Quantitative Approach.pdf`:
  `\HP{§1.9}{46}` (chapters: PDF = page + 29), `\HPA{B}{§B.3}{23}` (appendix page B-23).
- Every diagram carries a numbered `\diagramsource{}` note under it: the slide file, slide
  number and title it was redrawn from, and the matching H&P figure (book and PDF page) where
  one exists; own diagrams and approximate redraws say so.
- `\slidefix{}` in a `remark` marks a corrected slide error; `\beyond{}` marks material added
  from the textbook.
- Each topic ends with **Textbook Exercises**: `\begin{tbexercise}[appendix]{number}{page}{theory}`
  restates an H&P exercise and cites its page and the pages with the theory needed. No
  solutions are written (the book has none).
- Every number in worked examples and solutions was recomputed by a script.
