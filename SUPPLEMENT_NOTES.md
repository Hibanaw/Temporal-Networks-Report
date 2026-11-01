# Measured experiment supplement

The source/experiment repository is [Hibanaw/Temporal-Networks](https://github.com/Hibanaw/Temporal-Networks), branch `main` (the initial supplement was developed on `supplement-experiments`).
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

## Review corrections

The core table now uses null differences for H2--H6 and explicitly labels H1 as
descriptive and H7 as two conditional P1/P2 peak ratios. The experiment CSV's
`effect` always means `value - null_mean`; for H7 its units are seconds and the
ratio is a separate field. Different hypotheses still do not have a common
substantive sensitivity scale. H1 grids/definitions differ and cannot rank networks.

CM H3 reverses under both observation halves; PS H2's full-period excess is small
and larger in the day-length halves. P1-invariant repetition measures provide no
temporal-null evidence. PS H7 is conditional on parameter choice and qualifying
outbreak seeds. CM does not support general slowing across nulls/timing metrics.
The primary CM second-half setting has major-outbreak probability 0.360; two weaker
settings have no major real outbreaks and undefined peaks. Inter-day inactivity,
seed sampling and residual horizons are plausible boundary mechanisms, not causal
effects identified separately from the saved CSV comparisons.
