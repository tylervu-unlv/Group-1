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

# Get's the languages used from the repository
def get_repo_lang(repo,lstTokens):
    ct = 0
    languagesUrl = 'https://api.github.com/repos/' + repo + '/languages'
    languages, ct = github_auth(languagesUrl,lstTokens,ct)
    return languages

# Get's the repositories main branch.
def get_default_branch(repo, lstTokens):
    ct = 0
    repoUrl = 'https://api.github.com/repos/' + repo
    repoInfo, ct = github_auth(repoUrl, lstTokens, ct)

    return repoInfo['default_branch']

# Based on languages from previous function, tells what file extensions are.
source_extensions = {
    'Java': ['.java'],
    'Kotlin': ['.kt'],
    'Python': ['.py'],
    'C': ['.c'],
    'C++': ['.cpp']
}

excluded_directories = {
    '.git',
    '.gradle',
    'build',
    'out',
    'target',
    'bin',
    'generated',
    'test'
}

def is_source_file(filename, repoExtensions):
    extension = os.path.splitext(filename)[1].lower()
    folders = filename.lower().split('/')

    if extension not in repoExtensions:
        return False

    for folder in folders:
        if folder in excluded_directories:
            return False

    return True

def collect_source_files(repo, lstTokens, defaultBranch, repoExtensions):
    sourceFiles = []
    ct = 0

    treeUrl = (
        'https://api.github.com/repos/' + repo +
        '/git/trees/' + defaultBranch + '?recursive=1'
    )

    treeData, ct = github_auth(treeUrl, lstTokens, ct)

   

    for fileObj in treeData['tree']:
        if fileObj['type'] == 'blob':
            filename = fileObj['path']

            if is_source_file(filename, repoExtensions):
                sourceFiles.append(filename)

    return sourceFiles

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
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    dictfiles[filename] = dictfiles.get(filename, 0) + 1
                    print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'

# Personal Github Token.
lstTokens = [os.getenv("GITHUB_TOKEN")]

languages = get_repo_lang(repo, lstTokens)
defaultBranch = get_default_branch(repo, lstTokens)

repoExtensions = []

for language in languages:
    if language in source_extensions:
        repoExtensions.extend(source_extensions[language])

source_files = collect_source_files (
    repo,
    lstTokens,
    defaultBranch,
    repoExtensions
)
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits

#dictfiles = dict()
#countfiles(dictfiles, lstTokens, repo)
#print('Total number of files: ' + str(len(dictfiles)))

print('Total number of files: ' + str(len(source_files)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for filename in source_files:
    rows = [filename]
    writer.writerow(rows)
fileCSV.close()

