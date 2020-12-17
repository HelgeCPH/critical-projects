[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3626071.svg)](https://doi.org/10.5281/zenodo.3626071)


The data source by for this project is the [libraries.io](https://libraries.io/data) project [DOI](https://doi.org/10.5281/zenodo.3626071). 

Proper attribution:
Includes data from Libraries.io, a project from Tidelift





The main file to run to recreate the dataset locally is in `create_db.sh`


# Recreating the dataset

## Requirements

  * Linux/Unix OS (tested on MacOS Mojave only)
  * Bash shell interpreter
  * 300GB of free disk space should be enough
  * Docker needs to be installed and setup on your system
  * `pyenv` and `poetry` for dependency and virtual environment
  * `wget` and `unzip` need to be installed and available on the `$PATH`
  * Internet connection
  * ...time... the entire process of dataset creating takes some hours

## Configuration

In case you are running Docker on MacOS instead of Linux, you have to increase the max amount of memory from the default 2GB:
![](images/docker_memory_conf.png)


## 

Running the following script recreates the dataset and computes the page rank for the dependency graph:

```bash
$ poetry shell 
(critical-projects-kuSPJuld-py3.9) bash-3.2$ ./create_db.sh
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

