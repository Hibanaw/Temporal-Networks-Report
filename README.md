# Temporal Networks report

`main.tex` and `main.pdf` are the manuscript source and compiled report.
`b_report.tex` / `b_report.pdf` retain the detailed citation-network companion.

This revision integrates measured A--E results, the H1--H7 cross-network table,
and observation/null-count sensitivity. See [SUPPLEMENT_NOTES.md](SUPPLEMENT_NOTES.md)
for definitions, limitations and the reproducible generation workflow.

The experiment source and result tables are in
[Hibanaw/Temporal-Networks](https://github.com/Hibanaw/Temporal-Networks/tree/supplement-experiments).
This GitHub repository is the report delivery target; no Overleaf direct-Git
connection is required to review or build it.

Compile from this directory:

```sh
mkdir -p build
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
BIBINPUTS=.: BSTINPUTS=.: bibtex build/main
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

`report_sources.zip` bundles source files and figures. Draft expectation/outline
macros are disabled. Table values are regenerated from measured CSV files;
missing and inapplicable results are never replaced with expected values.
