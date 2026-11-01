# Measured experiment supplement

The source/experiment repository is [Hibanaw/Temporal-Networks](https://github.com/Hibanaw/Temporal-Networks), branch `supplement-experiments`.
The experiment protocol, data cards, shared H1--H7 summary, individual realization tables,
robustness comparisons, unit-test log and PBS provenance live there.

This report integrates the delivered E communities and centrality, A's measured PS/CM
window analysis, reconstructed C statistics, corrected D reachability/SIR, and the
cross-network/robustness tables. The C source definitions are explicit; the old PS
lifetime number is superseded by the canonical undirected-dyad result.
The old CM no-spreading interpretation and expected H7 ranking are removed.

Recreate numerical sections and figures from the experiment checkout:

```sh
python scripts/make_summary_table.py
python scripts/summarize_robustness.py
python scripts/plot_supplement.py
python scripts/sync_report_results.py --report ../Temporal-Networks-Report
```

Compile from this directory:

```sh
mkdir -p build
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
BIBINPUTS=.: BSTINPUTS=.: bibtex build/main
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

`main.pdf` is the compiled manuscript. Original B text and its companion are retained.
Half-window results are conditional on their changed node populations and observation
horizons. H7 peak ratios condition on major outbreaks. WSB keeps its fixed-horizon
forecast protocol, with early/late publication-cohort diagnostics rather than an
invalid stationary half-window interpretation.
