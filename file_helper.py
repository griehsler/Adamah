from pathlib import Path
import json


def ensure_directories(directories):
    for directory in directories:
        if not Path(directory).exists():
            Path(directory).mkdir()


def touch_file(file):
    if not Path(file).exists():
        Path(file).touch()


def dump_json(document, filename):
    f = open(filename, "w")
    json.dump(document, f)
    f.close()
