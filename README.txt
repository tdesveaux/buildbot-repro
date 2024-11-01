python3 -m venv .venv --upgrade-deps
. .venv/bin/activate
python -m pip install -r requirements.txt
NOTE: requirements.txt install latest (4.1.0) Buildbot release, which does not contain the issue

buildbot --verbose create-master --config=master.py --no-logrotate --relocatable
buildbot --verbose upgrade-master
buildbot --verbose start --nodaemon .

NOTE: `builderid` in the data's `params` object might not be the id of `builder-trigger` as Buildbot's Builder instantiation seems to not be deterministic.
    check the ID with `curl http://localhost:8010/api/v2/builders/builder-trigger`
curl 'http://localhost:8010/api/v2/forceschedulers/force-trigger' -X POST -H 'Content-Type: application/json' --data-raw '{"id":1,"jsonrpc":"2.0","method":"force","params":{"builderid":"2","username":"","reason":"force build","priority":0,"branch":"","project":"","repository":"","revision":""}}'

docker run --detach --env-file ./db.env --publish 127.0.0.1:5432:5432 --name bb-repro-psql --pull always --rm postgres:latest
docker stop bb-repro-psql


py-spy record --pid $(cat ../twistd.pid) --subprocesses --threads -o test.svg
py-spy record --subprocesses --threads -o $(buildbot --version | grep Buildbot | sed "s/Buildbot version: //").svg -- buildbot --verbose start --nodaemon .
