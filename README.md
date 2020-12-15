


The main file to run to recreate the dataset locally is in `create_db.sh`


# Recreating the dataset

Running the following script recreates the dataset and computes the page rank for the dependency graph:

```bash
$ poetry shell 
(critical-projects-kuSPJuld-py3.9) ./create_db.sh
```

The script does the following:

  * Download the original dataset from libraries.io. Since it is 24GB in size, the download will take some time.
  * Unpack the dataset into a local directory `./libraries_io_data` The script will check that 184GB of disk space are available. If not it will stop.
  * Convert the data so that it can be imported to Neo4j
  * Setup the GraphDB Neo4j in a Docker container.
  * Import the dependency graph to Neo4j
  * Compute the page rank for the selected package managers, see


In case you want to experiment with the dependency graph in the database, connect to http://localhost:7474 and login as `admin` with the password `password`.


Note, the Docker container will store the actual database on the host machine in the directory `neo4j_data`, which will take multiple GB too. Remember to clean the data once you are done with your analysis.

# Requirements

  * Linux/Unix OS (tested only on MacOS Mojave)
  * Bash shell interpreter
  * 300GB of free disk space should be enough
  * Docker needs to be installed and setup on your system
  * pyenv and poetry for dependency and virtual environment
  * wget and unzip need to be installed and available on the `$PATH