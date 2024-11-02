import os

from twisted.application import service
from buildbot.master import BuildMaster

basedir = '.'

configfile = 'master.py'

# Default umask for server
umask = None

# if this is a relocatable tac file, get the directory containing the TAC
if basedir == '.':
    basedir = os.path.abspath(os.path.dirname(__file__))

# note: this line is matched against to check that this is a buildmaster
# directory; do not edit it.
application = service.Application('buildmaster')


m = BuildMaster(basedir, configfile, umask)
m.setServiceParent(application)
