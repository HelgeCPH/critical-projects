import os
import csv
import sys
from truckfactor.compute import main as tf_compute
from criticality_score.run import get_repository, get_repository_stats
from github.GithubException import UnknownObjectException


RESULTS_FILE = "data/output/tf_and_cs.csv"


def main(url):
    try:
        truckfactor, _ = tf_compute(url, is_url=True)
    except Exception as e:
        print(e)
        truckfactor = None

    try:
        repo = get_repository(url)
    except UnknownObjectException as e:
        # The criticality score computation cannot handle Git URLs as, e.g.,
        # https://github.com/sbt/junit-interface.git, which are in the 
        # libraries.io dataset in some cases
        repo = get_repository(url.replace(".git", ""))

    try:
        output = get_repository_stats(repo)

        created_since = output["created_since"]
        updated_since = output["updated_since"]
        contributor_count = output["contributor_count"]
        org_count = output["org_count"]
        commit_frequency = output["commit_frequency"]
        recent_releases_count = output["recent_releases_count"]
        closed_issues_count = output["closed_issues_count"]
        updated_issues_count = output["updated_issues_count"]
        comment_frequency = output["comment_frequency"]
        dependents_count = output["dependents_count"]
        criticality_score = output["criticality_score"]

    except Exception as e:
        print(e)
        created_since = None
        updated_since = None
        contributor_count = None
        org_count = None
        commit_frequency = None
        recent_releases_count = None
        closed_issues_count = None
        updated_issues_count = None
        comment_frequency = None
        dependents_count = None
        criticality_score = None

    row = (
        url,
        truckfactor,
        criticality_score,
        created_since,
        updated_since,
        contributor_count,
        org_count,
        commit_frequency,
        recent_releases_count,
        closed_issues_count,
        updated_issues_count,
        comment_frequency,
        dependents_count,
    )
    with open(RESULTS_FILE, "a") as fp:
        csvwriter = csv.writer(fp)  
        csvwriter.writerow(row)  

if __name__ == "__main__":
    main(sys.argv[1].strip())
