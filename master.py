from buildbot.schedulers import forcesched
from buildbot.worker import local
from buildbot.config import BuilderConfig
from buildbot.steps.shell import ShellCommand
from buildbot.process.factory import BuildFactory
from buildbot.www.auth import UserPasswordAuth
from buildbot.process.properties import Interpolate

c = BuildmasterConfig = {}

####### WORKERS

c["workers"] = [
    local.LocalWorker("worker"),
]

c["protocols"] = {"pb": {"port": 9989}}

####### BUILDERS

factory = BuildFactory()
factory.addStep(ShellCommand(command=["echo", "ok"]))

c["builders"] = [
    BuilderConfig(name="builder", workernames=["worker"], factory=factory),
]

####### SCHEDULERS

c["schedulers"] = [
    forcesched.ForceScheduler(
        name="force",
        builderNames=["builder"],
    ),
]

####### PROJECT IDENTITY

# the 'title' string will appear at the top of this buildbot installation's
# home pages (linked to the 'titleURL').

c["title"] = "Hello World CI"
c["titleURL"] = "https://buildbot.github.io/hello-world/"

# the 'buildbotURL' string should point to the location where the buildbot's
# internal web server is visible. This typically uses the port number set in
# the 'www' entry below, but with an externally-visible host name which the
# buildbot cannot figure out without some help.

c["buildbotURL"] = "http://localhost:8010/"

c['collapseRequests'] = False

# minimalistic config to activate new web UI
c["www"] = {'port': 8010, 'auth': UserPasswordAuth(users={'user': 'pwd'})}

####### DB URL

c["db"] = {
    "db_url": Interpolate("sqlite:///%(kw:filename)s", filename="state.sqlite"),
}
c["buildbotNetUsageData"] = "full"
