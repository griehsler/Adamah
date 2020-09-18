from pathlib import Path


def ensure_directories(directories):
    for directory in directories:
        if not Path(directory).exists():
            Path(directory).mkdir()


def touch_file(file):
    if not Path(file).exists():
        Path(file).touch()
