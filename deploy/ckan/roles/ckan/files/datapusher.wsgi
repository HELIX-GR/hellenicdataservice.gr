# vim: filetype=python
import os
import sys
import hashlib

activate_this = os.path.join('/usr/lib/ckan/datapusher', 'bin/activate_this.py')
execfile(activate_this, dict(__file__ = activate_this))

import ckanserviceprovider.web as web
os.environ['JOB_CONFIG'] = '/etc/ckan/datapusher/config.py'

# Provide a custom CA bundle if needed
#os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ckan/datapusher/cacert.pem'

web.init()

import datapusher.jobs as jobs

application = web.app
