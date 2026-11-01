"""Manuscript figures at final CVPR widths; redraw saved results, never refit.

Two panels occupy one 3.28125-inch column; four panels occupy the 6.875-inch
text width. Text is 80% of the preceding revision at the final printed size. Original diagnostic
assets remain available for the companion report and numerical audit.
"""
import json
import os
import shutil
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LogLocator
from matplotlib.patches import FancyBboxPatch
from matplotlib.text import Text
import numpy as np
import pandas as pd

ROOT = Path(os.environ.get('PC5253_PROJECT_ROOT', Path(__file__).resolve().parents[1]))
OUT = ROOT / 'results/b'
FIG = ROOT / 'figures'
COL = {'real': '#173F5F', 'annual': '#C36A2B', 'P3a': '#D27D2D',
       'P3b': '#2C8A78', 'linear': '#2C8A78'}
plt.rcParams.update({
    'font.size': 8, 'axes.labelsize': 8, 'axes.titlesize': 8,
    'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'legend.fontsize': 7,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': .6, 'lines.linewidth': 1.1,
    'axes.labelpad': 2, 'axes.titlepad': 3, 'xtick.major.pad': 2, 'ytick.major.pad': 2,
    'pdf.fonttype': 42, 'savefig.dpi': 220,
})


def save(fig, name):
    # Reduce text only, then let constrained layout recompute the gutters.
    for text in fig.findobj(Text):
        text.set_fontsize(text.get_fontsize() * .80)
    fig.canvas.draw()
    FIG.mkdir(exist_ok=True)
    destination = ROOT / 'report/figures'
    destination.mkdir(exist_ok=True)
    for ext in ['pdf', 'png']:
        fig.savefig(FIG / f'{name}.{ext}')
    shutil.copy2(FIG / f'{name}.pdf', destination / f'{name}.pdf')
    plt.close(fig)


def axes_grid(rows, cols, width, height):
    fig, axs = plt.subplots(rows, cols, figsize=(width, height),
                            layout='constrained', squeeze=False)
    fig.set_constrained_layout_pads(w_pad=.004, h_pad=.008, wspace=.025, hspace=.04)
    return fig, axs.flatten()


