from logging import DEBUG, Formatter, StreamHandler, getLogger
from sys import stdout

getLogger('gunicorn').disabled = True
getLogger('gunicorn').propagate = False

logger = getLogger('werkzeug')
logger.propagate = False
logger.handlers.clear()
formatter = Formatter(
    fmt="[%(asctime)s][%(filename)s][%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
handler = StreamHandler(stdout)
handler.setLevel(DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)
