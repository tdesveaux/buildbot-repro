import os
import sys

from buildslave.bot import BuildSlave
from twisted.application import service
from twisted.python.log import ILogObserver, FileLogObserver

basedir = os.path.abspath(os.path.dirname(__file__))
rotateLength = 10000000
maxRotatedFiles = 10

# note: this line is matched against to check that this is a buildslave
# directory; do not edit it.
application = service.Application("buildslave")


application.setComponent(ILogObserver, FileLogObserver(sys.stdout).emit)

buildmaster_host = os.getenv(
    "BUILDBOT_MASTER",
    # docker host, can be found with `ip a dev docker0`
    "172.17.0.1",
)
port = 9989
slavename = os.getenv("WORKER_NAME")
# get password and remove from env
passwd = os.environ.pop("WORKER_PASSWORD")
keepalive = 600
usepty = 0
umask = None
maxdelay = 300
allow_shutdown = None

s = BuildSlave(
    buildmaster_host,
    port,
    slavename,
    passwd,
    basedir,
    keepalive,
    usepty,
    umask=umask,
    maxdelay=maxdelay,
    allow_shutdown=allow_shutdown,
)
s.setServiceParent(application)
