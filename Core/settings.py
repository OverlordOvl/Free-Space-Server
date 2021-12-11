import os
from pathlib import Path


FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
PARENT_PATH = str(Path(FILE_PATH).parent)

for string in open(f"{PARENT_PATH}/.env", 'r').readlines():
    if '=' in string:
        key, value = string.strip().replace("\n", '').split("=")
        if key:
            os.environ[key] = str(eval(value))

VERSION = 0.1
DB_NAME = "FreeSpace"

DATABASES = {
    "default": {
        "ENGINE":   "postgresql",
        "NAME":     "eshop",
        "HOST":     os.environ.get("DATABASE_HOST"),
        "USER":     os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "PORT":     os.environ.get("DATABASE_PORT"),
    },
}
