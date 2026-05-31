import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("--log", default="WARNING")

args = parser.parse_args()

numeric_level = logging.getLevelNamesMapping().get(args.log.upper())
if numeric_level is None:
    raise ValueError(f"Invalid log level: {args.log}")

logging.basicConfig(filename="log_events.log", encoding="utf_8", level=numeric_level)

logging.basicConfig(filename="log_events.log", filemode="w", encoding="utf_8", level=logging.INFO)


logger = logging.getLogger(__name__)


logger.debug("This message should go to the log file")
logger.info("So should this")
logger.warning("And this, too")
logger.error("And non-ASCII stuff, too, like Øresund and Malmö")

logger.warning("%s before you %s", "Look", "leap!")
