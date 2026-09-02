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

# Get repository information
def get_repo_info(repo, lsttokens, ct):
    url = 'https://api.github.com/repos/' + repo
    jsonData, ct = github_auth(url, lsttokens, ct)

    default_branch = jsonData['default_branch']
    languages_url = jsonData['languages_url']

    languages, ct = github_auth(languages_url, lsttokens, ct)

    return default_branch, languages, ct

# file extensions that indicate source files in repository
SOURCE_EXTENSIONS = {
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'Header',
    '.xml': 'XML'
}

NON_SOURCE_EXTENSIONS = {
    '.class',
    '.jar',
    '.aar',
    '.apk',
    '.dex',
    '.so',
    '.o',
    '.a',
    '.dll',
    '.exe'
}

NON_SOURCE_DIRECTORIES = {
    '.git',
    '.gradle',
    'build',
    'out',
    'target',
    'bin',
    'generated',
    'node_modules'
}

# check for source extensions
def is_source_file(filename):
    filename = filename.replace('\\', '/')

    # check if directory includes non source
    path_parts = filename.split('/')
    for directory in path_parts[:-1]:
        if directory in NON_SOURCE_DIRECTORIES:
            return False
    # get file extension
    extension = os.path.splitext(filename)[1].lower()

    # if not source extension then false
    if extension in NON_SOURCE_EXTENSIONS:
        return False

    # if source extension then return
    return extension in SOURCE_EXTENSIONS

# @branch, default branch of repo
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
# Collect source files from the repository
def collect_source_files(repo, branch, lsttokens):
    source_files = []
    ct = 0
    page = 1

    while True:
        url = (
            'https://api.github.com/repos/' + repo +
            '/git/trees/' + branch +
            '?recursive=1'
        )

        treeData, ct = github_auth(url, lsttokens, ct)

        if treeData is None:
            break

        if 'tree' not in treeData:
            break

        for item in treeData['tree']:
            if item['type'] == 'blob':
                filename = item['path']

                if is_source_file(filename):
                    source_files.append(filename)

        break

    return source_files


# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiletouches(sourcefiles, lsttokens, repo, branch):
    ct = 0  # token counter

    for filename in sourcefiles:
        print("-------------------------------------")
        print("File: " + filename)

        ipage = 1
        authors = set()
        dates = []
        count = 0
        # avoid merged commits
        duplicates = set()

        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?sha=' + branch + '&path=' + filename + '&page=' + spage + '&per_page=100'
            commits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(commits) == 0:
                break
            # iterate through the list of commits in  spage
            for commit in commits:
                sha = commit['sha']
                if sha in duplicates:
                    continue
                parents = commit.get('parents', [])

                if len(parents) > 1:
                    print("skipped commit")
                    continue
                duplicates.add(sha)
                count += 1
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']
                authors.add(author)
                dates.append(date)
            
            ipage += 1

        print("Authors:")
        for author in authors:
            print(author)

        print("Dates:")
        for date in dates:
            print(date)

        print("Number of changes: " + str(count))
# GitHub repo
repo = 'scottyab/rootbeer'

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
print("User Token: ")
lstTokens = [input()]

# get default  branch of repo
default_branch, languages, ct = get_repo_info(repo, lstTokens, 0)

print("\nDefault branch: " + default_branch)

# get source files
source_files = collect_source_files(repo, default_branch, lstTokens)

# displays full info on file touches
countfiletouches(source_files, lstTokens, repo, default_branch)