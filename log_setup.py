import logging
import logging.config
import yaml

with open('./logger_config.yaml', 'r') as stream:
    logger_config: dict = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(logger_config)
logger: logging.Logger = logging.getLogger('default')
