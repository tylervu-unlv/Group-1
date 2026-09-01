"""
Part 2, Task 3: Visualize repository activity as a scatter plot.

X-axis: weeks since the beginning of the repository
Y-axis: source files
Color: the author responsible for the change

"""

import csv
import sys
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib as mpl


def parse_date(iso_str):
    return datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def main():
    touches = []
    try:
        with open("data/touches_rootbeer.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                touches.append(row)
    except FileNotFoundError:
        sys.exit("ERROR: data/touches_rootbeer.csv not found. Run zombieg1rl_authors_file_touches.py first.")

    if not touches:
        sys.exit("ERROR: no touches found — nothing to plot.")

    dates = [parse_date(t["Date"]) for t in touches if t.get("Date")]
    start = min(dates)

    points = set()
    for t in touches:
        if not t.get("Date"):
            continue
        week = (parse_date(t["Date"]) - start).days // 7
        points.add((week, t["Filename"], t["Author"]))

    files_sorted = sorted({p[1] for p in points})
    file_to_y = {path: i for i, path in enumerate(files_sorted)}

    authors_sorted = sorted({p[2] for p in points})
    cmap = mpl.colormaps["tab20"].resampled(max(len(authors_sorted), 1))
    author_to_color = {author: cmap(i) for i, author in enumerate(authors_sorted)}

    fig, ax = plt.subplots(figsize=(14, max(6, len(files_sorted) * 0.3)))

    for author in authors_sorted:
        xs = [wk for wk, path, a in points if a == author]
        ys = [file_to_y[path] for wk, path, a in points if a == author]
        ax.scatter(xs, ys, label=author, color=author_to_color[author], s=25, alpha=0.8)

    ax.set_xlabel("Weeks since repository start")
    ax.set_ylabel("Source files")
    ax.set_yticks(range(len(files_sorted)))
    ax.set_yticklabels(files_sorted, fontsize=7)
    ax.set_title("scottyab/rootbeer — File Activity Over Time by Author")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=7)

    fig.tight_layout()
    fig.savefig("zombieg1rl_file_activity.png", dpi=150, bbox_inches="tight")
    print("Wrote zombieg1rl_file_activity.png")
    print(f"Plotted {len(points)} points across {len(files_sorted)} files and {len(authors_sorted)} authors.")


if __name__ == "__main__":
    main()