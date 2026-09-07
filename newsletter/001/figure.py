#!/usr/bin/env python3
"""Figure for issue 001 — Eleven nines, recomputed.

Annual probability of losing a 3-way-replicated placement group, as a function of
the correlated-wipe rate c. The independent (disk-failure) term is a floor at
~6.2e-13/yr; everywhere that evidence can reach, the answer is c and c alone.

Usage:  python3 figure.py        # writes assets/durability-floor.{svg,png}
Reproduces every number quoted in the issue; `python3 figure.py --table`
prints the parameter sweep and the rule-of-three bounds.
"""

import argparse
import math

HOURS_PER_YEAR = 8766.0


def mttdl_hours(afr, mttr_h, n=3):
    """Mean time to data loss for n-way replication, repair rate mu >> failure rate lambda.

    Markov chain on the number of surviving replicas (n ... 0), state 0 absorbing.
    For n = 3 the loss rate is 3L * (2L/mu) * (L/mu) = 6 L^3 MTTR^2, so
    MTTDL = MTTF^3 / (6 MTTR^2). The general form is MTTF^n / (n! MTTR^(n-1)).
    """
    mttf_h = HOURS_PER_YEAR / afr
    factorial = math.factorial(n)
    return mttf_h**n / (factorial * mttr_h ** (n - 1))


def p_loss_per_year(afr, mttr_h, n=3):
    return 1.0 / (mttdl_hours(afr, mttr_h, n) / HOURS_PER_YEAR)


def nines(p):
    return -math.log10(p)


# Baseline used throughout the issue: 2% AFR, 1-hour distributed rebuild.
AFR, MTTR_H = 0.02, 1.0
P_IND = p_loss_per_year(AFR, MTTR_H)


def print_tables():
    print("== 3-way replication: the number is a knob ==")
    for afr in (0.01, 0.02, 0.04):
        for mttr in (0.5, 1, 4, 10, 24):
            p = p_loss_per_year(afr, mttr)
            print(f"  AFR={afr:4.0%}  MTTR={mttr:5.1f}h  P={p:.3e}/yr  nines={nines(p):5.2f}")
    print(f"\n== Baseline: P_ind = {P_IND:.3e}/yr = {nines(P_IND):.2f} nines ==")
    print(f"   Knee (c == P_ind): c = {P_IND:.2e} per domain-year")
    for c in (1e-12, 1e-10, 1e-8, 1e-6, 1e-4):
        tot = P_IND + c
        print(f"   c={c:.0e} -> {nines(tot):5.2f} nines; independent term is {100*P_IND/tot:8.4f}% of the answer")
    print("\n== Rule of three: 95% upper bound from N clean domain-years ==")
    for dy in (1e5, 1e6, 1e7, 1e8):
        print(f"   {dy:.0e} domain-years, zero losses -> c <= {3/dy:.1e} -> at most {nines(3/dy):5.2f} demonstrated nines")
    print(f"\n   To demonstrate 1e-11: {3/1e-11:.1e} clean domain-years required.")


def make_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    c = np.logspace(-15, -4, 400)
    total = P_IND + c

    fig, ax = plt.subplots(figsize=(8, 4.8))

    # The region where evidence can actually reach: c >= 3/N for a plausible N.
    ax.axvspan(3e-7, 1e-4, color="#c8102e", alpha=0.07, lw=0)
    ax.text(5.5e-6, 3e-4, "the only region\nevidence can bound\n(10⁷ clean domain-years)",
            fontsize=8, color="#8c1020", ha="center", va="top", linespacing=1.4)

    ax.axhline(P_IND, color="#8a8a8a", ls="--", lw=1.2)
    ax.text(1.3e-15, P_IND / 2.6, f"independent disk-failure floor — {P_IND:.1e}/yr, {nines(P_IND):.1f} nines",
            fontsize=8.5, color="#5a5a5a", va="top")

    ax.plot(c, total, color="#c8102e", lw=2.2, label="total annual loss probability")
    ax.plot(c, c, color="#1f4e79", lw=1.1, ls=":", label="correlated term alone")

    ax.plot([P_IND], [2 * P_IND], "o", ms=5, color="#1a1a1a")
    ax.annotate("knee: c = 6.2×10⁻¹³\nright of here, the floor is noise",
                xy=(P_IND, 2 * P_IND), xytext=(2.5e-12, 8e-9), fontsize=8.5,
                arrowprops=dict(arrowstyle="->", lw=0.9, color="#1a1a1a"))

    for target, label in ((1e-11, "11 nines"), (1e-6, "6 nines")):
        ax.axhline(target, color="#bbbbbb", lw=0.7, zorder=0)
        ax.text(1.3e-15, target * 1.3, label, fontsize=8, color="#8a8a8a")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-15, 1e-4)
    ax.set_ylim(1e-15, 1e-3)
    ax.set_xlabel("c — rate of correlated events that wipe a placement group (per domain-year)")
    ax.set_ylabel("P(data loss) per year")
    ax.set_title("The floor you can compute vs. the term that decides the answer",
                 fontsize=11, loc="left", pad=10)
    ax.legend(loc="upper left", fontsize=8.5, frameon=False, bbox_to_anchor=(0.008, 0.99))
    ax.grid(alpha=0.18, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()

    for ext in ("svg", "png"):
        fig.savefig(f"assets/durability-floor.{ext}", dpi=200, transparent=False)
    print("wrote assets/durability-floor.svg and .png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", action="store_true", help="print the numbers instead of drawing")
    args = ap.parse_args()
    print_tables() if args.table else make_figure()
