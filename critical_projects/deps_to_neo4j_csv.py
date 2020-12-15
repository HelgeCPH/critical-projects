"""
Call me like:
python -m critical_projects.deps_to_neo4j_csv data/input/dependencies-1.6.0-2020-01-12.csv > data/processing/deps_neo4j.csv


The argument to this script has to be a path the the dependiencies CSV file, e.g., 
`dependencies-1.6.0-2020-01-12.csv` from the libraries.io dataset.

See:
https://libraries.io/data
https://zenodo.org/record/3626071/files/libraries-1.6.0-2020-01-12.tar.gz

The description of the fields can be found here:
https://libraries.io/data#dependenciesFields
"""


import os
import csv
import sys
from critical_projects import INCLUDED_PLATFORMS


def main(fname):
    csv_writer = csv.writer(sys.stdout)

    header_line = ":START_ID,:END_ID,:TYPE,ThisVersion,VersionReq"
    print(header_line)
    with open(fname) as fp:
        csv_reader = csv.reader(fp, delimiter=",")
        next(csv_reader)  # Skip the header line
        for row in csv_reader:
            # ID,Platform,Project Name,Project ID,Version Number,Version ID,
            # Dependency Name,Dependency Platform,Dependency Kind,
            # Optional Dependency,Dependency Requirements,Dependency Project ID
            (
                _,
                platform,
                _,
                project_id,
                version_number,
                _,
                _,
                dep_platform,
                dependency_kind,
                _,  # Do I need info on optionality for something?
                dependency_requirements,
                dependency_project_id,
            ) = row
            if (
                dependency_project_id
                and platform in INCLUDED_PLATFORMS
                and dep_platform in INCLUDED_PLATFORMS
            ):
                csv_writer.writerow(
                    (
                        project_id,
                        dependency_project_id,
                        dependency_kind,
                        version_number,
                        dependency_requirements,
                    )
                )

    # INFO: dependency_project_id can be empty. In that case the dependency is
    # not known as a project. We could just keep these relations and let Neo4j
    # drop them on import, but to save disk space we remove them here directly.
    # Another way to handle these is to create a second node dataset for all of
    # these projects. We do not do this for this study.


if __name__ == "__main__":
    deps_csv_file = sys.argv[1]
    if os.path.isfile(deps_csv_file):
        main(deps_csv_file)
    else:
        print(__doc__)
