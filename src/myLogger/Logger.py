import logging


def getLogger(name: str, level: int = logging.INFO):
    logging.addLevelName(levelName=logging.getLevelName(level), level=level)
    return logging.getLogger(name)
