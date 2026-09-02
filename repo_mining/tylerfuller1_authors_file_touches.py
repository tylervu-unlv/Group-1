import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

#extensions that will be considered as "source code"
SOURCE_EXTENSIONS = ('.java', '.kt', '.cpp', '.h', '.c')

# GitHub Authentication function
def github_auth(url, token):
    jsonData = None
    try:
        headers = {'Authorization': 'Bearer {}'.format(token)}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
    except Exception as e:
        pass
        print(e)
    return jsonData

# @touches, list for (file, author, date)
# @token, GitHub auth token
# @repo, GitHub repo
def collect_touches(touches, token, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits = github_auth(commitsUrl, token)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                if len(shaObject['parents']) > 1:
                    continue
                author = shaObject['commit']['author']['name']
                date = shaObject['commit']['author']['date']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails = github_auth(shaUrl, token)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename.endswith(SOURCE_EXTENSIONS):
                        touches.append([filename, author, date])
                        print(filename, author, date)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# read token from environment variable. 
token = os.environ.get('GITHUB_TOKEN')
if not token: 
    print("Error: GITHUB_TOKEN environment variable not set.")
    exit(1)

# determines and prints default branch instead of assuming its main
repoInfoUrl = 'https://api.github.com/repos/' + repo
repoInfo = github_auth(repoInfoUrl, token)
default_branch = repoInfo['default_branch']
print('Default branch: ' + default_branch)

touches = []
collect_touches(touches, token, repo)
print('Total touches recorded: ' + str(len(touches)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/touches_' + file + '.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for row in touches:
    writer.writerow(row)
fileCSV.close()
print('Touch data written to ' + fileOutput)
