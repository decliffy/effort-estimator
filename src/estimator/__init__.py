import logging
import sys

logger = logging.getLogger("estimator")

_handler = logging.StreamHandler(sys.stderr)
_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(_handler)
logger.setLevel(logging.WARNING)


def set_verbose(verbose: bool) -> None:
    if verbose:
        logger.setLevel(logging.DEBUG)