def main():
    agg = pd.read_csv(OUT / 'aggregation.csv')
    win = pd.read_csv(OUT / 'windows.csv')
    nodes = pd.read_csv(ROOT / 'data/processed/CIT/nodes.csv')

    fig, axs = axes_grid(1, 2, 3.28125, 1.25)
    d = agg[agg['mode'] == 'annual']
    axs[0].bar(d.year, d.E, color=COL['real'], width=.85)
    axs[1].plot(nodes.groupby('year').size(), color=COL['P3b'])
    for ax, title, label in zip(axs, ['(a) Citations', '(b) Publications'],
                                ['Citations / year', 'Papers / year']):
        ax.set(title=title, xlabel='Year', ylabel=label, xlim=(1970, 2021))
        ax.set_xticks([1980, 2000, 2020])
        ax.yaxis.set_major_locator(MaxNLocator(3))
    save(fig, 'b_manuscript_activity')

    fig, axs = axes_grid(1, 4, 6.875, 1.60)
    for ax, metric, label, letter in zip(axs[:2], ['density_directed', 'lcc_fraction'],
                                        ['Density (x 1000)', 'LCC fraction'], ['a', 'b']):
        for mode, color in [('annual', COL['annual']), ('cumulative', COL['real'])]:
            d = agg[agg['mode'] == mode]
            ax.plot(d.year, d[metric] * (1000 if metric == 'density_directed' else 1),
                    label='Annual' if mode == 'annual' else 'Cumul.', color=color)
        ax.set(xlabel='Year', ylabel=label, title=f'({letter}) ' + ('Density' if metric == 'density_directed' else 'Connectivity'))
        ax.legend(frameon=False, ncol=1, loc='upper right', handlelength=1.2, labelspacing=.15)
    for ax, metric, label, letter in zip(axs[2:], ['clustering_weak', 'lcc_fraction'],
                                        ['Clustering', 'LCC fraction'], ['c', 'd']):
        for width, d in win.groupby('window'):
            ax.plot(d.year, d[metric], label=f'{width} yr')
        ax.set(xlabel='End year', ylabel=label, title=f'({letter}) ' + ('Clustering' if metric == 'clustering_weak' else 'Connectivity'))
        ax.legend(frameon=False, ncol=2, loc='upper right', handlelength=.8, columnspacing=.5, handletextpad=.3, labelspacing=.15)
    axs[1].legend(frameon=False, ncol=1, loc='center', bbox_to_anchor=(.55, .52), handlelength=1.2, labelspacing=.15)
    for ax in axs:
        ax.grid(alpha=.15)
        ax.xaxis.set_major_locator(MaxNLocator(3, integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(3))
    handles, labels = axs[0].get_legend_handles_labels()
    h, lab = axs[2].get_legend_handles_labels()
    for ax in axs:
        ax.get_legend().remove()
    fig.set_layout_engine('constrained', rect=(0, .13, 1, .87))
    fig.legend(handles + h, labels + lab, loc='lower center', ncol=6, frameon=False,
               handlelength=1.4, columnspacing=1.3, borderaxespad=.1)
    save(fig, 'b_manuscript_aggregation')

    fig, axs = axes_grid(1, 4, 6.875, 1.55)
    pa = json.loads((OUT / 'pa.json').read_text())
    kernel = pd.read_csv(OUT / 'pa_kernel.csv')
    k = kernel[(kernel.hits >= 5) & (kernel.uniform_expected > 0)]
    axs[0].scatter(k.k + 1, k.relative_rate, s=8, alpha=.45, color=COL['real'], rasterized=True)
    x = np.geomspace(1, max(k.k) + 1, 100)
    scale = np.median(k.relative_rate / (k.k + 1) ** pa['alpha'])
    axs[0].plot(x, scale * x ** pa['alpha'], color='black', label=r'$\alpha=0.714$')
    axs[0].set(xscale='log', yscale='log', xlabel='Prior in-degree + 1',
               ylabel='Attachment rate', title='(a) Attachment')
    axs[0].legend(frameon=False)

    null = pd.read_csv(OUT / 'null_metrics.csv')
    for j, kind in enumerate(['P3a', 'P3b']):
        values = null[null.kind == kind].alpha.to_numpy()
        axs[1].scatter(np.full(len(values), j) + np.linspace(-.13, .13, len(values)),
                       values, s=10, color=COL[kind], alpha=.65)
    axs[1].errorbar([2], [pa['alpha']], yerr=[[pa['alpha'] - pa['ci95'][0]],
                                           [pa['ci95'][1] - pa['alpha']]],
                    fmt='o', color=COL['real'], capsize=3, markersize=4)
    axs[1].axhline(0, color='gray', lw=.6, ls=':')
    axs[1].set(xticks=[0, 1, 2], xticklabels=['P3a', 'P3b', 'Real'], xlim=(-.5, 2.5),
               ylabel=r'Exponent $\alpha$', title='(b) Null controls')

    age = pd.read_csv(OUT / 'age_curve.csv')
    axs[2].plot(age.age, age.relative_rate, color=COL['real'], label='Observed')
    for kind in ['P3a', 'P3b']:
        curves = []
        for i in range(20):
            a = pd.read_csv(OUT / 'null_events' / f'{kind}_{i:02d}_age.csv')
            curves.append(np.divide(a.hits, a.expected_uniform,
                                     out=np.full(len(a), np.nan), where=a.expected_uniform > 0))
        a = np.asarray(curves)
        valid = np.isfinite(a).sum(axis=0) > 1
        mean, sd = np.full(a.shape[1], np.nan), np.full(a.shape[1], np.nan)
        mean[valid], sd[valid] = np.nanmean(a[:, valid], axis=0), np.nanstd(a[:, valid], axis=0, ddof=1)
        axs[2].plot(age.age, mean, color=COL[kind], label=kind)
        axs[2].fill_between(age.age, mean - sd, mean + sd, color=COL[kind], alpha=.16)
    axs[2].set(xlabel='Paper age (yr)', ylabel='Age preference', xlim=(1, 40),
               title='(c) Ageing', ylim=(-.05, 2.7))
    axs[2].legend(frameon=False, ncol=1, handlelength=1, labelspacing=.1, loc='upper right')

    den = json.loads((OUT / 'densification.json').read_text())
    d = agg[(agg['mode'] == 'cumulative') & (agg.year >= 1990)]
    axs[3].scatter(d.N, d.E, c=d.year, cmap='viridis', s=14)
    x = np.geomspace(d.N.min(), d.N.max(), 100)
    axs[3].plot(x, np.exp(den['intercept']) * x ** den['a'], color='black', label=r'$a=1.343$')
    axs[3].set(xscale='log', yscale='log', xlabel='Papers N',
               ylabel='Citations E', title='(d) Densification')
    axs[3].legend(frameon=False)
    for ax in [axs[0], axs[3]]:
        ax.minorticks_off()
        ax.xaxis.set_major_locator(LogLocator(numticks=3))
        ax.yaxis.set_major_locator(LogLocator(numticks=3))
    save(fig, 'b_manuscript_growth')

    pred = pd.read_csv(OUT / 'wsb_predictions.csv')
    pred = pred[pred.evaluation == 'age15']
    summary = json.loads((OUT / 'wsb_summary.json').read_text())
    fig, axs = axes_grid(1, 2, 3.28125, 1.35)
    hi = max(float(pred.observed.max() + 1), float(pred.wsb.max() + 1), float(pred.linear.max() + 1))
    for model, label in [('wsb', 'WSB'), ('linear', 'Linear')]:
        axs[0].scatter(pred.observed + 1, pred[model] + 1, s=4, alpha=.3,
                       color=COL['real' if model == 'wsb' else 'linear'], label=label, rasterized=True)
    axs[0].plot([1, hi], [1, hi], color='black', lw=.6)
    axs[0].set(xscale='log', yscale='log', xlim=(1, hi), ylim=(1, hi),
               xlabel='Observed c(15) + 1', ylabel='Predicted c(15) + 1', title='(a) Age-15 prediction')
    axs[0].xaxis.set_major_locator(LogLocator(numticks=3))
    axs[0].yaxis.set_major_locator(LogLocator(numticks=3))
    axs[0].minorticks_off()
    axs[0].legend(frameon=False, handletextpad=.2, borderpad=.1, labelspacing=.15)
    comparisons = [next(v for v in summary['evaluation'] if v.get('evaluation') == tag
                        and v.get('paired_difference') == 'WSB minus linear')
                   for tag in ['age15', 'observed_endpoint']]
    vals = np.array([r['mean_MAE_difference'] for r in comparisons])
    ci = np.array([r['ci95'] for r in comparisons])
    axs[1].errorbar(vals, [1, 0], xerr=[vals - ci[:, 0], ci[:, 1] - vals],
                    fmt='o', markersize=3, capsize=2, color=COL['real'])
    axs[1].axvline(0, ls='--', lw=.7, color='gray')
    axs[1].set(yticks=[1, 0], yticklabels=['Age 15', '2020'], ylim=(-.7, 1.7),
               xlabel='MAE difference', title='(b) Paired error')
    axs[1].xaxis.set_major_locator(MaxNLocator(3))
    save(fig, 'b_manuscript_forecast')

    # Four conceptual panels; P3 is included explicitly in the study overview.
    fig, ax = plt.subplots(figsize=(6.875, 1.25), layout='constrained')
    fig.set_constrained_layout_pads(w_pad=.004, h_pad=.008)
    ax.axis('off'); ax.set(xlim=(0, 4), ylim=(0, 1))
    parts = [('I  Representation', 'Aggregation and windows', 'H1  |  M1'),
             ('II  Activity', 'Burstiness and persistence', 'H2, H3  |  M2a, M2b'),
             ('III  Evolution', 'Growth and communities', 'H4, H5  |  M2c, M4'),
             ('IV  Function', 'Paths and spreading', 'H6, H7  |  M3a--c')]
    colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2']
    for i, (title, description, methods) in enumerate(parts):
        ax.add_patch(FancyBboxPatch((i + .03, .29), .94, .65, boxstyle='round,pad=.01',
                                    fc=colors[i], alpha=.15, ec=colors[i]))
        ax.text(i + .5, .80, title, ha='center', va='center', fontsize=8.5, weight='bold')
        ax.text(i + .5, .59, description.replace(' and ', '\nand '), ha='center', va='center', fontsize=8)
        ax.text(i + .5, .36, methods, ha='center', va='center', fontsize=8)
    ax.text(2, .12, 'Datasets: contact (PS), messaging (CM), citation (CIT)   |   Controls: P1/P2 (PS, CM), P3 (CIT)',
            ha='center', va='center', fontsize=8)
    save(fig, 'b_manuscript_framework')


if __name__ == '__main__':
    main()
