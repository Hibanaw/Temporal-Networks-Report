# Report snapshot — 29 October 2026

The canonical manuscript is main.tex; b_report.tex is the detailed B companion.
The shortened title and full-width hypothesis table from Overleaf commit 4b93753
are preserved. This update edits B's interpretation and the manuscript layout.

Compile using PDFLaTeX, BibTeX, then PDFLaTeX twice (repeat if labels change).
All figure PDFs needed by either report are in figures/.

Main manuscript figures are drawn at their final printed widths:
- Full width 6.875 in: four panels in one horizontal row.
- Column width 3.28125 in: two panels in one horizontal row.
- Activity height 1.25 in; forecast height 1.35 in.
- Aggregation height 1.60 in; growth height 1.55 in.
- Figure text is 80% of the original pre-scaling revision: axis labels 6.4 pt, ticks 6 pt, legends 5.6 pt; manuscript body remains 10 pt.
- Panel gutters and outer padding are tightened before final-width placement. Tables use tabular* with distributed column gaps to reach column/text width, preserving their font sizes; no table resize was needed.

AIC bars, repeated fitted-parameter/collapse graphics, the constant diameter plot,
and introductory time-order/null cartoons are omitted from the main manuscript.
Their content remains in tables/text and the detailed companion/assets.
Empty PS/CM image boxes are omitted; draft expected prose stays explicitly labelled.

Interpretation corrections:
- Primary forecast: ages 1–5 -> cumulative citations at age 15 (ten years ahead).
- All selected age-15 targets lie within the observed period.
- The secondary 2020 endpoint mixes prediction horizons and is not lifetime impact.
- Optimizer success (500/500) differs from touching a bound (193/500).
- Effective diameter is measured inside the weak LCC, excluding isolates.
- P3b preserves calibrated age preference and removes explicit degree preference.

The full project's scripts/plot_b_manuscript.py redraws these figures from saved
results, without refitting any scientific model. The plotting script expects the
full project's results and processed data; these are not needed for LaTeX compilation.
The separate GitHub repository has newer E contributions. They are not overwritten
or merged into this Overleaf-based snapshot by this B-layout-only update.

The identical renderer source is also included in figure_sources/plot_b_manuscript.py.
When invoking that archived copy, set PC5253_PROJECT_ROOT to the full project root
containing results/b and data/processed/CIT; the original scripts/ copy needs no override.
