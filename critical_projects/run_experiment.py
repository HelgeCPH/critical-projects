import numpy as np
import pandas as pd
from critical_projects import EXPERIMENT_PLATFORMS, NUMBER_OF_PROJECTS
from truckfactor.compute import main as tf_compute
from criticality_score.run import get_repository, get_repository_stats


def main():
    tfs = []
    platforms = []
    ids = []
    names = []
    urls = []
    pageranks = []

    created_sinces = []
    updated_sinces = []
    contributor_counts = []
    org_counts = []
    commit_frequencies = []
    recent_releases_counts = []
    closed_issues_counts = []
    updated_issues_counts = []
    comment_frequencies = []
    dependents_counts = []
    criticality_scores = []

    for platform in EXPERIMENT_PLATFORMS:
        fname = f"data/output/{platform.lower()}_top_{NUMBER_OF_PROJECTS}.csv"
        df = pd.read_csv(fname)

        mini_df = df[:20]
        ids += list(mini_df.id.values)
        names += list(mini_df.name.values)
        urls += list(mini_df.repo_url.values)
        pageranks += list(mini_df.pagerank.values)
        for url in mini_df.repo_url:
            print(f"Processing {platform}'s {url}")
            platforms.append(platform)

            if url != url:
                # Check if url != NaN since NaN objects have this property.
                # In case we do not know a repo_url for this project do not
                # compute a truck factor neither a criticality score
                tfs.append(np.nan)
                created_sinces.append(np.nan)
                updated_sinces.append(np.nan)
                contributor_counts.append(np.nan)
                org_counts.append(np.nan)
                commit_frequencies.append(np.nan)
                recent_releases_counts.append(np.nan)
                closed_issues_counts.append(np.nan)
                updated_issues_counts.append(np.nan)
                comment_frequencies.append(np.nan)
                dependents_counts.append(np.nan)
                criticality_scores.append(np.nan)
            else:
                try:
                    # This is wrapped since the truckfactor computation cannot
                    # handle non UTF-8 characters in file names and for example
                    # the `cucumber` project contains such file names...
                    truckfactor = tf_compute(url, is_url=True)
                    tfs.append(truckfactor)
                except Exception as e:
                    print(e)
                    tfs.append(np.nan)

                try:
                    repo = get_repository(url)
                    output = get_repository_stats(repo)

                    created_sinces.append(output["created_since"])
                    updated_sinces.append(output["updated_since"])
                    contributor_counts.append(output["contributor_count"])
                    org_counts.append(output["org_count"])
                    commit_frequencies.append(output["commit_frequency"])
                    recent_releases_counts.append(
                        output["recent_releases_count"]
                    )
                    closed_issues_counts.append(output["closed_issues_count"])
                    updated_issues_counts.append(output["updated_issues_count"])
                    comment_frequencies.append(output["comment_frequency"])
                    dependents_counts.append(output["dependents_count"])
                    criticality_scores.append(output["criticality_score"])
                except Exception as e:
                    print(e)
                    created_sinces.append(np.nan)
                    updated_sinces.append(np.nan)
                    contributor_counts.append(np.nan)
                    org_counts.append(np.nan)
                    commit_frequencies.append(np.nan)
                    recent_releases_counts.append(np.nan)
                    closed_issues_counts.append(np.nan)
                    updated_issues_counts.append(np.nan)
                    comment_frequencies.append(np.nan)
                    dependents_counts.append(np.nan)
                    criticality_scores.append(np.nan)
    res_df = pd.DataFrame(
        list(
            zip(
                platforms,
                ids,
                names,
                urls,
                created_sinces,
                updated_sinces,
                contributor_counts,
                org_counts,
                commit_frequencies,
                recent_releases_counts,
                closed_issues_counts,
                updated_issues_counts,
                comment_frequencies,
                dependents_counts,
                criticality_scores,
                pageranks,
                tfs,
            )
        ),
        columns=(
            (
                "platform",
                "id",
                "name",
                "repo_url",
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
                "criticality_score",
                "pagerank",
                "truckfactor",
            )
        ),
    )
    res_df.to_csv("data/output/comparison.csv", index=False)


def oi():
    {
        "java": "Maven",
        "js": "NPM",
        "php": "Packagist",
        "python": "Pypi",
        "rust": "Cargo",
    }
    for platform in ["java", "js", "php", "python", "rust"]:
        fname = f"data/input/{platform}_top_200.csv"

        df = pd.read_csv(fname)
        mini_df = df[:20]


if __name__ == "__main__":
    main()
