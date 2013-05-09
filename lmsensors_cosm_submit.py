#!/usr/bin/env python2.7
"""
This script will read sensor values using sensors data and will post to COSM.com

It is using cosm.cfg which is JSON dictionary with following fields:

{
"key":"your key"
"feed":123
}
"""

import json
import sys
import logging
import time,datetime
import string
import getopt
import cosm
import sensors

CFG_FILE="cosm.cfg"
COSM_LOGFILE="cosm.log"

def usage():
    print """
%s [-f <cfg file>] [-c] [-d] 

-c -- log to console instead of log file
-d -- dry-run mode. No data submitted.
-f <cfg file> -- config file name. Default is '%s'

"""  % (sys.argv[0],CFG_FILE,DATA_FILE)

def read_config(cfg_fname):
    log.info("Reading config file %s" % cfg_fname)
    f=open(cfg_fname,"r")
    try:
        return json.load(f)
    finally:
        f.close()

def main():
    global log
    global debug_mode = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dcf:', [])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    console = False
    debug_mode = False
    cfg_fname = CFG_FILE
    data_fname = DATA_FILE
    sleep_time = 0 # non zero means loop mode
    
    for o, a in opts:
        if o in ['-d']:
            debug_mode = True
        elif o in ['-c']:
            console = True
        elif o in ['-f']:
            cfg_fname = a
        else:
            usage()
            sys.exit(1)

    log_format = '%(asctime)s %(process)d %(filename)s:%(lineno)d %(levelname)s %(message)s'
    if debug_mode:
        log_level=logging.DEBUG
    else:
        log_level=logging.INFO
    if console:
        logging.basicConfig(level=log_level, format=log_format)
    else:
        logging.basicConfig(level=log_level, format=log_format,
                            filename=COSM_LOGFILE, filemode='a')
    log = logging.getLogger('default')

    try:
        cfg = read_config(cfg_fname)
    except Exception, ex:
        log.error("Error reading config file %s" % ex)
        sys.exit(1)
        
    feed = cfg["feed"]
    key  = cfg["key"]
    log.info("Using feed %s" % feed)

    try:
        try:
            sensors.init()
        except Exception, ex:
            log.error("Error initializing sensors: %s" % ex )
            sys.exit(200)
            
        try:
            if not debug_mode:
                cosm.submit_datapoints(feed,ch,key,temps[ch])
        except Exception, ex:
            log.error("Error sending to COSM: %s" % ex )
            sys.exit(100)
        finally:
                f.close()
    finally:
             sensors.cleanup()
    log.debug("Done")


if __name__ == '__main__':
    main()
