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
import time

import pools
import setting

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

        poolclass = getattr(pools, poolname, None)
        if (not poolclass):
            logging.error('Pool name %s is not valid' % poolname)
            continue

        pool = poolclass(apikey)
        status = pool.get_status()
        status['time'] = datetime.isoformat(datetime.utcnow())

        d[key] = status
        logging.debug(pprint.pformat(status))

    d.close()

def main():
    logging.basicConfig(
            filename='bmonitor.log',
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG)

    while 1:
        # Read config each round to get config file change
        config = read_config(setting.CONF_FILE)
        get_status(config)

        time.sleep(setting.WAIT_SEC)

if __name__ == '__main__':
    main()
