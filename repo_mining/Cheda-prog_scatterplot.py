import csv
import os
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.cm as cm

REPO_NAME = "rootbeer"
INPUT_CSV = "data/authors_file_touches_" + REPO_NAME + ".csv"
OUTPUT_PNG = "Cheda-prog_file_activity.png"


def load_touches(path):
    touches = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.strptime(row["Date"], "%Y-%m-%dT%H:%M:%SZ")
            touches.append({"filename": row["Filename"], "author": row["Author"], "date": date})
    return touches


def main():
    touches = load_touches(INPUT_CSV)
    if not touches:
        raise SystemExit("No touch data found in " + INPUT_CSV)

    start_date = min(t["date"] for t in touches)

    # One point per (author, file, week): dedupe multiple touches by the
    # same author on the same file in the same week into a single point.
    points = set()
    for t in touches:
        week = (t["date"] - start_date).days // 7
        points.add((week, t["filename"], t["author"]))

    files = sorted({p[1] for p in points})
    authors = sorted({p[2] for p in points})
    file_index = {f: i for i, f in enumerate(files)}
    author_index = {a: i for i, a in enumerate(authors)}

    cmap = cm.get_cmap("tab20", max(len(authors), 1))
    author_colors = {a: cmap(author_index[a]) for a in authors}

    fig_height = max(6, len(files) * 0.25)
    fig, ax = plt.subplots(figsize=(12, fig_height))

    for author in authors:
        weeks = [p[0] for p in points if p[2] == author]
        ys = [file_index[p[1]] for p in points if p[2] == author]
        ax.scatter(weeks, ys, label=author, color=author_colors[author], s=25, alpha=0.8)

    ax.set_yticks(range(len(files)))
    ax.set_yticklabels(files, fontsize=6)
    ax.set_xlabel("Weeks since first commit")
    ax.set_ylabel("Source file")
    ax.set_title("File activity over time by author — " + REPO_NAME)
    ax.legend(title="Author", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=7)

    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=150)
    print("Saved scatter plot to " + OUTPUT_PNG)


if __name__ == "__main__":
    main()
