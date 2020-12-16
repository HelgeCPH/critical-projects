from critical_projects import INCLUDED_PLATFORMS


if __name__ == "__main__":
    for platform in INCLUDED_PLATFORMS:
        cql = (
            f'CALL gds.graph.create("{platform.lower()}_pr_graph",'
            + f' "{platform}", "*");'
        )
        print(cql)
    print()

    for platform in INCLUDED_PLATFORMS:
        cql = (
            f'CALL gds.pageRank.write("{platform.lower()}_pr_graph", {{'
            + "maxIterations: 20, dampingFactor: 0.85,"  # Default values
            + 'writeProperty: "pagerank"}) '
            + "YIELD nodePropertiesWritten, ranIterations;"
        )
        print(cql)
