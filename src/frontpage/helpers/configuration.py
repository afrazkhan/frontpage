import configparser
from pathlib import Path

def get_config(logger):
    """ Return configuration, if present """

    try:
        config_reader = configparser.ConfigParser()
        # TODO: Raise exception for file not found, as config_reader
        #       raises a section exception in that case, which is
        #       confusing
        config_reader.read(f"{Path.home()}/.config/frontpage.ini")
        config = dict(config_reader.items('default'))
    except configparser.NoSectionError as e:
        logger.warn(f"Problem reading configuration: {e}")
        config = { 'log_level': 'ERROR' }

    return config
