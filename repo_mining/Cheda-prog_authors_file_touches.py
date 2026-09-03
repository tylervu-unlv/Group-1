import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

REPO = "scottyab/rootbeer"

# Same source-file definition as Cheda-prog_collect_files.py: hand-written
# Java/Kotlin source only, excluding build/generated output.
SOURCE_EXTENSIONS = (".java", ".kt")
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
    repoData = github_get("https://api.github.com/repos/" + repo, token)
    return repoData["default_branch"]


def is_source_file(filename):
    if not filename.lower().endswith(SOURCE_EXTENSIONS):
        return False
    lower_name = filename.lower()
    return not any(part in lower_name for part in EXCLUDED_DIR_PARTS)


def get_commit_author(shaDetails):
    # Prefer the GitHub login (stable handle); fall back to the raw commit
    # author name if the commit isn't linked to a GitHub account.
    author = shaDetails.get("author")
    if author and author.get("login"):
        return author["login"]
    commit_author = shaDetails.get("commit", {}).get("author", {})
    return commit_author.get("name", "unknown")


def get_commit_date(shaDetails):
    return shaDetails.get("commit", {}).get("author", {}).get("date")


# Collects, for every source file touched in the repo:
#   path, list of (author, date) touches
def collect_touches(token, repo, branch):
    # file path -> list of {"author": ..., "date": ...} dicts, one per touch
    file_touches = {}
    ipage = 1

    while True:
        commitsUrl = (
            "https://api.github.com/repos/" + repo
            + "/commits?sha=" + branch
            + "&page=" + str(ipage) + "&per_page=100"
        )
        jsonCommits = github_get(commitsUrl, token)
        if len(jsonCommits) == 0:
            break

        for shaObject in jsonCommits:
            sha = shaObject["sha"]
            shaUrl = "https://api.github.com/repos/" + repo + "/commits/" + sha
            shaDetails = github_get(shaUrl, token)

            author = get_commit_author(shaDetails)
            date = get_commit_date(shaDetails)

            for filenameObj in shaDetails.get("files", []):
                filename = filenameObj["filename"]
                if not is_source_file(filename):
                    continue
                file_touches.setdefault(filename, []).append({"author": author, "date": date})
                print(filename, author, date)

        ipage += 1

    return file_touches


def main():
    token = get_token()
    branch = get_default_branch(REPO, token)
    print("Default branch for {}: {}".format(REPO, branch))

    file_touches = collect_touches(token, REPO, branch)

    repo_name = REPO.split("/")[1]
    fileOutput = "data/authors_file_touches_" + repo_name + ".csv"
    with open(fileOutput, "w", newline="") as fileCSV:
        writer = csv.writer(fileCSV)
        writer.writerow(["Filename", "Author", "Date", "TouchCountForFile"])
        for filename, touches in file_touches.items():
            touch_count = len(touches)
            for touch in touches:
                writer.writerow([filename, touch["author"], touch["date"], touch_count])

    print("Wrote touch data for {} source files to {}".format(len(file_touches), fileOutput))


if __name__ == "__main__":
    main()
