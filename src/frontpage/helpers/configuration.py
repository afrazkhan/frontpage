from pathlib import Path
import yaml

def get_config(logger):
    """ Return configuration, if present """

    try:
        # TODO: Raise exception for file not found, as config_reader
        #       raises a section exception in that case, which is
        #       confusing
        with open(f"{Path.home()}/.config/frontpage.yaml", 'r') as config_file:
            config = yaml.safe_load(config_file)
    except Exception as e:
        logger.warn(f"Problem reading configuration: {e}")
        config = { 'log_level': 'ERROR' }

    return config
