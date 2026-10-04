# CO5059 – Advanced System Architectures (Semester 261)

Study materials for the course: original slides, my lecture notes, quiz reviews and references.

```
slides/          Original lecture slides (PDF)
lecture-notes/   Lecture notes for all lectures, in one document → main.pdf
  main.tex         entry point (cover, contents, \input of each lecture)
  preamble.tex     shared styling, also used by the reviews
  lectures/        one file per lecture (lecture-01.tex, …)
reviews/         Quiz review papers (each folder has its own .tex and .pdf)
  theory_review/       condensed theory for Lectures 1–3 + self-check Q&A
  performance_review/  Lecture 1: cheat sheet, slide/class/exam-style exercises, practice problems
  isa_review/          Lecture 2: cheat sheet, slide/exam-style exercises, practice problems
  pipelining_review/   Lecture 3: cheat sheet, slide/exam-style exercises, practice problems
  */*-textbook-exercises.pdf
                       map of the textbook's exercises for that topic (Ch. 1, App. A, App. C)
                       with page numbers, priorities, worked solutions and hints
references/      Textbook and the MIPS reference sheet (original + readable version)
templates/       Blank lecture-notes template
```

## Building

All documents use XeLaTeX (except `references/mips-reference-readable.tex`, which uses pdfLaTeX).

```bash
cd lecture-notes && xelatex main.tex && xelatex main.tex
```

The reviews load `../../lecture-notes/preamble.tex`, so keep the folder layout as is.
Build them from their own folder the same way, e.g. `cd reviews/isa_review && xelatex isa-review.tex`.

In `reviews/pipelining_review/`, `pipelining-review.tex` and `pipelining-textbook-exercises.tex` are generated: edit the matching `.src.tex`, then run `python3 make_grids.py` to rebuild the aligned pipeline diagrams before compiling.

## Adding a lecture

1. Put the slides in `slides/` (e.g. `L04-….pdf`).
2. Create `lecture-notes/lectures/lecture-04.tex`, starting with `\lecture{4}{Title}{Date}`.
3. Add `\input{lectures/lecture-04}` at the end of `lecture-notes/main.tex`.
