from time import gmtime, strftime
import sys
import os

error_file = "logs/error.txt"
debug_file = "logs/debug.txt"

import logging
import auxiliary_module

# create logger with 'spam_application'
logger = logging.getLogger('Incwo_Updater')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('logs/spam.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

def error(error_msg):
    logger.error(error_msg)
    
def debug(debug_msg):
    logger.debug(debug_msg)
    
def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

