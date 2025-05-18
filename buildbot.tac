import os
import sys

from twisted.application import service
from twisted.python.log import ILogObserver, FileLogObserver
from buildbot.master import BuildMaster

basedir = os.path.abspath(os.path.dirname(__file__))
configfile = 'master.py'

# Default umask for server
umask = None

# if this is a relocatable tac file, get the directory containing the TAC

# note: this line is matched against to check that this is a buildmaster
# directory; do not edit it.
application = service.Application('buildmaster')
application.setComponent(ILogObserver, FileLogObserver(sys.stdout).emit)

m = BuildMaster(basedir, configfile, umask)
m.setServiceParent(application)
