import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Read the data created in VegasBear_authors_file_touches.
def read_file_activity(filename):
    fileActivity = []

    with open(filename, 'r') as fileCSV:
        reader = csv.DictReader(fileCSV)

        for row in reader:
            fileActivity.append(row)

    return fileActivity



# Find the oldest change date.
def get_start_date(fileActivity):
    dates = []

    for row in fileActivity:
        date = datetime.strptime(
            row['Date'],
            '%Y-%m-%dT%H:%M:%SZ'
        )

        dates.append(date)

    return min(dates)

# Calclulate how many weeks after the start each change happened.
def get_week(date, startDate):
    changeDate = datetime.strptime(
        date,
        '%Y-%m-%dT%H:%M:%SZ'
    )

    daysSinceStart = (changeDate - startDate).days
    week = daysSinceStart // 7

    return week

# Gather needed information for the scatterplot.
def get_plot_data(fileActivity, startDate):
    weeks = []
    files = []
    authors = []

    for row in fileActivity:
        week = get_week(row['Date'], startDate)

        weeks.append(week)
        files.append(row['File Path'])
        authors.append(row['Author'])

    return weeks, files, authors

# Create the scatter plot
def create_scatterplot(weeks, files, authors):
    uniqueAuthors = list(set(authors))

    for author in uniqueAuthors:
        authorWeeks = []
        authorFiles = []

        for i in range(len(authors)):
            if authors[i] == author:
                authorWeeks.append(weeks[i])
                authorFiles.append(files[i])

        plt.scatter(
            authorWeeks,
            authorFiles,
            label=author
        )

    plt.xlabel('Weeks Since Beginning of Repository')
    plt.ylabel('Source Files')
    plt.title('RootBeer Source File Activity')

    plt.legend(
        title='Authors',
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )

    plt.tight_layout()

    plt.savefig(
        'VegasBear_file_activity.png',
        bbox_inches='tight'
    )
activityFile = 'data/authors_file_touches.csv'

fileActivity = read_file_activity(activityFile)

startDate = get_start_date(fileActivity)

weeks, files, authors = get_plot_data(
    fileActivity,
    startDate
)

create_scatterplot(weeks, files, authors)