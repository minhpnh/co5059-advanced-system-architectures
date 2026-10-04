"""Expand @@GRID:name@@ markers in the *.src.tex files of this folder into
aligned pipeline diagrams and write the matching .tex files."""
from pathlib import Path

S = ["IF", "ID", "EX", "MEM", "WB"]
W = 6  # characters per cycle column


def stalled(after_id, n):
    """Stages for an instruction that waits n cycles in ID."""
    return ["IF", "ID"] + ["stall"] * n + ["EX", "MEM", "WB"]


def held(n_if, n_id=0):
    """Instruction held n_if cycles in IF (behind a stall), then n_id in ID."""
    return ["IF"] + ["stall"] * n_if + ["ID"] + ["stall"] * n_id + ["EX", "MEM", "WB"]


GRIDS = {
    "raw_nofwd": [
        ("add r1,r2,r3", 1, S),
        ("sub r4,r1,r3", 2, stalled(True, 2)),
        ("and r6,r1,r7", 3, held(2)),
        ("or  r8,r1,r9", 6, S),
        ("xor r10,r1,r11", 7, S),
    ],
    "loaduse": [
        ("lw  r1,0(r2)", 1, S),
        ("sub r4,r1,r6", 2, stalled(True, 1)),
        ("and r6,r1,r7", 3, held(1)),
        ("or  r8,r1,r9", 5, S),
    ],
    "lec_nofwd": [
        ("lw  $1,40($6)", 1, S),
        ("add $6,$2,$2", 2, S),
        ("nop", 3, S),
        ("nop", 4, S),
        ("sw  $6,50($1)", 5, S),
        ("add $4,$5,$6", 6, S),
        ("nop", 7, S),
        ("nop", 8, S),
        ("lw  $6,10($4)", 9, S),
    ],
    "lec_fwd": [
        ("lw  $1,40($6)", 1, S),
        ("add $6,$2,$2", 2, S),
        ("sw  $6,50($1)", 3, S),
        ("add $4,$5,$6", 4, S),
        ("lw  $6,10($4)", 5, S),
    ],
    "p3_nofwd": [
        ("add $t0,$t1,$t2", 1, S),
        ("lw  $t3,0($t0)", 2, stalled(True, 2)),
        ("sub $t4,$t3,$t5", 3, held(2, 2)),
        ("sw  $t4,4($t0)", 6, held(2, 2)),
        ("or  $t6,$t0,$t4", 9, held(2)),
    ],
    "p3_fwd": [
        ("add $t0,$t1,$t2", 1, S),
        ("lw  $t3,0($t0)", 2, S),
        ("sub $t4,$t3,$t5", 3, stalled(True, 1)),
        ("sw  $t4,4($t0)", 4, held(1)),
        ("or  $t6,$t0,$t4", 6, S),
    ],
    "p10": [
        ("lw  $2,20($1)", 1, S),
        ("and $4,$2,$5", 2, stalled(True, 1)),
        ("or  $8,$2,$6", 3, held(1)),
        ("add $9,$4,$2", 5, S),
        ("slt $1,$6,$7", 6, S),
    ],
    "x2_nofwd": [
        ("lw  $s2,0($s1)", 1, S),
        ("add $s3,$s2,$s4", 2, stalled(True, 2)),
        ("sub $s5,$s3,$s2", 3, held(2, 2)),
        ("sw  $s5,4($s1)", 6, held(2, 2)),
        ("add $t0,$s6,$s7", 9, held(2)),
    ],
    "x2_fwd": [
        ("lw  $s2,0($s1)", 1, S),
        ("add $s3,$s2,$s4", 2, stalled(True, 1)),
        ("sub $s5,$s3,$s2", 3, held(1)),
        ("sw  $s5,4($s1)", 5, S),
        ("add $t0,$s6,$s7", 6, S),
    ],
    "x2_sched": [
        ("lw  $s2,0($s1)", 1, S),
        ("add $t0,$s6,$s7", 2, S),
        ("add $s3,$s2,$s4", 3, S),
        ("sub $s5,$s3,$s2", 4, S),
        ("sw  $s5,4($s1)", 5, S),
    ],
    "c1_nofwd": [
        ("LD    R1,0(R2)", 1, S),
        ("DADDI R1,R1,#1", 2, stalled(True, 2)),
        ("SD    R1,0(R2)", 3, held(2, 2)),
        ("DADDI R2,R2,#4", 6, held(2)),
        ("DSUB  R4,R3,R2", 9, stalled(True, 2)),
        ("BNEZ  R4,Loop", 10, held(2, 2)),
        ("LD (next iter.)", 16, ["IF"]),
    ],
    "c1_fwd": [
        ("LD    R1,0(R2)", 1, S),
        ("DADDI R1,R1,#1", 2, stalled(True, 1)),
        ("SD    R1,0(R2)", 3, held(1)),
        ("DADDI R2,R2,#4", 5, S),
        ("DSUB  R4,R3,R2", 6, S),
        ("BNEZ  R4,Loop", 7, stalled(True, 1)),
        ("LD (next iter.)", 10, S),
    ],
}


def render(rows):
    lw = max(len(r[0]) for r in rows) + 2
    last = max(start + len(stages) - 1 for _, start, stages in rows)
    wide = last > 11
    w = (4 if last > 15 else 5) if wide else W
    tok = (lambda t: "stl" if t == "stall" else t) if wide else (lambda t: t)
    out = [" " * lw + "".join(f"c{i}".ljust(w) for i in range(1, last + 1))]
    for label, start, stages in rows:
        line = label.ljust(lw) + " " * (w * (start - 1)) + "".join(tok(s).ljust(w) for s in stages)
        out.append(line.rstrip())
    body = "\n".join(x.rstrip() for x in out)
    size = "\\scriptsize" if wide else "\\footnotesize"
    return ("\\begin{lstlisting}[basicstyle=\\ttfamily" + size + ",keywords={}]\n"
            + body + "\n\\end{lstlisting}")


here = Path(__file__).parent
FILES = ["pipelining-review", "pipelining-textbook-exercises"]
used = set()
for name in FILES:
    src = (here / f"{name}.src.tex").read_text()
    for key, rows in GRIDS.items():
        marker = f"@@GRID:{key}@@"
        if marker in src:
            src = src.replace(marker, render(rows))
            used.add(key)
    assert "@@GRID" not in src, name
    (here / f"{name}.tex").write_text(src)
assert used == set(GRIDS), set(GRIDS) - used
for key in ("c1_nofwd", "c1_fwd"):
    print(render(GRIDS[key]))
