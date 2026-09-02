from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")  # take environment variables from .env.local
import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

GITHUB_PAT = os.getenv("GITHUB_PAT")

# Mapping of file extensions to programming languages
LANGUAGE_MAP = {
    '.java': 'Java',
    '.kt': 'Kotlin',
    '.c': 'C',
    '.cpp': 'C++',
    '.cc': 'C++',
    '.h': 'C/C++ Header',
    '.hpp': 'C++',
    '.aidl': 'AIDL',
    '.xml': 'XML',
    '.py': 'Python',
    '.pyx': 'Cython',
    '.js': 'JavaScript',
    '.jsx': 'JavaScript/JSX',
    '.ts': 'TypeScript',
    '.tsx': 'TypeScript/TSX',
    '.go': 'Go',
    '.rs': 'Rust',
    '.scala': 'Scala',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.swift': 'Swift',
    '.m': 'Objective-C',
    '.mm': 'Objective-C++',
    '.cs': 'C#',
    '.java': 'Java',
    '.gradle': 'Gradle',
    '.sh': 'Shell Script',
    '.bash': 'Bash',
    '.yml': 'YAML',
    '.yaml': 'YAML',
    '.json': 'JSON',
    '.toml': 'TOML',
}

# Paths to exclude (build outputs, generated files, etc.)
EXCLUDED_PATHS = {
    '/build/', '/.gradle/', '/bin/', '/gen/', '/obj/',
    '/dist/', '/out/', '/.idea/', '/.settings/',
    '/node_modules/', '/venv/', '/.venv/',
    '/vendor/', '/.git/', '/.github/',
    '/target/', '/Debug/', '/Release/',
    '/__pycache__/', '/.pytest_cache/', '/.mypy_cache/',
    '/coverage/', '/.tox/', '/site-packages/',
    '/generated/', '/generated-sources/',
}

# Function to determine if a file is a source file
def is_source_file(filename):
    """
    Filters for source files across multiple programming languages.
    Includes: .java, .kt, .py, .js, .ts, .go, .rs, .c, .cpp, .h, .xml, and more
    Excludes: build artifacts, generated files, dependencies, config files
    """
    # Check if file is in an excluded directory
    for excluded_path in EXCLUDED_PATHS:
        if excluded_path in filename:
            return False
    
    # Get file extension
    _, ext = os.path.splitext(filename)
    
    # Exclude files without extensions (build files, Makefiles, etc.)
    if not ext:
        return False
    
    return ext.lower() in LANGUAGE_MAP

# Function to get the default branch of the repository
def get_default_branch(repo, lsttokens):
    """
    Fetches the repository's default branch from GitHub API.
    """
    try:
        url = f'https://api.github.com/repos/{repo}'
        ct = 0
        ct = ct % len(lsttokens)
        headers = {'Authorization': f'Bearer {lsttokens[ct]}'}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        if 'default_branch' in jsonData:
            return jsonData['default_branch']
        else:
            print("Warning: Could not determine default branch, defaulting to 'main'")
            return 'main'
    except Exception as e:
        print(f"Error fetching default branch: {e}")
        return 'main'

# Function to identify programming languages used in the repository
def identify_languages(dictfiles):
    """
    Identifies all programming languages used in the repository based on file extensions.
    Returns a dictionary with language names and their file counts.
    """
    languages = {}
    for filename in dictfiles.keys():
        _, ext = os.path.splitext(filename)
        ext_lower = ext.lower()
        if ext_lower in LANGUAGE_MAP:
            language = LANGUAGE_MAP[ext_lower]
            if language not in languages:
                languages[language] = 0
            languages[language] += 1
    return languages

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
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # Only count if it's a source file
                    if is_source_file(filename):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
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
lstTokens = [GITHUB_PAT]

# Get the repository's default branch
print(f"Fetching repository information for {repo}...")
default_branch = get_default_branch(repo, lstTokens)
print(f"Default branch: {default_branch}")

dictfiles = dict()
print(f"Collecting source files from {repo}...")
countfiles(dictfiles, lstTokens, repo)
print(f'Total number of source files touched: {len(dictfiles)}')

# Identify programming languages used
print("\nIdentifying programming languages...")
languages = identify_languages(dictfiles)
print(f"Programming languages found ({len(languages)}):")
for language, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {language}: {count} files")

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
source_files_list = []
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    source_files_list.append(filename)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename
fileCSV.close()
print(f'\nThe file {bigfilename} has been touched {bigcount} times.')

# Output source files list to a separate file
source_files_output = 'data/source_files_list_' + file + '.txt'
with open(source_files_output, 'w') as f:
    f.write(f"Source Files Found in {repo}\n")
    f.write(f"Default Branch: {default_branch}\n")
    f.write(f"Total Source Files: {len(source_files_list)}\n")
    f.write(f"\nProgramming Languages:\n")
    for language, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        f.write(f"  - {language}: {count} files\n")
    f.write(f"\n{'='*80}\n")
    f.write(f"Complete List of Source Files:\n")
    f.write(f"{'='*80}\n")
    for i, filename in enumerate(sorted(source_files_list), 1):
        f.write(f"{i}. {filename}\n")

print(f"\nSource files list saved to: {source_files_output}")
