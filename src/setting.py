#!/usr/bin/env python

import os

# Constants
WAIT_SEC  = 600

DATA_DIR  = os.path.join(os.environ['HOME'], '.bmonitor')
DB_FILE   = os.path.join(DATA_DIR, 'db')
CONF_FILE = os.path.join(DATA_DIR, 'config')
