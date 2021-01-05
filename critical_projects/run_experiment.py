import csv
import numpy as np
import pandas as pd
from critical_projects import (
    EXPERIMENT_PLATFORMS,
    NUMBER_OF_PROJECTS,
    NUMBER_OF_TF_PROJECTS,
)
from truckfactor.compute import main as tf_compute
from criticality_score.run import get_repository, get_repository_stats
import multiprocessing as mp
from itertools import product



RESULTS_FILE = "data/output/comparison.csv"
TF_PROJECT_CACHE = {}
COLUMNS=(
            (
                "platform",
                "id",
                "name",
                "repo_url",
                "pagerank",
                "truckfactor",
                "criticality_score",
                "created_since(m)",
                "updated_since(m)",
                "contributor_count",
                "org_count",
                "commit_frequency(y)",
                "recent_releases_count(y)",
                "closed_issues_count(90d)",
                "updated_issues_count(90d)",
                "comment_frequency",
                "dependents_count",
            )
        )


def compute_project_results(platform, url, iD, name, pagerank):
    global TF_PROJECT_CACHE
    with open("/tmp/experiment.log", "a") as fp:
        fp.write(f"Processing {platform}'s {url}\n")

    if url != url:
        # Check if url != NaN since NaN objects have this property.
        # In case we do not know a repo_url for this project do not
        # compute a truck factor neither a criticality score
        tf = np.nan
        created_since = np.nan
        updated_since = np.nan
        contributor_count = np.nan
        org_count = np.nan
        commit_frequency = np.nan
        recent_releases_count = np.nan
        closed_issues_count = np.nan
        updated_issues_count = np.nan
        comment_frequency = np.nan
        dependents_count = np.nan
        criticality_score = np.nan
    else:
        try:
            # This is wrapped since the truckfactor computation cannot
            # handle non UTF-8 characters in file names and for example
            # the `cucumber` project contains such file names...

            if url in TF_PROJECT_CACHE:
                # Do not recompute is for projects for which we have
                # done it already. Since multiple packages can be build
                # from one Git repository
                truckfactor = TF_PROJECT_CACHE[url]
            else:
                truckfactor, _ = tf_compute(url, is_url=True)
                TF_PROJECT_CACHE[url] = truckfactor
            tf = truckfactor

        except Exception as e:
            print(e)
            tf = np.nan

        try:
            repo = get_repository(url)
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
            created_since = np.nan
            updated_since = np.nan
            contributor_count = np.nan
            org_count = np.nan
            commit_frequency = np.nan
            recent_releases_count = np.nan
            closed_issues_count = np.nan
            updated_issues_count = np.nan
            comment_frequency = np.nan
            dependents_count = np.nan
            criticality_score = np.nan

    with open("/tmp/experiment.log", "a") as fp:
        fp.write(f"Done with {platform}'s {url}\n")

    row = (
        platform,
        iD,
        name,
        url,
        pagerank,
        tf,
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
    with open("/tmp/experiment.csv", "a") as fp:
        csvwriter = csv.writer(fp)  
        csvwriter.writerow(row)  
    return row


def compute_platform_results(platform):
    fname = f"data/output/{platform.lower()}_top_{NUMBER_OF_PROJECTS}.csv"
    df = pd.read_csv(fname)
    if 0 <= NUMBER_OF_TF_PROJECTS < df.shape[0]:
        mini_df = df[:NUMBER_OF_TF_PROJECTS]
    else:
        mini_df = df
    
    ids = list(mini_df.id.values)
    names = list(mini_df.name.values)
    urls = list(mini_df.repo_url.values)
    pageranks = list(mini_df.pagerank.values)
    platforms = (platform, ) * len(urls) 
    
    args = zip(platforms, urls, ids, names, pageranks)
    results = []
    for arguments in args:
        results.append(compute_project_results(*arguments))
    store_csv(results, platform)

    return results

def store_csv(results, platform):
    res_df = pd.DataFrame(results, columns=COLUMNS)
    res_df.to_csv(f"data/output/results_{platform}.csv", index=False)


def main():
    with open("/tmp/experiment.csv", "w") as fp:
        csvwriter = csv.writer(fp)  
        csvwriter.writerow(COLUMNS)

    results = []
    pool = mp.Pool(processes=mp.cpu_count())

    # for platform in EXPERIMENT_PLATFORMS[:2]:
    results = pool.map(compute_platform_results, EXPERIMENT_PLATFORMS)
    # flatten the resulting list of lists
    results = [el for platform_results in results for el in platform_results]
    print(results)


def results_to_adoc():
    with open(RESULTS_FILE) as fp:
        csv_contents = fp.read()

    with open("data/output/comparison.adoc", "w") as fp:
        contents = f"""= Results

[format="csv", options="header"]
|===
{csv_contents}
|=== """
        fp.write(contents)


if __name__ == "__main__":
    main()
    results_to_adoc()
