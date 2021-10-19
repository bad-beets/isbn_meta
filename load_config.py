import os
import configparser

cfg = configparser.ConfigParser(os.environ)
cfg.read('config.ini')

assert cfg['gobo_params']['key'], 'Google Books API Key required.'
assert cfg['isbndb_headers']['Authorization'], 'ISBNDB API Key required.'
