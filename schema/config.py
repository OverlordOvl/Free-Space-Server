import configparser
import os

config = configparser.RawConfigParser()
config_file = os.environ.get('SCHEMA_INI', os.path.join(os.path.dirname(__file__), 'schema.ini'))
config.read_file(open(config_file))
