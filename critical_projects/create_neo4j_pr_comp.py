from critical_projects import INCLUDED_PLATFORMS


if __name__ == "__main__":
    for platform in INCLUDED_PLATFORMS:
        cql = (
            f'CALL gds.graph.create("{platform.lower()}_pr_graph",'
            + f' "{platform}", "*")'
        )
        print(cql)
    print()

    for platform in INCLUDED_PLATFORMS:

        # cql = (
        #     f'CALL gds.pageRank.stream("{platform.lower()}_pr_graph")\n'
        #     + "YIELD nodeId, score\n"
        #     + "RETURN gds.util.asNode(nodeId).Name AS name, score\n"
        #     + "ORDER BY score DESC, name ASC\n"
        # )
        cql = (
            f'CALL gds.pageRank.write("{platform.lower()}_pr_graph", {{'
            + "maxIterations: 20, dampingFactor: 0.85,"
            + 'writeProperty: "pagerank"})\n'
            + "YIELD nodePropertiesWritten, ranIterations"
        )
        print(cql)
