#!/bin/bash

. /usr/lib/ckan/default/bin/activate

export PYENV=/usr/lib/ckan/default/
export CKAN_PYENV=${PYENV}
export CKAN_HOME=${CKAN_PYENV}/src/ckan/

cd ${CKAN_HOME} 
