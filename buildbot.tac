import os

from twisted.application import service
from buildbot.master import BuildMaster

basedir = '.'

rotateLength = 10000000
maxRotatedFiles = 10
configfile = 'master.py'

# Default umask for server
umask = None

# if this is a relocatable tac file, get the directory containing the TAC
if basedir == '.':
    basedir = os.path.abspath(os.path.dirname(__file__))

# note: this line is matched against to check that this is a buildmaster
# directory; do not edit it.
application = service.Application('buildmaster')
from twisted.python.logfile import LogFile
from twisted.logger import ILogObserver
from twisted.logger import textFileLogObserver
from twisted.logger import LogLevelFilterPredicate
from twisted.logger import FilteringLogObserver
logfile = LogFile.fromFullPath(os.path.join(basedir, "twistd.log"), rotateLength=rotateLength,
                                maxRotatedFiles=maxRotatedFiles)
application.setComponent(
    ILogObserver,
    FilteringLogObserver(
        textFileLogObserver(logfile), predicates=[LogLevelFilterPredicate()]
    ),
)

m = BuildMaster(basedir, configfile, umask)
m.setServiceParent(application)
m.log_rotation.rotateLength = rotateLength
m.log_rotation.maxRotatedFiles = maxRotatedFiles