from controllers.controller_main import Controller
from constants import DB_FILE_NAME
import logging

logging.basicConfig(filename="debug.log",
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


""" This is where the main application is run from. """


def main():
    """ Creates logger object, instantiates Controller,
    then starts Application."""
    logger = logging.getLogger(__name__)
    logger.info("Starting Application")

    controller = Controller(DB_FILE_NAME)
    controller.start()


if __name__ == "__main__":
    main()
