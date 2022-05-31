#!/bin/bash

# see: https://discuss.python.org/t/understanding-site-packages-directories/12959
_SYSCONFIG_VERSION=$(python -c 'import sysconfig; print(sysconfig.get_python_version())')

# Detect if a virtualenv has been mounted. Python virtualenv activation scripts
# contain hard coded paths from the host system that will not be available in
# the container. To accomadate for this manually set the VIRTUAL_ENV and the
# PYTHONPATH.
if [ -d "/venv/lib/python$_SYSCONFIG_VERSION" ]; then
  export VIRTUAL_ENV=/venv
  if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="/venv/lib/python$_SYSCONFIG_VERSION/site-packages"
  else
    export PYTHONPATH="/venv/lib/python$_SYSCONFIG_VERSION/site-packages:$PYTHONPATH"
  fi
fi
/usr/local/bin/pylsp $@
