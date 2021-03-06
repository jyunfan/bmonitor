#!/usr/bin/env python
# Retrieve status of miners in Bitcoin pools
# Result will be place in database

# std library
import ConfigParser
from datetime import datetime
import logging
import os
import pprint
import shelve
import subprocess
import sys
import time

import pools
import setting

HASH_RATE_THRESH = 1
PROG_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_FILE = os.path.join(PROG_DIR, '..', 'script', 'alert.sh')

# Logging
logger = logging.getLogger(__name__)

def read_config(filename):
    config = ConfigParser.ConfigParser()
    config.read(filename)

    return config._sections

# Get miner status of each pool
def get_status(config):
    d = shelve.open(setting.DB_FILE)

    for key in config.keys():
        miner = config[key]

        # pool name is mandatory
        poolname = miner.get('pool', None)
        if (None == poolname):
            logging.error('pool key is not specified')

        apikey = miner.get('apikey', None)
        if (None == apikey):
            logging.error('apikey key is not specified')

        pool = pools.getpool(poolname, apikey)
        if None == pool:
            logging.error('Pool name %s is not valid' % poolname)
            continue

        status = pool.get_status()
        if not status:
            logging.wraning('Pool %s return no data' % poolname)
        status['time'] = datetime.isoformat(datetime.utcnow())

        d[key] = status
        logging.debug(pprint.pformat(status))

    d.close()

# Get worker status and fire alerts if conditions meet
def check_alert():
    d = shelve.open(setting.DB_FILE)
    for pool in d:
        if not 'std' in d[pool] or not 'workers' in d[pool]['std']:
            continue
        workers = d[pool]['std']['workers']
        for workername in workers:
            if not 'hash_rate' in workers[workername]:
                continue
            if workers[workername]['hash_rate'] >= HASH_RATE_THRESH:
                continue
            subprocess.call([SCRIPT_FILE, pool, workername])

    d.close()

def main():
    logging.basicConfig(
            filename='bmonitor.log',
            filemode='a',
            format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)

    while 1:
        try:
            # Read config each round to get config file change
            config = read_config(setting.CONF_FILE)
            get_status(config)
            check_alert()
        except KeyboardInterrupt:
            break
        except:
            print "Unexpected error:", sys.exc_info()[0]

        time.sleep(setting.WAIT_SEC)

if __name__ == '__main__':
    main()
