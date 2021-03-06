# vim: filetype=python
import os

activate_this = os.path.join('/usr/lib/ckan/default', 'bin/activate_this.py')
execfile(activate_this, dict(__file__ = activate_this))

# Provide a custom CA bundle if needed
#os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ckan/default/cacert.pem'

from paste.deploy import loadapp
config_filepath = os.path.join('/etc/ckan/default', 'config.ini')
from paste.script.util.logging_config import fileConfig
fileConfig(config_filepath)
application = loadapp('config:%s' % config_filepath)
