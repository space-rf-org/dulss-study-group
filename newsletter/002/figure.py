#!/usr/bin/env python3
"""Figure for issue 002 — What a quorum actually buys.

The (R, W) configuration space for N = 5, coloured by which of the TWO quorum
inequalities hold. `R + W > N` buys read-write intersection; `2W > N` buys
write-write intersection. The band where the first holds and the second does
not is the subject of the issue.

Usage:  python3 figure.py          # writes assets/quorum-space.{svg,png}
        python3 figure.py --table  # every number quoted in the issue
"""

import argparse
import math

# --- the two inequalities -------------------------------------------------


def reads_intersect_writes(r, w, n):
    """|R n W| >= R + W - N, so R + W > N forces an overlap."""
    return r + w > n


def writes_intersect_writes(w, n):
    """Same argument with two write sets: |W1 n W2| >= 2W - N."""
    return 2 * w > n


def zone(r, w, n):
    if not reads_intersect_writes(r, w, n):
        return "none"
    return "both" if writes_intersect_writes(w, n) else "visibility"


def blind_spots(n):
    """Configs that pass the check everyone runs and fail the one they don't."""
    return [(r, w) for w in range(1, n + 1) for r in range(1, n + 1) if zone(r, w, n) == "visibility"]


# --- what waiting for W of N costs ----------------------------------------


def p_slow(w, n, p):
    """P(write is slow) when waiting for W of N acks, replicas independent.

    The W-th fastest is slow exactly when fewer than W replicas are fast, i.e.
    when at least N - W + 1 of them are slow.
    """
    return sum(math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n - w + 1, n + 1))


def print_tables():
    print("== Blind spots: R + W > N holds, 2W > N does not ==")
    for n in (3, 5, 7):
        spots = blind_spots(n)
        print(f"  N={n}: {len(spots)} config(s) -> {', '.join(f'(R={r},W={w})' for r, w in spots)}")

    print("\n== The scaling trap ==")
    for n in (3, 5):
        w = 2
        print(f"  N={n}, W=2: read-write needs R>{n-w} ; write-write 2W={2*w} vs N={n} -> "
              f"{'holds' if writes_intersect_writes(w, n) else 'FAILS'}")
    print("  Adding two replicas while holding W=2 loses write-write intersection.")

    print("\n== Cost of waiting for W of N (single replica slow 1% of the time) ==")
    n, p = 3, 0.01
    for w in (1, 2, 3):
        q = p_slow(w, n, p)
        ratio = q / p
        how = f"{1/ratio:,.0f}x better" if ratio < 1 else f"{ratio:.1f}x worse"
        print(f"  W={w}: P(slow)={q:.3e}  ({how} than one replica)")


# --- figure ----------------------------------------------------------------

N = 5
FILL = {"none": "#eceff1", "visibility": "#f0c05a", "both": "#bcd6e8"}
INK = {"none": "#7b8288", "visibility": "#3d2f06", "both": "#123650"}
LABEL = {
    "none": "neither — a read can miss the write",
    "visibility": "R + W > N only — reads intersect writes, writes do not intersect each other",
    "both": "R + W > N and 2W > N",
}


def make_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    fig, ax = plt.subplots(figsize=(9.0, 5.4))

    for w in range(1, N + 1):
        for r in range(1, N + 1):
            z = zone(r, w, N)
            ax.add_patch(Rectangle((r - 0.5, w - 0.5), 1, 1, facecolor=FILL[z],
                                   edgecolor="white", linewidth=2.0, zorder=1))
            ax.text(r, w, f"{r+w}", ha="center", va="center", fontsize=10.5,
                    color=INK[z], zorder=2,
                    fontweight="bold" if z == "visibility" else "normal")

    # Outline the blind spots and name one config people actually reach for.
    for r, w in blind_spots(N):
        ax.add_patch(Rectangle((r - 0.5, w - 0.5), 1, 1, facecolor="none",
                               edgecolor="#b3121f", linewidth=2.2, zorder=3))

    ax.annotate("these three pass the\ncheck everyone runs,\nand fail the one\nthey don't",
                xy=(5.48, 1.5), xycoords="data", annotation_clip=False,
                xytext=(1.06, 0.30), textcoords="axes fraction",
                fontsize=9, color="#8c1020", linespacing=1.5, ha="left", va="center",
                arrowprops=dict(arrowstyle="->", lw=1.1, color="#8c1020",
                                connectionstyle="arc3,rad=0.2"))

    ax.set_xticks(range(1, N + 1))
    ax.set_yticks(range(1, N + 1))
    ax.set_xlim(0.5, N + 0.5)
    ax.set_ylim(0.5, N + 0.5)
    ax.set_xlabel("R — replicas consulted per read")
    ax.set_ylabel("W — acks required per write")
    ax.set_title(f"Quorum configurations for N = {N}   (cell shows R + W)",
                 fontsize=11.5, loc="left", pad=12)
    ax.set_aspect("equal")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)

    handles = [Rectangle((0, 0), 1, 1, facecolor=FILL[z], edgecolor="#d7dade")
               for z in ("none", "visibility", "both")]
    ax.legend(handles, [LABEL[z] for z in ("none", "visibility", "both")],
              loc="upper left", bbox_to_anchor=(0.0, -0.13), fontsize=8.5,
              frameon=False, handlelength=1.1, handleheight=1.1, labelspacing=0.45)

    fig.tight_layout()
    for ext in ("svg", "png"):
        fig.savefig(f"assets/quorum-space.{ext}", dpi=200, transparent=False,
                    bbox_inches="tight", facecolor="white")
    print("wrote assets/quorum-space.svg and .png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", action="store_true", help="print the numbers instead of drawing")
    a = ap.parse_args()
    print_tables() if a.table else make_figure()
