import yaml


CONF_FILE = "analysis_conf.yml"

with open(CONF_FILE) as fp:
    conf = yaml.safe_load(fp)


INCLUDED_PLATFORMS = conf["INCLUDED_PLATFORMS"]
KEEP_ORIG_DATA = conf["KEEP_ORIG_DATA"]
