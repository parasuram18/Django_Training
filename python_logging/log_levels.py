import logging

# logging.basicConfig(filename='all.log',level=logging.DEBUG, format="%(asctime)s - %(levelname)s: %(message)s")
logging.basicConfig(filename='error.log',level=logging.ERROR, format="%(asctime)s - %(levelname)s: %(message)s")

logging.debug('This is the debug message')
logging.info('This is the info message')
logging.warning('This is the warning message')
logging.error('This is the error message')
logging.critical('This is the critical message')