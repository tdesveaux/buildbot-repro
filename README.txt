python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

buildbot --verbose create-master -c master.py --relocatable .
buildbot --verbose upgrade-master . && rm master.cfg.sample twistd.log
buildbot --verbose start --nodaemon .
