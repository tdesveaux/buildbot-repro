from pathlib import Path

from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.schedulers import forcesched, triggerable
from buildbot.steps import shell
from buildbot.steps.trigger import Trigger
from buildbot.worker.docker import DockerLatentWorker

c = BuildmasterConfig = {}

####### WORKERS


def _docker_worker(name: str):
    return DockerLatentWorker(
        name,
        password=None,
        docker_host="unix:///var/run/docker.sock",
        masterFQDN="localhost",
        image="buildbot/buildbot-worker:master",
        autopull=True,
        hostconfig={"network_mode": "host"},
        volumes=[f"{Path().parent.absolute() / 'lorem.txt'}:/tmp/lorem.txt"],
    )


c["workers"] = [_docker_worker(f"local-worker-{idx:02d}") for idx in range(20)]

all_workers = [w.name for w in c["workers"]]

c["protocols"] = {"pb": {"port": 9989}}

####### BUILDERS

builder_factory = BuildFactory(
    steps=[shell.ShellCommand(command=["cat", "/tmp/lorem.txt"])]
)

# trigger as much jobs as cpu to saturate
# job_count = os.cpu_count() or 2
job_count = 12

c["builders"] = [
    BuilderConfig(
        name="builder-trigger",
        workernames=all_workers,
        factory=BuildFactory(
            steps=[
                Trigger(
                    waitForFinish=True,
                    schedulerNames=["trigger-scheduler"] * job_count,
                ),
            ]
        ),
    ),
    BuilderConfig(
        name="builder-logger", workernames=all_workers, factory=builder_factory
    ),
]

####### SCHEDULERS

c["schedulers"] = [
    forcesched.ForceScheduler(
        name="force-trigger",
        builderNames=["builder-trigger"],
    ),
    triggerable.Triggerable(name="trigger-scheduler", builderNames=["builder-logger"]),
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
c["www"] = {"port": 8010}

####### DB URL

with (Path().parent / "db.env").open() as fp:
    db_vars = {}
    for line in fp.readlines():
        line = line.strip()
        if not line:
            continue
        k, v = line.strip().split("=", 1)
        db_vars[k] = v

c["db"] = {
    "db_url": "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}".format(
        **db_vars
    )
}
c["buildbotNetUsageData"] = None
