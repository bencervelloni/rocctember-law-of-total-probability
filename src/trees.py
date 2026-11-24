"""Draws the walk-off probability tree (law of total probability) for the Rocctember post.

Usage: python src/trees.py   -> writes figures/walkoffs_tree.png
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(exist_ok=True)

SEPT, OTHER, GREY, ROOT, RESULT = "#9FE1CB", "#CECBF6", "#D3D1C7", "#F1EFE8", "#FAC775"


def draw_tree(filename, root, root_sub, sept_sub, other_sub, leaves, calcs, result, result_sub,
              callout, root_w=3.6, result_w=4.8, leaf_w=1.6, leaf_x=(1.1, 3.5, 6.5, 8.9), callout_w=8.6):
    fig, ax = plt.subplots(figsize=(9.5, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.6)
    ax.axis("off")

    def box(x, y, w, h, title, subtitle, color):
        ax.add_patch(patches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                     boxstyle="round,pad=0.02,rounding_size=0.08",
                     linewidth=1.1, edgecolor="#444441", facecolor=color))
        ax.text(x, y + h * 0.16, title, ha="center", va="center", fontsize=11.5,
                fontweight="bold", color="#2C2C2A")
        ax.text(x, y - h * 0.22, subtitle, ha="center", va="center", fontsize=10, color="#444441")

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color="#5F5E5A", lw=1.1))

    # root -> month split
    box(5, 6.8, root_w, 0.9, root, root_sub, ROOT)
    box(2.3, 5.3, 2.4, 0.9, "September", sept_sub, SEPT)
    box(7.7, 5.3, 2.4, 0.9, "Other months", other_sub, OTHER)
    arrow(5, 6.35, 2.6, 5.75)
    arrow(5, 6.35, 7.4, 5.75)

    # leaves: (title, subtitle) x4 -> sept-yes, sept-no, other-yes, other-no
    colors = (SEPT, GREY, OTHER, GREY)
    for (t, s), x, c in zip(leaves, leaf_x, colors):
        box(x, 3.8, leaf_w, 0.85, t, s, c)
    for x in leaf_x[:2]:
        arrow(2.3, 4.85, x, 4.22)
    for x in leaf_x[2:]:
        arrow(7.7, 4.85, x, 4.22)

    # recomposition
    ax.text(leaf_x[0], 3.15, calcs[0], ha="center", fontsize=9.5, color="#444441")
    ax.text(leaf_x[2], 3.15, calcs[1], ha="center", fontsize=9.5, color="#444441")
    arrow(leaf_x[0], 3.375, 4.1, 2.0)   # from the bottom of the leaf boxes
    arrow(leaf_x[2], 3.375, 5.9, 2.0)
    box(5, 1.5, result_w, 0.85, result, result_sub, RESULT)

    box(5, 0.35, callout_w, 0.6, callout, "", ROOT)

    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", OUT / filename)


# Walk-offs split by month
draw_tree("walkoffs_tree.png",
          "All plate appearances (2024-2026)", "1,233 AB",
          "190 AB  |  P = .154", "1,043 AB  |  P = .846",
          [("Walk-off", "4/190 = .0211"), ("No walk-off", ".9789"),
           ("Walk-off", "3/1043 = .0029"), ("No walk-off", ".9971")],
          (".0211 x .154 = .00325", ".0029 x .846 = .00243"),
          "Recomposed walk-off rate = .0057", ".00325 + .00243  (matches actual 7/1,233)",
          "September walk-off rate is 7.3x higher than other months (.0211 vs .0029)",
          root_w=4.0, result_w=5.0, leaf_w=1.8, leaf_x=(1.1, 3.7, 6.3, 8.9), callout_w=8.8)
