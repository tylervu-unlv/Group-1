import csv
import json
import os
import requests

# Read the source files from first script.
def get_source_files(filename):
    sourceFiles = []

    with open(filename, 'r') as fileCSV:
        reader = csv.DictReader(fileCSV)

        for row in reader:
            sourceFiles.append(row['Filename'])

    return sourceFiles

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# Get the commits that changed a source file
def get_file_commits(repo, filename, lstTokens):
    ct = 0
    commitsUrl = (
        'https://api.github.com/repos/' + repo +
        '/commits?path=' + filename
    )

    commits, ct = github_auth(commitsUrl, lstTokens, ct)

    return commits

# Get the authors and dates for changes to a file
def get_file_history(commits):
    fileHistory = []

    for commitObj in commits:
        author = commitObj['commit']['author']['name']
        date = commitObj['commit']['author']['date']

        fileHistory.append([author, date])

    return fileHistory

# Collect the change history for each source file
def collect_file_history(repo, sourceFiles, lstTokens):
    fileData = []

    for filename in sourceFiles:
        commits = get_file_commits(repo, filename, lstTokens)
        history = get_file_history(commits)

        fileData.append([
            filename,
            history,
            len(history)
        ])

    return fileData

# GitHub repo
repo = 'scottyab/rootbeer'

# GitHub authentication token
lstTokens = [os.getenv("GITHUB_TOKEN")]

# Source files created by VegasBear_collect_files
sourceFileCSV = 'data/file_rootbeer.csv'

sourceFiles = get_source_files(sourceFileCSV)
fileData = collect_file_history(repo, sourceFiles, lstTokens)

# Write file history to CSV
fileOutput = 'data/authors_file_touches.csv'

fileCSV = open(fileOutput, 'w', newline='')
writer = csv.writer(fileCSV)

writer.writerow([
    'File Path',
    'Author',
    'Date',
    'Number of Changes'
])

for filename, history, changeCount in fileData:

    for author, date in history:
        writer.writerow([
            filename,
            author,
            date,
            changeCount
        ])

fileCSV.close()
