from time import gmtime, strftime
import sys
import os

error_file = "logs/error.txt"
debug_file = "logs/debug.txt"

def error(error_msg):
    log_msg(error_msg, error_file)
    
def debug(debug_msg):
    log_msg(debug_msg, debug_file)

def log_msg(msg, filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    t = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    if os.path.exists(filename):
        with open(filename, 'a') as fp:
            fp.write(t+' : '+msg+"\n")
            fp.close()
    
    else:
        with open(filename, 'w') as fp:
            fp.write(t+' : '+msg+"\n")
            fp.close()