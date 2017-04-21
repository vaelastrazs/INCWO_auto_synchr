from time import strftime
import logging


PATH = "logs" # EDITABLE : change for your own convenience
filename = strftime("%Y%m%d_%H")
LOG_LEVEL = logging.INFO # EDITABLE : change for your own convenience


# create logger with 'spam_application'
logger = logging.getLogger('Incwo_Updater')
logger.setLevel(LOG_LEVEL)
# create file handler which logs even debug messages

fh = logging.FileHandler(PATH+"/"+filename+'.log')
fh.setLevel(LOG_LEVEL)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

def error(error_msg):
    logger.error(error_msg)

def warning(msg):
    logger.warning(msg)    
    
def info(msg):
    logger.info(msg)
    
def debug(debug_msg):
    logger.debug(debug_msg)


