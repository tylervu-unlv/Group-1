import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

SOURCE_EXTENSIONS = (".java", ".kt", ".cpp", ".h")
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

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                author = shaDetails.get('commit', {}).get('author', {})
                author_name = shaDetails.get('author') or {}
                author_login = author_name.get('login', author.get('name', 'unknown'))
                date = author.get('date')

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename.endswith(SOURCE_EXTENSIONS):
                        dictfiles.setdefault(filename, []).append({
                            'author': author_login,
                            'date': date,
                            'sha': sha,
                        })
                        print(filename, author_login, date)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
token = os.environ.get("GITHUB_TOKEN")
if not token:
    raise SystemExit("Set GITHUB_TOKEN first: export GITHUB_TOKEN=\"your_token\"")
lstTokens = [token]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)

print('Total source files touched: ' + str(len(dictfiles)))

file = repo.split('/')[1]
fileOutput = 'data/touches_' + file + '.csv'
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(["Filename", "Author", "Date", "SHA"])

for filename, touches in dictfiles.items():
    for touch in touches:
        writer.writerow([filename, touch['author'], touch['date'], touch['sha']])

fileCSV.close()
print('Wrote ' + fileOutput)
