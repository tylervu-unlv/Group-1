import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import os



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
def collectTouches(lsttokens, repo):
    touches = []
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
                date = authorInfo.get('date', 'N/A')

                if date == 'N/A':
                    continue

                commitDate = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

                filesUsed = shaDetails['files']
                for filePath in filesUsed:
                    filename = filePath['filename']
                    if filename.endswith((".java", ".kt", ".h", ".c", ".cpp")):
                        touches.append((commitDate, filename, authorName))
                        print("collected the filepath:", filename, " | ", "author:", authorName, " | ", "date:", commitDate)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
    return touches



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

touches = collectTouches(lstTokens, repo)

earliestCommit = min(t[0] for t in touches)
print("Earliest commit date: ", earliestCommit)

# convert each touch into week, filename, and author
uniquePoints = set(); 
for commitDate, filename, authorName, in touches:
    weeks = (commitDate - earliestCommit).days // 7
    uniquePoints.add((weeks, filename, authorName))
print("Unique points:", len(uniquePoints))


# mappings
allFilenames = sorted(set(p[1] for p in uniquePoints))
filenameToIndex = {filename: i for i, filename in enumerate(allFilenames)}

allAuthors = sorted(set(p[2] for p in uniquePoints))
authorToColor = {author: i for i, author in enumerate(allAuthors)}

# lists for plotting
xVal = []
yVal = []
colorVal = []

for week, filename, authorName in uniquePoints:
    xVal.append(week)
    yVal.append(filenameToIndex[filename])
    colorVal.append(authorToColor[authorName])


# plot
fig, ax = plt.subplots(figsize=(14, max(6, len(allFilenames) * 0.3)))
scatter = ax.scatter(yVal, xVal, c=colorVal, cmap='tab20', s=40)

#label axes
ax.set_xticks(range(len(allFilenames)))
ax.set_xlabel("file")
ax.set_ylabel("weeks")
ax.set_title("Repository Activity")

plt.tight_layout()
plt.show()





