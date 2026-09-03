import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub repo to analyze
REPO = "scottyab/rootbeer"

# Source file extensions we consider "source code" for this repo.
# rootbeer is a Java/Kotlin Android library, so we keep .java and .kt.
# Excluded on purpose: .xml (Android resources/manifests/build config),
# .gradle/.properties (build config), .md (docs), images, and anything
# under generated/build directories.
SOURCE_EXTENSIONS = (".java", ".kt")

# Directories that never contain hand-written source, even if a stray
# .java/.kt file ends up there (generated code, build output, etc.)
EXCLUDED_DIR_PARTS = ("build/", "/build/", "generated/", ".gradle/")


def get_token():
    token = os.environ.get("GITHUB_PAT")
    if not token:
        token = input("Enter your GitHub personal access token: ").strip()
    if not token:
        raise SystemExit("A GitHub token is required (env var GITHUB_PAT or prompt).")
    return token


def github_get(url, token):
    headers = {"Authorization": "Bearer {}".format(token)}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return json.loads(response.content)


def get_default_branch(repo, token):
    repoUrl = "https://api.github.com/repos/" + repo
    repoData = github_get(repoUrl, token)
    return repoData["default_branch"]


def is_source_file(filename):
    if not filename.lower().endswith(SOURCE_EXTENSIONS):
        return False
    lower_name = filename.lower()
    return not any(part in lower_name for part in EXCLUDED_DIR_PARTS)


# @dictfiles, empty dictionary of files -> touch count
# @token, GitHub authentication token
# @repo, GitHub repo
# @branch, default branch to pull commits from
def countfiles(dictfiles, token, repo, branch):
    ipage = 1  # url page counter

    while True:
        spage = str(ipage)
        commitsUrl = (
            "https://api.github.com/repos/" + repo
            + "/commits?sha=" + branch
            + "&page=" + spage + "&per_page=100"
        )
        jsonCommits = github_get(commitsUrl, token)

        # break out of the loop if there are no more commits in the page
        if len(jsonCommits) == 0:
            break

        for shaObject in jsonCommits:
            sha = shaObject["sha"]
            # For each commit, use the GitHub commit API to extract the files touched
            shaUrl = "https://api.github.com/repos/" + repo + "/commits/" + sha
            shaDetails = github_get(shaUrl, token)
            for filenameObj in shaDetails.get("files", []):
                filename = filenameObj["filename"]
                if not is_source_file(filename):
                    continue
                dictfiles[filename] = dictfiles.get(filename, 0) + 1
                print(filename)
        ipage += 1


def main():
    token = get_token()
    branch = get_default_branch(REPO, token)
    print("Default branch for {}: {}".format(REPO, branch))

    dictfiles = dict()
    countfiles(dictfiles, token, REPO, branch)
    print("Total number of source files touched: " + str(len(dictfiles)))

    repo_name = REPO.split("/")[1]
    fileOutput = "data/file_" + repo_name + ".csv"
    with open(fileOutput, "w", newline="") as fileCSV:
        writer = csv.writer(fileCSV)
        writer.writerow(["Filename", "Touches"])

        bigcount = None
        bigfilename = None
        for filename, count in dictfiles.items():
            writer.writerow([filename, count])
            if bigcount is None or count > bigcount:
                bigcount = count
                bigfilename = filename

    if bigfilename is not None:
        print("The file " + bigfilename + " has been touched " + str(bigcount) + " times.")


if __name__ == "__main__":
    main()
