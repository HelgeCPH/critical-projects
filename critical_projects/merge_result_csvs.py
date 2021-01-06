import os
import csv
from critical_projects import (
    EXPERIMENT_PLATFORMS,
    NUMBER_OF_PROJECTS,
    NUMBER_OF_TF_PROJECTS,
)
from critical_projects.compute_results import RESULTS_FILE


DATA_PATH = "data/output/"
COMPARISON_FILE = os.path.join(DATA_PATH, "comparison.csv")
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


def read_experiment_results():
    results = {}
    with open(RESULTS_FILE) as fp:
        for row in csv.reader(fp):
            results[row[0]] = row[1:]

    return results


def main():
    results = read_experiment_results()
    new_lines = []
    for idx, platform in enumerate(EXPERIMENT_PLATFORMS):
        fname = os.path.join(DATA_PATH, f"{platform.lower()}_top_{NUMBER_OF_PROJECTS}.csv")
        with open(fname) as fp:
            contents = fp.readlines()
            contents = contents[1:NUMBER_OF_TF_PROJECTS + 1]
            new_lines += [platform + "," + l for l in contents]

    with open(COMPARISON_FILE, "w") as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow(COLUMNS)
        for row in csv.reader(new_lines):
            inorder_row = row[:3] + [row[-1], row[-2]]
            result_row = inorder_row + results.get(row[-1], [""]*12)
            csv_writer.writerow(result_row)


def results_to_adoc():
    with open(COMPARISON_FILE) as fp:
        csv_contents = fp.read()

    with open(COMPARISON_FILE.replace(".csv", ".adoc"), "w") as fp:
        contents = f"""= Results

[format="csv", options="header"]
|===
{csv_contents}
|=== """
        fp.write(contents)


if __name__ == '__main__':
    main()
    results_to_adoc()