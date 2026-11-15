"""Generator for the redrawn lecture-note diagrams (B[n] = TikZ body of Diagram n,
SRC[n] = new source note). Apply by replacing the body between
\\begin{minipage}{\\linewidth}\\centering and \\diagramsource{ of the n-th diagram."""
"""New bodies for the diagrams being redrawn (black and white)."""
import math

B = {}      # diagram number -> new body (inside the minipage, before \diagramsource)
SRC = {}    # diagram number -> new source note (only where it changes)

# ---------------------------------------------------------------- helpers
def pipeline(rows, header=None, arrows=(), P=1.25, W=1.05, H=0.55, R=0.85,
             label_w=None, extra=""):
    """rows: list of (label, start_col, [stage,...]); stage may be
    'Reg>' (read: right half shaded), 'Reg<' (write: left half shaded),
    'bubble', or None (empty cell).
    arrows: (r1, gapcol, r2, tcol, style) -- start under row r1 in the gap
    right of column gapcol, run down that gap, end on top of (r2, tcol)."""
    out = [r"\begin{tikzpicture}[font=\scriptsize]"]
    x0 = lambda c: (c - 1) * P
    yc = lambda r: -r * R
    gap = lambda c: x0(c) + W + (P - W) / 2
    if header:
        out.append(r"  \node[anchor=east,font=\scriptsize\itshape] at (-0.15,%.2f) {%s};" % (R * 0.75, header[0]))
        for c in range(1, header[1] + 1):
            out.append(r"  \node at (%.3f,%.2f) {%d};" % (x0(c) + W / 2, R * 0.75, c))
    for r, (lab, start, stages) in enumerate(rows):
        out.append(r"  \node[anchor=east] at (-0.15,%.3f) {%s};" % (yc(r), lab))
        for k, st in enumerate(stages):
            if st is None:
                continue
            c = start + k
            xa, xb = x0(c), x0(c) + W
            ya, yb = yc(r) - H / 2, yc(r) + H / 2
            if st == 'bubble':
                out.append(r"  \draw[dashed,rounded corners=4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"
                           % (xa + 0.05, ya + 0.04, xb - 0.05, yb - 0.04))
                out.append(r"  \node[font=\tiny\itshape] at (%.3f,%.3f) {bubble};" % ((xa + xb) / 2, yc(r)))
                continue
            if st in ('Reg>', 'Reg<'):
                xm = (xa + xb) / 2
                if st == 'Reg>':
                    out.append(r"  \fill[black!25] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xm, ya, xb, yb))
                else:
                    out.append(r"  \fill[black!25] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xa, ya, xm, yb))
                st = 'Reg'
            bold = st.startswith('*')
            st = st.lstrip('*')
            out.append(r"  \draw%s (%.3f,%.3f) rectangle (%.3f,%.3f);" % ("[very thick]" if bold else "", xa, ya, xb, yb))
            out.append(r"  \node at (%.3f,%.3f) {%s};" % ((xa + xb) / 2, yc(r), st))
    for (r1, gc, r2, tc, style) in arrows:
        sx, sy = gap(gc), yc(r1) - H / 2
        tx, ty = x0(tc) + W / 2, yc(r2) + H / 2
        if r2 == r1 + 1:
            out.append(r"  \draw[-{Latex[length=2mm]},thick,%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (style, sx, sy, tx, ty))
        else:
            ky = yc(r2) + H / 2 + (R - H) / 2
            out.append(r"  \draw[-{Latex[length=2mm]},thick,%s] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);"
                       % (style, sx, sy, sx, ky, tx, ty))
    out.append(extra)
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)

STG = ['Ifetch', 'Reg', 'ALU', 'DMem', 'Reg']

# ---------------------------------------------------------------- 2 levels of abstraction
B[2] = r"""
\begin{tikzpicture}[x=1cm,y=0.62cm,font=\small]
  % software (above the ISA)
  \draw (0,1) rectangle (10,4.6);
  \node[anchor=north west] at (0.1,4.55) {Applications};
  \draw (3.4,1) rectangle (10,3.5);
  \node[anchor=north] at (6.7,3.45) {Operating System};
  \draw (4.0,1) rectangle (6.6,2.1) node[midway] {Compiler};
  \draw (7.0,1) rectangle (9.6,2.1) node[midway] {Firmware};
  % the interface
  \draw[fill=black!12,thick] (-0.4,0.25) rectangle (10.4,1) node[midway] {\bfseries Instruction Set Architecture};
  % hardware (below the ISA)
  \draw (0.4,-0.6) rectangle (6.4,0.25) node[midway] {Instruction Set Processor};
  \draw (6.4,-0.6) rectangle (9.6,0.25) node[midway] {I/O System};
  \draw (1.0,-1.45) rectangle (9.0,-0.6) node[midway] {Datapath \& Control};
  \draw (1.6,-2.3) rectangle (8.4,-1.45) node[midway] {Digital Design};
  \draw (2.2,-3.15) rectangle (7.8,-2.3) node[midway] {Circuit Design};
  \draw (2.8,-4.0) rectangle (7.2,-3.15) node[midway] {Layout};
  % side labels
  \draw[-{Latex[length=2.5mm]},thick] (-0.9,1.05) -- (-0.9,4.6)
    node[midway,rotate=90,above] {Software};
  \draw[-{Latex[length=2.5mm]},thick] (-0.9,0.2) -- (-0.9,-4.0)
    node[midway,rotate=90,above] {Hardware};
\end{tikzpicture}"""

# ---------------------------------------------------------------- 5 design cycle
B[5] = r"""
\begin{tikzpicture}[font=\small]
  \def\r{1.35}
  \draw[very thick,-{Latex[length=3mm]}] (15:\r) arc[start angle=15,end angle=-75,radius=\r];
  \draw[very thick,-{Latex[length=3mm]}] (-105:\r) arc[start angle=-105,end angle=-195,radius=\r];
  \draw[very thick,-{Latex[length=3mm]}] (135:\r) arc[start angle=135,end angle=45,radius=\r];
  \node[align=center,font=\small\bfseries] at (0,0) {Performance,\\Technology\\and Cost};
  \node[anchor=south west,align=left,font=\scriptsize] at (30:1.55)
    {\textbf{1 Performance}\\evaluate existing systems\\for bottlenecks\\\emph{using benchmarks}};
  \node[anchor=north,align=center,font=\scriptsize] at (-90:1.55)
    {\textbf{2 Technology}\\simulate new designs and organizations\\\emph{using workloads}};
  \node[anchor=south east,align=right,font=\scriptsize] at (150:1.55)
    {\textbf{3 Cost}\\implement the next-generation\\system\\\emph{implementation complexity}};
\end{tikzpicture}"""

# ---------------------------------------------------------------- 6 image
B[6] = r"""
\includegraphics[width=0.95\linewidth]{assets/figures/diag-6.png}"""
SRC[6] = r"""image supplied by the note-taker (a cost-to-price figure from an earlier edition of H\&P; not in the 5th ed.); the same cost components as \nolinkurl{01-introduction-lecture.pdf}, slide 46 (``Price vs.\ Cost'')"""

# ---------------------------------------------------------------- 7 wafers
def wafer(cx, d, off, defects, r=1.6):
    lines = [r"  \begin{scope}[shift={(%.2f,0)}]" % cx,
             r"  \fill[black!12] (0,0) circle (%.2f);" % r]
    n = good = 0
    k0 = -int(math.ceil(r / d)) - 1
    for i in range(k0, -k0 + 1):
        for j in range(k0, -k0 + 1):
            xa, ya = off + i * d, off + j * d
            cs = [(xa, ya), (xa + d, ya), (xa, ya + d), (xa + d, ya + d)]
            if all(math.hypot(x, y) <= r for x, y in cs):
                n += 1
                bad = any(xa < px < xa + d and ya < py < ya + d for px, py in defects)
                good += not bad
                lines.append(r"  \draw[fill=%s] (%.3f,%.3f) rectangle ++(%.3f,%.3f);"
                             % ("black!45" if bad else "white", xa, ya, d, d))
    lines.append(r"  \draw[thick] (0,0) circle (%.2f);" % r)
    for px, py in defects:
        lines.append(r"  \fill (%.3f,%.3f) circle (1.6pt);" % (px, py))
    lines.append(r"  \end{scope}")
    return "\n".join(lines), n, good

DEF = [(-0.95, 0.75), (0.35, 1.05), (1.05, -0.3), (-0.3, -1.1), (0.15, 0.25)]
wa, na, _ = wafer(0, 0.9, 0.0, [])
wb, nb, _ = wafer(3.9, 0.9, -0.45, [])
wc, nc, gc = wafer(7.8, 0.9, -0.45, DEF)
wd, nd, gd = wafer(11.7, 0.45, -0.225, DEF)
B[7] = r"""
\begin{tikzpicture}[font=\scriptsize,scale=0.86,every node/.style={scale=0.86}]
%s
%s
%s
%s
  \node[align=center] at (0,-2.15) {large dies,\\grid through the centre:\\%d whole dies};
  \node[align=center] at (3.9,-2.15) {same dies,\\grid shifted:\\%d whole dies};
  \node[align=center] at (7.8,-2.15) {large dies with\\5 defects:\\%d of %d good};
  \node[align=center] at (11.7,-2.15) {small dies,\\same defects:\\%d of %d good};
  \draw[fill=black!12] (2.0,-3.35) rectangle ++(0.3,0.3); \node[anchor=west] at (2.35,-3.2) {wafer edge (wasted)};
  \draw[fill=black!45] (5.6,-3.35) rectangle ++(0.3,0.3); \node[anchor=west] at (5.95,-3.2) {die hit by a defect};
  \fill (9.25,-3.2) circle (1.6pt); \node[anchor=west] at (9.4,-3.2) {defect};
\end{tikzpicture}""" % (wa, wb, wc, wd, na, nb, gc, nc, gd, nd)

# ---------------------------------------------------------------- 8 metrics
B[8] = r"""
\begin{tikzpicture}[font=\small]
  \draw (-0.4,4) -- (5.4,4) -- (3.8,1.8) -- (1.2,1.8) -- cycle;
  \node[align=center] at (2.5,2.95) {Application\\Programming Language\\Compiler};
  \draw[-{Latex}] (5.11,3.6) -- (6,3.6);
  \node[anchor=west,align=left] at (6.05,3.6) {Answers per month\\Operations per second};
  \draw[-{Latex}] (4.09,2.2) -- (6,2.2);
  \node[anchor=west,align=left] at (6.05,2.2) {\textbf{MIPS}: millions of instructions per second\\\textbf{MFLOPS}: millions of FP operations per second};
  \node[draw,thick,minimum width=4.2cm,minimum height=0.55cm] at (2.5,1.25) {Instruction Set Architecture};
  \draw (1.4,0.7) -- (3.6,0.7) -- (5,-2) -- (0,-2) -- cycle;
  \node[align=center,font=\footnotesize] at (2.5,-0.75) {Datapath, Control\\Function Units\\Transistors\\Pins/Wire--I/O};
  \draw[-{Latex}] (3.86,0.2) -- (6,0.2);
  \node[anchor=west] at (6.05,0.2) {Megabytes per second};
  \draw[-{Latex}] (4.59,-1.2) -- (6,-1.2);
  \node[anchor=west] at (6.05,-1.2) {Cycles per second (clock rate)};
\end{tikzpicture}"""

# ---------------------------------------------------------------- 9 Amdahl
B[9] = r"""
\begin{tikzpicture}[font=\small,x=1.15cm]
  \node[anchor=east] at (-0.15,0.35) {\textbf{Before}};
  \draw (0,0) rectangle (4.95,0.7) node[midway] {Unaffected fraction: $1-F$};
  \draw[fill=black!15] (4.95,0) rectangle (9,0.7) node[midway] {Affected fraction: $F$};
  \node[anchor=east] at (-0.15,-1.55) {\textbf{After}};
  \draw (0,-1.9) rectangle (4.95,-1.2) node[midway] {Unaffected fraction: $1-F$};
  \draw[fill=black!15] (4.95,-1.9) rectangle (6.3,-1.2) node[midway] {$F/S$};
  \draw[dashed,-{Latex}] (0.15,-0.05) -- (0.15,-1.15);
  \draw[dashed,-{Latex}] (4.8,-0.05) -- (4.8,-1.15);
  \node[font=\footnotesize\itshape] at (2.475,-0.6) {unchanged};
  \draw[dashed,-{Latex}] (9,-0.05) -- (6.35,-1.15);
  \node[font=\footnotesize\itshape,anchor=west] at (7.75,-0.75) {sped up by $S$};
  \node[font=\footnotesize] at (4.5,-2.35) {(old time normalized to $1=(1-F)+F$; drawn with $F=0.45$, $S=3$)};
\end{tikzpicture}"""

# ---------------------------------------------------------------- 14-18 ISA styles
B[14] = r"""
\begin{tikzpicture}[font=\small]
  \draw (-1.3,0.5) rectangle (1.3,1.0) node[midway] {Stack Element};
  \draw (-1.3,0) rectangle (1.3,0.5) node[midway] {Stack Element};
  \node[draw] (tos) at (-2.6,0.75) {TOS};
  \draw[-{Latex}] (tos) -- (-1.3,0.75);
  \pic at (0,-0.6) {valu};
  \draw[-{Latex}] (-0.65,0) -- (-0.65,-0.6);
  \draw[-{Latex}] (1.3,0.75) -- (1.8,0.75) |- (0.65,-0.3) -- (0.65,-0.6);
  \draw[-{Latex}] (0,-1.6) -- (0,-1.95) -| (2.4,1.35) -| (0.65,1.0);
  \node[anchor=west,font=\footnotesize] at (2.7,0.2) {operands: the top two elements};
  \node[anchor=west,font=\footnotesize] at (2.7,-0.3) {result: pushed back on the stack};
\end{tikzpicture}"""

B[15] = r"""
\begin{tikzpicture}[font=\small]
  \draw (-1.1,0.75) rectangle (1.1,1.25) node[midway] {Accumulator};
  \draw (2.4,-0.6) rectangle (4.2,1.4);
  \foreach \y in {-0.1,0.4,0.9} \draw (2.4,\y) -- (4.2,\y);
  \node[fill=white,inner sep=1pt] at (3.3,0.65) {Memory};
  \pic at (0,0) {valu};
  \draw[-{Latex}] (-0.65,0.75) -- (-0.65,0);
  \draw[-{Latex}] (2.4,0.15) -| (0.65,0);
  \draw[-{Latex}] (0,-1) -- (0,-1.3) -| (-1.7,1) -- (-1.1,1);
\end{tikzpicture}"""

B[16] = r"""
\begin{tikzpicture}[font=\small]
  \draw (2.2,-1.6) rectangle (4.0,1.0);
  \foreach \y in {-1.1,-0.6,-0.1,0.4} \draw (2.2,\y) -- (4.0,\y);
  \node[fill=white,inner sep=1pt] at (3.1,-0.35) {Memory};
  \pic at (0,0) {valu};
  \draw[-{Latex}] (2.2,0.7) -| (-0.65,0);
  \draw[-{Latex}] (2.2,0.15) -| (0.65,0);
  \draw[-{Latex}] (0,-1) -- (0,-1.35) -- (2.2,-1.35);
\end{tikzpicture}"""

REGS = r"""
  \draw (-1.1,1.2) rectangle (1.1,1.6) node[midway] {Register};
  \draw (-1.1,0.8) rectangle (1.1,1.2) node[midway] {Register};
  \draw (-1.1,0.4) rectangle (1.1,0.8) node[midway] {Register};
  \pic at (0,0) {valu};"""
B[17] = r"""
\begin{tikzpicture}[font=\small]""" + REGS + r"""
  \draw (2.4,-1.0) rectangle (4.2,1.4);
  \foreach \y in {-0.5,0.0,0.5} \draw (2.4,\y) -- (4.2,\y);
  \node[fill=white,inner sep=1pt] at (3.3,0.25) {Memory};
  \draw[-{Latex}] (-0.65,0.4) -- (-0.65,0);
  \draw[-{Latex}] (2.4,0.2) -| (0.65,0);
  \draw[-{Latex}] (0,-1) -- (0,-1.3) -| (-1.7,1.4) -- (-1.1,1.4);
\end{tikzpicture}"""

B[18] = r"""
\begin{tikzpicture}[font=\small]""" + REGS + r"""
  \draw[-{Latex}] (-0.65,0.4) -- (-0.65,0);
  \draw[-{Latex}] (0.65,0.4) -- (0.65,0);
  \draw[-{Latex}] (0,-1) -- (0,-1.3) -| (-1.7,1.4) -- (-1.1,1.4);
\end{tikzpicture}"""

# ---------------------------------------------------------------- 20 addressing-mode use
cats = [("Memory indirect", (1, 6, 1)), ("Scaled", (0, 16, 6)), ("Register deferred", (24, 3, 11)),
        ("Immediate", (43, 17, 39)), ("Displacement", (32, 55, 40))]
L = [r"\begin{tikzpicture}[font=\scriptsize]"]
fills = ["white", "black!35", "black"]
progs = ["TeX", "spice", "gcc"]
for g, (name, vals) in enumerate(cats):
    base = -g * 1.15
    L.append(r"  \node[anchor=east] at (-0.85,%.3f) {%s};" % (base - 0.3, name))
    for k, v in enumerate(vals):
        y = base - k * 0.3
        L.append(r"  \node[anchor=east,font=\tiny] at (-0.08,%.3f) {%s};" % (y, progs[k]))
        if v:
            L.append(r"  \draw[fill=%s] (0,%.3f) rectangle (%.2f,%.3f);" % (fills[k], y - 0.12, v * 0.1, y + 0.12))
        L.append(r"  \node[anchor=west,font=\tiny] at (%.2f,%.3f) {%d\%%};" % (v * 0.1 + 0.05, y, v))
L.append(r"  \draw (0,0.25) -- (0,-5.45) -- (6.1,-5.45);")
for t in range(0, 61, 10):
    L.append(r"  \draw (%.1f,-5.45) -- (%.1f,-5.52) node[below,font=\tiny] {%d\%%};" % (t / 10, t / 10, t))
L.append(r"  \node at (3,-6.05) {Frequency of the addressing mode};")
L.append(r"\end{tikzpicture}")
B[20] = "\n" + "\n".join(L)

# ---------------------------------------------------------------- 21 image
B[21] = r"""
\includegraphics[width=0.8\linewidth]{assets/figures/diag-21.png}"""
SRC[21] = r"""H\&P Fig.~A.8, \hppage{A}{12} (image supplied by the note-taker); the same chart as \nolinkurl{02-isa-lecture.pdf}, slide 26 (``Addressing mode'')"""

# ---------------------------------------------------------------- 25 endianness
def endian(little):
    L = []
    for i, b in enumerate(["0A", "0B", "0C", "0D"]):
        L.append(r"  \draw (%.2f,0) rectangle ++(0.7,0.5) node[midway] {\texttt{%s}};" % (1.0 + 0.7 * i, b))
    L.append(r"  \node at (2.4,0.75) {Register};")
    mx0, mx1 = (4.6, 5.4) if little else (-0.8, 0.0)
    for i in range(4):
        yc = -0.8 - 0.55 * i
        byte = (3 - i) if little else i
        content = ["0A", "0B", "0C", "0D"][byte]
        L.append(r"  \draw (%.2f,%.3f) rectangle (%.2f,%.3f) node[midway] {\texttt{%s}};" % (mx0, yc - 0.25, mx1, yc + 0.25, content))
        lab = "$a$" if i == 0 else "$a+%d$" % i
        if little:
            L.append(r"  \node[anchor=west] at (%.2f,%.3f) {%s};" % (mx1 + 0.08, yc, lab))
        else:
            L.append(r"  \node[anchor=east] at (%.2f,%.3f) {%s};" % (mx0 - 0.08, yc, lab))
        xs = 1.35 + 0.7 * byte
        end = mx0 if little else mx1
        L.append(r"  \draw[-{Latex[length=2mm]}] (%.2f,0) |- (%.2f,%.3f);" % (xs, end, yc))
    L.append(r"  \node at (%.2f,-1.95) {Memory};" % ((mx0 + mx1) / 2 if False else (mx0 + mx1) / 2))
    L.append(r"  \node[font=\small\bfseries] at (2.4,-3.0) {%s};" % ("Little-endian" if little else "Big-endian"))
    return "\n".join(L)
B[25] = r"""
\begin{tikzpicture}[font=\scriptsize]
%s
  \begin{scope}[xshift=7.2cm]
%s
  \end{scope}
\end{tikzpicture}""" % (endian(False).replace(r"\node at (-0.40,-1.95) {Memory};", r"\node at (-0.40,-2.95) {Memory};"),
                        endian(True).replace(r"\node at (5.00,-1.95) {Memory};", r"\node at (5.00,-2.95) {Memory};"))

# ---------------------------------------------------------------- 30 laundry (label fix + grey)
B[30] = r"""
\begin{tikzpicture}[x=0.95cm,y=-0.9cm,font=\scriptsize]
  \draw[-{Stealth}] (0,-0.6) -- (12.4,-0.6) node[right] {time (hours)};
  \foreach \t/\lab in {0/6PM,1.5/7,3.5/8,5.5/9,7.5/10,9.5/11,11.5/Midnight}
    \node at (\t,-1.0) {\lab};
  \foreach \task/\row in {A/0,B/1,C/2,D/3}{
    \pgfmathsetmacro{\xoff}{\row*3}
    \node[left] at (-0.3,\row) {\task};
    \draw[fill=white]    (\xoff,\row-0.35) rectangle ++(1,0.7) node[midway]{Wash};
    \draw[fill=black!12] (\xoff+1,\row-0.35) rectangle ++(1.33,0.7) node[midway]{Dry};
    \draw[fill=black!28] (\xoff+2.33,\row-0.35) rectangle ++(0.67,0.7) node[midway]{Fold};
  }
\end{tikzpicture}"""

# ---------------------------------------------------------------- 33/34 single-cycle vs pipelined (to scale)
def timing(pipelined):
    u = 0.51
    L = [r"\begin{tikzpicture}[x=%.2fcm,y=1cm,font=\scriptsize]" % u]
    T = 14 if pipelined else 24
    L.append(r"  \draw[-{Stealth}] (0,0.6) -- (%.1f,0.6) node[right] {ns};" % (T + 0.6))
    for t in range(0, T + 1, 2):
        L.append(r"  \draw (%d,0.55) -- (%d,0.65) node[above,font=\tiny] {%d};" % (t, t, t))
    labs = [r"\texttt{lw \$1,100(\$0)}", r"\texttt{lw \$2,200(\$0)}", r"\texttt{lw \$3,300(\$0)}"]
    for i in range(3):
        y = -1.1 * i
        t0 = 2 * i if pipelined else 8 * i
        L.append(r"  \node[anchor=east] at (-0.3,%.2f) {%s};" % (y, labs[i]))
        if pipelined:
            segs = [(0, 2, "Fetch"), (3, 4, "Reg"), (4, 6, "ALU"), (6, 8, "Data"), (8, 9, "Reg")]
        else:
            segs = [(0, 2, "Fetch"), (2, 3, "Reg"), (3, 5, "ALU"), (5, 7, "Data"), (7, 8, "Reg")]
        for a, b, n in segs:
            f = r"\tiny" if b - a == 1 else ""
            L.append(r"  \draw (%d,%.3f) rectangle (%d,%.3f) node[midway,font=%s] {%s};"
                     % (t0 + a, y - 0.27, t0 + b, y + 0.27, f if f else r"\scriptsize", n))
        if not pipelined:
            L.append(r"  \draw[{Latex[length=1.5mm]}-{Latex[length=1.5mm]}] (%d,%.2f) -- (%d,%.2f) node[midway,below,font=\tiny] {8 ns};"
                     % (t0, y - 0.38, t0 + 8, y - 0.38))
    if pipelined:
        for i in range(2):
            y = -1.1 * i
            L.append(r"  \draw[{Latex[length=1.5mm]}-{Latex[length=1.5mm]}] (%d,%.2f) -- (%d,%.2f) node[midway,below,font=\tiny] {2 ns};"
                     % (2 * i, y - 0.38, 2 * i + 2, y - 0.38))
        L.append(r"  \node[anchor=west,font=\scriptsize] at (0,-2.75) {registers are written in the first half and read in the second half of a 2 ns slot};")
    L.append(r"\end{tikzpicture}")
    return "\n" + "\n".join(L)
B[33] = timing(False)
B[34] = timing(True)

# ---------------------------------------------------------------- 36, 43, 46 images
B[36] = r"""
\includegraphics[width=\linewidth]{assets/figures/diag-36.png}"""
SRC[36] = r"""H\&P Fig.~C.22, \hppage{C}{35} (image supplied by the note-taker); the same datapath as \nolinkurl{03-pipelining-lecture.pdf}, slide 26 (``5 Steps of MIPS Datapath'')"""
B[43] = r"""
\includegraphics[width=0.7\linewidth]{assets/figures/diag-43.png}"""
SRC[43] = r"""H\&P Fig.~C.27, \hppage{C}{41} (image supplied by the note-taker; dotted lines are the forwarding paths); cf.\ \nolinkurl{03-pipelining-lecture.pdf}, slide 41 (``HW Change for Forwarding'')"""
B[46] = r"""
\includegraphics[width=\linewidth]{assets/figures/diag-46.png}"""
SRC[46] = r"""H\&P Fig.~C.28, \hppage{C}{42} (image supplied by the note-taker; zero test and branch-target adder moved into ID); cf.\ \nolinkurl{03-pipelining-lecture.pdf}, slide 61 (``Pipelined MIPS Datapath'')"""

# ---------------------------------------------------------------- 37 visualizing (half-cycle register use)
B[37] = "\n" + pipeline(
    [("Instr 1", 1, ['Ifetch', 'Reg>', 'ALU', 'DMem', 'Reg<']),
     ("Instr 2", 2, ['Ifetch', 'Reg>', 'ALU', 'DMem', 'Reg<']),
     ("Instr 3", 3, ['Ifetch', 'Reg>', 'ALU', 'DMem', 'Reg<']),
     ("Instr 4", 4, ['Ifetch', 'Reg>', 'ALU', 'DMem', 'Reg<'])],
    header=("cycle", 8),
    extra=r"""  \fill[black!25] (0,-3.25) rectangle ++(0.25,0.25); \draw (0,-3.25) rectangle ++(0.5,0.25);
  \node[anchor=west] at (0.6,-3.125) {Reg in WB: written in the \emph{first} half of the cycle};
  \fill[black!25] (0.25,-3.65) rectangle ++(0.25,0.25); \draw (0,-3.65) rectangle ++(0.5,0.25);
  \node[anchor=west] at (0.6,-3.525) {Reg in ID: read in the \emph{second} half of the cycle};""")

# ---------------------------------------------------------------- 38 structural hazard
B[38] = "\n" + pipeline(
    [("Load", 1, ['Mem', 'Reg', 'ALU', '*DM', 'Reg']),
     ("Instr 1", 2, ['Mem', 'Reg', 'ALU', 'DM', 'Reg']),
     ("Instr 2", 3, ['Mem', 'Reg', 'ALU', 'DM', 'Reg']),
     ("Instr 3", 4, ['*Mem', 'Reg', 'ALU', 'DM', 'Reg']),
     ("Instr 4", 5, ['Mem', 'Reg', 'ALU', 'DM', 'Reg'])],
    header=("cycle", 9),
    extra=r"""  \draw[dashed,rounded corners=6pt] (3.70,0.45) rectangle (4.95,-2.95);
  \node[anchor=north west,font=\scriptsize] at (0,-3.85) {cycle 4: the Load's data access (DM) and Instr 3's instruction fetch (Mem) both need the one memory port};""")

# ---------------------------------------------------------------- 39 stall
B[39] = "\n" + pipeline(
    [("Load", 1, ['Mem', 'Reg', 'ALU', 'DM', 'Reg']),
     ("Instr 1", 2, ['Mem', 'Reg', 'ALU', 'DM', 'Reg']),
     ("Instr 2", 3, ['Mem', 'Reg', 'ALU', 'DM', 'Reg']),
     (r"\emph{stall}", 4, ['bubble'] * 5),
     ("Instr 3", 5, ['Mem', 'Reg', 'ALU', 'DM', 'Reg'])],
    header=("cycle", 9), P=1.2, W=1.0)

# ---------------------------------------------------------------- 40/41 hazard classification panels
def panel(x, title, iop, jop, iw, jw):
    # arrows show data flow: a write goes into the shared operand, a read comes out of it
    L = [r"  \begin{scope}[xshift=%.2fcm]" % x,
         r"  \node[draw,minimum width=1.9cm] (I) at (0,1.3) {$I$ (%s)};" % iop,
         r"  \node[draw,minimum width=1.9cm] (J) at (0,0) {$J$ (%s)};" % jop,
         r"  \node[draw,align=center] (S) at (2.7,0.65) {Shared\\operand};"]
    L.append(r"  \draw[-{Latex}] (I.east) -- (S.north west);" if iw else r"  \draw[-{Latex}] (S.north west) -- (I.east);")
    L.append(r"  \draw[-{Latex}] (J.east) -- (S.south west);" if jw else r"  \draw[-{Latex}] (S.south west) -- (J.east);")
    L.append(r"  \node[font=\small\bfseries,align=center] at (1.35,-0.75) {%s};" % title)
    L.append(r"  \end{scope}")
    return "\n".join(L)
ORDER = r"""  \draw[-{Latex}] (-1.6,1.3) -- (-1.6,0) node[midway,left,font=\scriptsize,align=right] {program\\order};"""
B[40] = r"""
\begin{tikzpicture}[font=\small]
%s
%s
%s
\end{tikzpicture}""" % (ORDER, panel(0, "RAW (true dependence)", "Write", "Read", True, False),
                        panel(6.2, "WAR (name dependence)", "Read", "Write", False, True))
B[41] = r"""
\begin{tikzpicture}[font=\small]
%s
%s
%s
\end{tikzpicture}""" % (ORDER, panel(0, "WAW (name dependence)", "Write", "Write", True, True),
                        panel(6.2, r"RAR (\emph{not} a hazard)", "Read", "Read", False, False))

# ---------------------------------------------------------------- 42 data hazard on r1
HZ = [(r"\texttt{add r1,r2,r3}", 1, STG), (r"\texttt{sub r4,r1,r3}", 2, STG), (r"\texttt{and r6,r1,r7}", 3, STG),
      (r"\texttt{or\ \ r8,r1,r9}", 4, STG), (r"\texttt{xor r10,r1,r11}", 5, STG)]
LEG = r"""  \draw[thick,-{Latex[length=2mm]}] (0,-4.1) -- (0.7,-4.1); \node[anchor=west] at (0.8,-4.1) {%s};
  \draw[thick,dashed,-{Latex[length=2mm]}] (0,-4.5) -- (0.7,-4.5); \node[anchor=west] at (0.8,-4.5) {%s};"""
B[42] = "\n" + pipeline(HZ, header=("cycle", 9),
    arrows=[(0, 4, 1, 3, "solid"), (0, 4, 2, 4, "solid"), (0, 5, 3, 5, "dashed"), (0, 5, 4, 6, "dashed")],
    extra=LEG % ("needed before \\texttt{add} writes \\texttt{r1}: hazard",
                 "read after the write (WB first half): no hazard"))

# ---------------------------------------------------------------- 44 forwarding
B[44] = "\n" + pipeline(HZ, header=("cycle", 9),
    arrows=[(0, 3, 1, 4, "solid"), (0, 4, 2, 5, "solid"), (0, 5, 3, 5, "dashed")],
    extra=LEG % ("forwarded from EX/MEM or MEM/WB to the ALU",
                 "through the register file (write, then read)"))

# ---------------------------------------------------------------- 45 load-use
B[45] = "\n" + pipeline(
    [(r"\texttt{lw\ \ r1,0(r2)}", 1, STG),
     (r"\texttt{sub r4,r1,r6}", 2, ['Ifetch', 'Reg', 'bubble', 'ALU', 'DMem', 'Reg']),
     (r"\texttt{and r6,r1,r7}", 3, ['Ifetch', 'bubble', 'Reg', 'ALU', 'DMem', 'Reg']),
     (r"\texttt{or\ \ r8,r1,r9}", 4, ['bubble', 'Ifetch', 'Reg', 'ALU', 'DMem'])],
    header=("cycle", 9),
    arrows=[(0, 4, 1, 5, "solid"), (0, 5, 2, 5, "dashed")],
    extra=(LEG % ("MEM/WB $\\to$ ALU after a one-cycle stall",
                  "through the register file")).replace("-4.1", "-3.3").replace("-4.5", "-3.7"))

# ---------------------------------------------------------------- 47 placement (set separators)
B[47] = r"""
\begin{tikzpicture}[font=\scriptsize,x=0.42cm,y=0.42cm]
  \node[font=\small\bfseries] at (4,3.2) {Fully associative};
  \fill[black!15] (0,0) rectangle (8,1);
  \foreach \i in {0,...,7} {\draw (\i,0) rectangle ++(1,1); \node at (\i+0.5,-0.5) {\i};}
  \node at (4,2) {block 12: anywhere};
  \node[font=\small\bfseries] at (15,3.2) {2-way set associative};
  \fill[black!15] (11,0) rectangle (13,1);
  \foreach \i in {11,...,18} {\draw (\i,0) rectangle ++(1,1);}
  \foreach \x in {11,13,15,17,19} {\draw[very thick] (\x,-0.15) -- (\x,1.15);}
  \foreach \s/\x in {0/12,1/14,2/16,3/18} {\node at (\x,-0.5) {set \s};}
  \node at (15,2) {block 12: set $12 \bmod 4 = 0$};
  \node[font=\small\bfseries] at (26,3.2) {Direct mapped};
  \fill[black!15] (26,0) rectangle (27,1);
  \foreach \i/\n in {22/0,23/1,24/2,25/3,26/4,27/5,28/6,29/7} {\draw (\i,0) rectangle ++(1,1); \node at (\i+0.5,-0.5) {\n};}
  \node at (26,2) {block 12: $12 \bmod 8 = 4$};
\end{tikzpicture}"""

# ---------------------------------------------------------------- 50 VM pages (labels right, clean routing)
B[50] = r"""
\begin{tikzpicture}[font=\small,x=1cm,y=0.55cm]
  \node[font=\small\bfseries] at (0.6,4.6) {Virtual};
  \foreach \l/\y/\a in {A/3/0,B/2/4K,C/1/8K,D/0/12K} {
    \draw (0,\y) rectangle ++(1.2,1) node[midway] {\l};
    \node[anchor=east,font=\scriptsize] at (-0.1,\y+0.5) {\a};}
  \node[font=\small\bfseries] at (4.6,4.6) {Physical};
  \foreach \y/\a/\l in {3/0/,2/4K/C,1/8K/,0/12K/,-1/16K/A,-2/20K/,-3/24K/B,-4/28K/} {
    \draw (4,\y) rectangle ++(1.2,1) node[midway] {\l};
    \node[anchor=west,font=\scriptsize] at (5.3,\y+0.5) {\a};}
  \draw[fill=black!10] (7,0) rectangle ++(1.4,1) node[midway] {D};
  \node[font=\small\bfseries] at (7.7,4.6) {Disk};
  \draw[-{Latex}] (1.2,3.5) -- (4,-0.5);
  \draw[-{Latex}] (1.2,2.5) -- (4,-2.5);
  \draw[-{Latex}] (1.2,1.5) -- (4,2.5);
  \draw[-{Latex},dashed] (0.6,0) -- (0.6,-5) -- (7.7,-5) -- (7.7,0);
  \node[font=\scriptsize\itshape,fill=white,inner sep=1pt] at (2.6,-5) {page on disk};
\end{tikzpicture}"""

# ---------------------------------------------------------------- 52 concept map (all six topics)
B[52] = r"""
\begin{tikzpicture}[font=\small,
  box/.style={concept,text width=3.3cm,minimum height=1cm}]
  \node[box] (perf) at (0,0) {\textbf{Performance}\\execution time};
  \node[box] (eq) at (5.2,0) {\textbf{CPU equation}\\$I\times\CPI\times C$};
  \node[box] (isa) at (10.4,0) {\textbf{ISA and compiler}\\determine $I$};
  \node[box] (amd) at (0,-2.4) {\textbf{Amdahl's Law}\\limits any speedup};
  \node[box] (pipe) at (5.2,-2.4) {\textbf{Pipelining}\\lowers $\CPI$ toward 1};
  \node[box] (haz) at (10.4,-2.4) {\textbf{Hazards}\\add stall cycles};
  \node[box] (mp) at (0,-4.8) {\textbf{Multiprocessors}\\TLP, coherence, sync};
  \node[box] (cache) at (5.2,-4.8) {\textbf{Cache}\\memory stalls add to $\CPI$};
  \node[box] (vm) at (10.4,-4.8) {\textbf{Virtual memory}\\TLB, page faults};
  \draw[diagram arrow] (eq) -- (perf);
  \draw[diagram arrow] (isa) -- (eq);
  \draw[diagram arrow] (pipe) -- (eq);
  \draw[diagram arrow] (haz) -- (pipe);
  \draw[diagram arrow] (amd) -- (perf);
  \draw[diagram arrow] (isa) -- (pipe);
  \draw[diagram arrow] (cache) -- (pipe);
  \draw[diagram arrow] (vm) -- (cache);
  \draw[diagram arrow] (mp) -- (amd);
  \draw[diagram arrow] (cache) -- (mp);
\end{tikzpicture}"""
