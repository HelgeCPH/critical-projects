#!/usr/bin/env bash




python -c"import psutil,sys;sys.exit() if 184 < psutil.disk_usage('/').free / (1024.0 ** 3) else sys.exit(1)"
if [ $? -ne 0 ]
then
  echo "You need around 184GB of free disk space for this operation to succeed" >&2
  exit 1
fi

echo "The following will take some time! Go do something else..."
echo "" 
echo "Downloading the dataset..."
wget --no-check-certificate -P ./data/input https://zenodo.org/record/3626071/files/libraries-1.6.0-2020-01-12.tar.gz
echo "Extracting the dataset..."
# Extract only the projects and the dependencies file for this project
tar -zxvf data/input/libraries-1.6.0-2020-01-12.tar.gz libraries-1.6.0-2020-01-12/projects-1.6.0-2020-01-12.csv
tar -zxvf data/input/libraries-1.6.0-2020-01-12.tar.gz libraries-1.6.0-2020-01-12/dependencies-1.6.0-2020-01-12.csv

mv libraries-1.6.0-2020-01-12/*.csv ./data/input
rm -r libraries-1.6.0-2020-01-12/

grep "KEEP_ORIG_DATA: FALSE" analysis_conf.yml
if [ $? -eq 0 ]
then
  echo "Deleting libraries.io dataset"
  rm libraries-1.6.0-2020-01-12.tar.gz
fi


echo "Generating Neo4j input data..."
python -m critical_projects.projects_to_neo4j_csv data/input/projects-1.6.0-2020-01-12.csv > data/processing/projects_neo4j.csv
python -m critical_projects.deps_to_neo4j_csv data/input/dependencies-1.6.0-2020-01-12.csv > data/processing/deps_neo4j.csv

echo "Generating cypher queries..."
python -m critical_projects.create_neo4j_indexes > data/processing/create_indexes.cql
python -m critical_projects.create_neo4j_pr_comp > data/processing/compute_pagerank.cql


echo "Setting up Neo4j DB..."
# Getting the Neo4j plugin with the PageRank algorithm
wget --no-check-certificate -P ./neo4j/plugins https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/graph-data-science/neo4j-graph-data-science-1.4.1-standalone.zip
unzip ./neo4j/plugins/neo4j-graph-data-science-1.4.1-standalone.zip -d ./neo4j/plugins
rm ./neo4j/plugins/neo4j-graph-data-science-1.4.1-standalone.zip


# Starting container for DBMS
docker run \
    --name depgraphneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $(pwd)/neo4j/data:/data \
    -v $(pwd)/neo4j/logs:/logs \
    -v $(pwd)/data/processing:/var/lib/neo4j/import \
    -v $(pwd)/neo4j/plugins:/plugins \
    --env NEO4J_dbms_memory_heap_initial__size=1G \
    --env NEO4J_dbms_memory_heap_max__size=1G \
    --env NEO4J_dbms_security_procedures_unrestricted=gds.\\\* \
    --env NEO4J_AUTH=neo4j/password \
    neo4j:4.2

echo "Importing data..."
docker exec depgraphneo4j neo4j stop
sleep 2
# Do not connect the browser UI to the DB before this step, otherwise it will not work due to a locked DB!
# The import takes long, on a MacBook Pro 2017 with 2,9 GHz i7, it takes almost 50min.
docker exec depgraphneo4j neo4j-admin import \
    --nodes=/var/lib/neo4j/import/projects_neo4j.csv \
    --relationships=/var/lib/neo4j/import/deps_neo4j.csv \
    --skip-bad-relationships
sleep 20
docker container restart depgraphneo4j
sleep 20
docker exec depgraphneo4j neo4j start
sleep 20
# Creating indexes on Names field, not sure if that is really needed but good for experimenting
docker exec depgraphneo4j cypher-shell -u neo4j -p password -f /var/lib/neo4j/import/create_indexes.cql



echo "Computing PageRank..."
docker exec depgraphneo4j cypher-shell -u neo4j -p password -f /var/lib/neo4j/import/compute_pagerank.cql



python -m critical_projects.generate_pr_reports


# CALL dbms.listConfig("heap");