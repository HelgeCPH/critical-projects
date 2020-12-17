import os
import csv
from neo4j import GraphDatabase
from critical_projects import INCLUDED_PLATFORMS, NUMBER_OF_PROJECTS


uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))


def report(tx, platform, limit):
    query = f"""MATCH (n:{platform})
    RETURN ID(n), n.Name, n.pagerank, n.RepoURL
    ORDER BY n.pagerank DESC
    LIMIT {limit};"""
    result = tx.run(query)

    return [
        (r["ID(n)"], r["n.Name"], r["n.pagerank"], r["n.RepoURL"])
        for r in result
    ]


def main():

    with driver.session() as session:
        for platform in INCLUDED_PLATFORMS:
            result_str = session.read_transaction(
                report, platform, NUMBER_OF_PROJECTS
            )
            fname = f"{platform.lower()}_top_{NUMBER_OF_PROJECTS}.csv"
            outfile = os.path.join("data", "output", fname)
            with open(outfile, "w") as fp:
                csv_writer = csv.writer(fp)
                csv_writer.writerow(("id", "name", "pagerank", "repo_url"))
                for r in result_str:
                    csv_writer.writerow(r)

    driver.close()


if __name__ == "__main__":
    main()
