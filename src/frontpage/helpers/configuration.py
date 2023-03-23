import configparser

def get_config(logger):
    """ Return configuration, if present """

    try:
        config_reader = configparser.ConfigParser()
        config_reader.read('/Users/afraz/.config/frontpage.inis')
        config = dict(config_reader.items('default'))
    except configparser.NoSectionError as e:
        logger.warn(f"Problem reading configuration: {e}")
        config = { 'log_level': 'ERROR' }

    return config
