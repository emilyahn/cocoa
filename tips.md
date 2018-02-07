# random useful things
export PYTHONPATH=.
pip install -r requirements.txt
import ipdb; ipdb.set_trace()

/Users/eahn/.pyenv/versions/2.7.10/Python.framework/Versions/2.7/lib/python2.7/site-packages/fuzzywuzzy/fuzz.py:35: UserWarning: Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning

### command to dump logs to outfiles --surveys and --output
python src/web/dump_db_neg.py --db web_output/2018-01-16/chat_state.db --output web_output/log1_01-16_chats.json --surveys web_output/log1_01-16_surv.json --schema-path data/schema.json --scenarios-path data/scenarios.json

### command to run app
python src/web/start_app.py --port 5000 --schema-path data/friends-schema.json --scenarios-path data/scenarios.json --config data/web/app_params.json

### mt stuff
Downloaded the following with brew:
* subversion
* libtool
* boost
* xmlrpc-c
* boost-build