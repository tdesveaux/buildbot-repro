from buildbot.schedulers import forcesched, triggerable
from buildbot.worker import local, Worker
from buildbot.config import BuilderConfig
from buildbot.steps.shell import ShellCommand
from buildbot.steps.trigger import Trigger
from buildbot.process.factory import BuildFactory
from buildbot.www.auth import UserPasswordAuth

c = BuildmasterConfig = {}

####### WORKERS

c["workers"] = [
    local.LocalWorker("worker"),
    Worker("pb-worker", "password"),
    Worker("msgpack-worker", "password"),
]

c["protocols"] = {
    "pb": {"port": 9989},
    "msgpack_experimental_v7": {"port": 9990},
}

####### BUILDERS

factory = BuildFactory(
    [
        ShellCommand(command=["echo", "ok"]),
    ]
)


c["builders"] = [
    BuilderConfig(name="local-builder", workernames=["worker"], factory=factory),
    BuilderConfig(name="pb-builder", workernames=["pb-worker"], factory=factory),
    BuilderConfig(
        name="msgpack-builder", workernames=["msgpack-worker"], factory=factory
    ),
    BuilderConfig(
        name="all-builder",
        workernames=["worker"],
        factory=BuildFactory(
            steps=[Trigger(waitForFinish=True, schedulerNames=["triggerable"])]
        ),
    ),
]

####### SCHEDULERS

c["schedulers"] = [
    forcesched.ForceScheduler(
        name="force",
        builderNames=["all-builder"],
    ),
    triggerable.Triggerable(
        "triggerable",
        builderNames=[
            "local-builder",
            "pb-builder",
            "msgpack-builder",
        ],
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

c["collapseRequests"] = False

# minimalistic config to activate new web UI
c["www"] = {
    "port": 8010,
    "auth": UserPasswordAuth(users={"user": "pwd"}),
    "plugins": {
        "grid_view": {},
        "console_view": {},
        "waterfall_view": {},
    }
}
####### DB URL

c["db"] = {
    "db_url": "sqlite:///state.sqlite",
}
c["buildbotNetUsageData"] = None
