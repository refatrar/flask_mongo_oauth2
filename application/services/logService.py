import logging


class LOG:
    @staticmethod
    def report(err: Exception):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %P', filename="logs/logger.log")
        logging.exception(str(err))
