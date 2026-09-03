import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

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



# @fileTouches, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def authorFileTouches(fileTouches, lsttokens, repo):
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

                if shaDetails is None or 'files' not in shaDetails:
                    continue

                commit = shaDetails.get('commit', {})
                authorInfo = commit.get('author', {})
                authorName = authorInfo.get('name', 'N/A')
                commitDate = authorInfo.get('date', 'N/A')

                filesUsed = shaDetails['files']
                for filePath in filesUsed:
                    filename = filePath['filename']
                    if filename.endswith((".java", ".kt", ".h", ".c", ".cpp")):
                        if filename not in fileTouches:
                            fileTouches[filename] = []
                        fileTouches[filename].append({
                            "author": authorName,
                            "date": commitDate
                        })
                        print("filepath:", filename, " | ", "author:", authorName, " | ", "date:", commitDate)
               
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)



def findDefaultBranch(repo, lsttokens, ct):
    url = 'https://api.github.com/repos/' + repo
    repoData, ct = github_auth(url, lsttokens, ct)
    return repoData['default_branch'], ct 



# GitHub repo
repo = 'scottyab/rootbeer'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
token = os.environ.get("GITHUB_TOKEN")
lstTokens = [token]

# finds default branch
defaultBranch, ct = findDefaultBranch(repo, lstTokens, 0)
print("Default branch is named ", defaultBranch)

fileTouches = dict()
authorFileTouches(fileTouches, lstTokens, repo)
print('Total number of files: ' + str(len(fileTouches)))

for filepath, touches in fileTouches.items(): 
    print("\nFile: ", filepath)
    print("Touches: ", len(touches))
    for touch in touches:
        print(touch["author"], " on: ", touch["date"])
