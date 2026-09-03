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

# get the default branch name
def get_default_branch(repo, lsttokens):
    url = 'https://api.github.com/repos/' + repo
    jsonData, ct = github_auth(url, lsttokens, 0)

    if jsonData is not None:
        return jsonData['default_branch']

    return None

# file extensions that indicate source files in repository
SOURCE_EXTENSIONS = {
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.c': 'C',
    '.cpp': 'C++',
    '.h': 'Header',
    '.xml': 'XML'
}

# file extensions that are not source
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
# GitHub repo
repo = 'scottyab/rootbeer'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
print("User Token: ")
lstTokens = [input()]

# get default  branch of repo
default_branch = get_default_branch(repo, lstTokens)
# if no default branch
if default_branch is None:
    print("Default branch not found.")
    exit(0)

print("\nDefault branch: " + default_branch)

# get source files
source_files = collect_source_files(repo, default_branch, lstTokens)

# display programming languages found
languages = set()
# sorts/splits source files into languages
for filename in source_files:
    extension = os.path.splitext(filename)[1].lower()

    if extension in SOURCE_EXTENSIONS:
        languages.add(SOURCE_EXTENSIONS[extension])

print("\nProgramming languages used for source files:")
for language in sorted(languages):
    print(language)

# display source files chosen
print("\nSource files selected for analysis:")
for filename in sorted(source_files):
    print(filename)