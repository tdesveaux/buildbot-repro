python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

buildbot --verbose upgrade-master . && rm master.cfg.sample twistd.log
buildbot --verbose start --nodaemon .

# old worker image
docker build -f ./Dockerfile.worker -t local-old-worker .
docker run --rm -ti -eWORKER_NAME=old-worker -eWORKER_PASSWORD=s3cret local-old-worker
