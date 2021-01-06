#!/usr/bin/env bash

# rm /tmp/experiment_repo_urls.txt
NO_PROJ=`grep "NUMBER_OF_PROJECTS:" analysis_conf.yml | cut -d":" -f2 | xargs`
NO_TF_PROJ=`grep "NUMBER_OF_TF_PROJECTS:" analysis_conf.yml | cut -d":" -f2 | xargs`
# Run the experiment for Cargo, Maven, NPM, Packagist, Pypi
for f in "data/output/cargo_top_${NO_PROJ}.csv" \
         "data/output/maven_top_${NO_PROJ}.csv" \
         "data/output/npm_top_${NO_PROJ}.csv" \
         "data/output/packagist_top_${NO_PROJ}.csv" \
         "data/output/pypi_top_${NO_PROJ}.csv"
do
    # The CSV files are sorted by PageRank, therefore, the head is okay for this
    # experiment
    tail -n +2 $f | head -${NO_TF_PROJ} | cut -d"," -f4 >> /tmp/experiment_repo_urls.txt
done
                                                  
cat /tmp/experiment_repo_urls.txt | \
    sort | \
    uniq | \
    # Remove empty line
    grep '\S' | \
    # We cannot compute Truck Factor for SVN repositories, so exclude them
    grep -v 'https\?://svn\.' | \
    # There are no longer repositories hosted at Google Code
    grep -v 'code\.google\.com' | \
    # Some of the repositories have this string prepended to the Git URL
    sed 's/scm:git://' | \
    xargs -P 4 -n 1 python -m critical_projects.compute_results


python -m critical_projects.merge_result_csvs
# asciidoctor data/output/comparison.adoc
