# Consolidation of the code repository's report directory

The ordinary `report/` directory from `Hibanaw/Temporal-Networks` at commit
`3a90bd0` was compared with this repository's main at `0f51e22` before replacing
that directory with a Git submodule.

- No file existed only in the code repository's report copy.
- All bibliography keys and entry contents were already present here; differences
  were whitespace only.
- The delivered E methods, centrality and community results, and associated figure
  assets were already integrated here. The community text differed only by a
  trailing blank line.
- A/C/D measured results, H1--H7 and robustness tables, and the corrected data
  card and experimental conventions were retained from this repository.
- B's newer fixed-horizon forecast interpretation, optimizer/boundary distinction,
  figure layout and companion were retained. The older code copy was not used to
  restore outdated wording or duplicate figures.
- The compiled manuscript and source bundle remain the verified delivery from
  `0f51e22`; this consolidation does not change manuscript content.

This repository is the canonical manuscript. The code repository's `report/`
is a pinned submodule with `branch = main`; clone it recursively or initialize
its submodules. Report edits must be committed and pushed here first, then the
code repository must commit the updated submodule pointer.
