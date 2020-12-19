import yaml


CONF_FILE = "analysis_conf.yml"

with open(CONF_FILE) as fp:
    conf = yaml.safe_load(fp)


INCLUDED_PLATFORMS = conf["INCLUDED_PLATFORMS"]
KEEP_ORIG_DATA = conf["KEEP_ORIG_DATA"]
NUMBER_OF_PROJECTS = conf["NUMBER_OF_PROJECTS"]
EXPERIMENT_PLATFORMS = conf["EXPERIMENT_PLATFORMS"]
