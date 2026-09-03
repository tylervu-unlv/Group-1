import csv
from datetime import datetime
import matplotlib.pyplot as plt

# read touch data from task 2
touches = []
with open('data/touches_rootbeer.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        touches.append(row)

# parse dates
for t in touches:
    t['date_parsed'] = datetime.strptime(t['Date'], '%Y-%m-%dT%H:%M:%SZ')

# earliest date = week 0
all_dates = []
for t in touches:
    all_dates.append(t['date_parsed'])
start_date = min(all_dates)

# weeks since start
for t in touches:
    days_since_start = (t['date_parsed'] - start_date).days
    t['week'] = days_since_start // 7

# dedupe to unique file/author/week combos
unique_touches = []
seen = set()
for t in touches:
    key = (t['Filename'], t['Author'], t['week'])
    if key not in seen:
        seen.add(key)
        unique_touches.append(t)

# map filenames to y positions
filenames_set = set()
for t in unique_touches:
    filenames_set.add(t['Filename'])
filenames = sorted(filenames_set)

filename_to_y = {}
for i, name in enumerate(filenames):
    filename_to_y[name] = i

# map authors to colors
authors_set = set()
for t in unique_touches:
    authors_set.add(t['Author'])
authors = sorted(authors_set)

cmap = plt.get_cmap('tab20')
author_to_color = {}
for i, author in enumerate(authors):
    author_to_color[author] = cmap(i % 20)

# plot
fig, ax = plt.subplots(figsize=(14, 10))

for author in authors:
    xs = []
    ys = []
    for t in unique_touches:
        if t['Author'] == author:
            xs.append(t['week'])
            ys.append(filename_to_y[t['Filename']])
    ax.scatter(xs, ys, label=author, color=author_to_color[author], s=40, alpha=0.8)

ax.set_yticks(range(len(filenames)))
ax.set_yticklabels(range(len(filenames)), fontsize=8)
ax.set_xlabel('weeks since repository start')
ax.set_ylabel('source file')
ax.set_title('scottyab/rootbeer: file activity by author over time')
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=6)

plt.tight_layout()
plt.savefig('tylerfuller1_file_activity.png', dpi=150)
print('plot saved to tylerfuller1_file_activity.png')

# lookup table since y-axis uses numbers
print('\nfile index lookup:')
for i, name in enumerate(filenames):
    print(str(i) + ': ' + name)