import itertools
from typing import Any

from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.schedulers import forcesched, triggerable
from buildbot.steps.shell import ShellCommand
from buildbot.steps.trigger import Trigger
from buildbot.steps.master import MasterShellCommand
from buildbot.worker import local
from buildbot.www.auth import UserPasswordAuth
from buildbot.schedulers.forcesched import FixedParameter, StringParameter, TextParameter, IntParameter, BooleanParameter, UserNameParameter, ChoiceStringParameter, WorkerChoiceParameter, FileParameter, NestedParameter, AnyPropertyParameter

c: dict[str, Any] = {}
BuildmasterConfig = c


####### WORKERS
c["protocols"] = {"pb": {"port": 9989}}

c["workers"] = [
    local.LocalWorker("worker"),
]

####### BUILDERS
c["builders"] = [
    BuilderConfig(
        name="triggered",
        workernames=["worker"],
        factory=BuildFactory(
            [
                MasterShellCommand(
                    command=["python3", "-c", "import sys; sys.exit(1)"]
                ),
                ShellCommand(command=["python3", "-c", "import sys; sys.exit(1)"]),
            ]
        ),
    ),
    BuilderConfig(
        name="builder-with-a-really-long-name-and-some-more",
        workernames=["worker"],
        factory=BuildFactory(([Trigger(["triggerable"], waitForFinish=True)])),
    ),
]

####### SCHEDULERS

c["schedulers"] = [
    forcesched.ForceScheduler(
        name="force",
        builderNames=[c["builders"][1].name],
        properties=[
            FixedParameter(name="FixedParameter", default="FixedParameter"),
            StringParameter(name="StringParameter", default="StringParameter"),
            TextParameter(name="TextParameter", default="TextParameter"),
            IntParameter(name="IntParameter", default=1),
            BooleanParameter(name="BooleanParameter", default=False),
            UserNameParameter(name="UserNameParameter-no-mail", need_email=False),
            UserNameParameter(name="UserNameParameter-with-mail", need_email=True),
            *[
                ChoiceStringParameter(name=f"ChoiceStringParameter-{strict=}-{multiple=}", strict=strict, multiple=multiple)
                for strict, multiple in itertools.product((True, False), (True, False))
            ],
            WorkerChoiceParameter(name="WorkerChoiceParameter"),
            FileParameter(name="FileParameter"),
            *[
                NestedParameter(name=f"NestedParameter-{layout}", layout=layout, fields=[
                    IntParameter(name=f"NestedIntParameter-{layout}", default=1),
                ])
                for layout in ["vertical", "tabs", "simple"]
            ],
            AnyPropertyParameter(name="AnyPropertyParameter"),
        ]
    ),
    triggerable.Triggerable(
        "triggerable",
        builderNames=["triggered"],
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
        "badges": {},
        "console_view": {},
        "grid_view": {},
        "waterfall_view": {},
        "wsgi_dashboards": [],
    }
}

####### DB URL

c["db"] = {
    "db_url": "sqlite:///state.sqlite",
}
c["buildbotNetUsageData"] = None
