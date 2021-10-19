import logging
import logging.config
import yaml

with open('./logger_config.yaml', 'r') as stream:
    logger_config = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(logger_config)
logger = logging.getLogger('default')
