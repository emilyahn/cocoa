import sqlite3
import json
import math
import os
from argparse import ArgumentParser

# from cocoa.core.schema import Schema
from src.basic.schema import Schema
# from cocoa.core.scenario_db import add_scenario_arguments, ScenarioDB
from src.basic.scenario_db import add_scenario_arguments, ScenarioDB
# from cocoa.core.util import read_json, write_json
from src.basic.util import read_json, write_json

# Task-specific modules
# from web.main.db_reader import DatabaseReader
from src.web.db_reader_neg import DatabaseReader
# from core.scenario import Scenario

def read_results_csv(csv_file):
    '''
    Return a dict from mturk_code to worker_id.
    '''
    import csv
    reader = csv.reader(open(csv_file, 'r'))
    header = reader.next()
    worker_idx = header.index('WorkerId')
    code_idx = header.index('Answer.surveycode')
    d = {}
    for row in reader:
        workerid = row[worker_idx]
        code = row[code_idx]
        d[code] = workerid
    return d

def chat_to_worker_id(cursor, code_to_wid):
    '''
    chat_id: {'0': workder_id, '1': worker_id}
    workder_id is None means it's a bot
    '''
    d = {}
    cursor.execute('SELECT chat_id, agent_ids FROM chat')
    for chat_id, agent_uids in cursor.fetchall():
        agent_wid = {}
        agent_uids = eval(agent_uids)
        for agent_id, agent_uid in agent_uids.iteritems():
            if not (isinstance(agent_uid, basestring)): #and agent_uid.startswith('U_')):
                agent_wid[agent_id] = None
            else:
                cursor.execute('''SELECT mturk_code FROM mturk_task WHERE name=?''', (agent_uid,))
                res = cursor.fetchall()
                if len(res) > 0:
                    mturk_code = res[0][0]
                    if mturk_code not in code_to_wid:
                        continue
                    else:
                        agent_wid[agent_id] = code_to_wid[mturk_code]
        d[chat_id] = agent_wid
    return d

def log_worker_id_to_json(db_path, batch_results):
    '''
    {chat_id: {'0': worker_id; '1': worker_id}}
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    code_to_wid = read_results_csv(batch_results)
    worker_ids = chat_to_worker_id(cursor, code_to_wid)
    output_dir = os.path.dirname(batch_results)
    write_json(worker_ids, output_dir + '/worker_ids.json')

# moidfied method from original file: dump_events_to_json.py
def log_surveys_to_json(cursor, surveys_file):
    questions = ['fluent', 'correct', 'cooperative', 'humanlike', 'comments']
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    cursor.execute('''SELECT * FROM survey''')
    logged_surveys = cursor.fetchall()
    survey_data = {}
    agent_types = {}

    for survey in logged_surveys:
        # print survey
        (userid, cid, _, fluent, correct, cooperative, humanlike, comments) = survey
        responses = dict(zip(questions, [fluent, correct, cooperative, humanlike, comments]))
        cursor.execute('''SELECT agent_types, agent_ids FROM chat WHERE chat_id=?''', (cid,))
        chat_result = cursor.fetchone()
        agents = json.loads(chat_result[0])
        agent_ids = json.loads(chat_result[1])
        agent_types[cid] = agents
        if cid not in survey_data.keys():
            survey_data[cid] = {0: {}, 1: {}}
        partner_idx = 0 if agent_ids['1'] == userid else 1
        survey_data[cid][partner_idx] = responses

    json.dump([agent_types, survey_data], open(surveys_file, 'w'))


if __name__ == "__main__":
    parser = ArgumentParser()
    add_scenario_arguments(parser)
    parser.add_argument('--db', type=str, required=True, help='Path to database file containing logged events')
    parser.add_argument('--output', type=str, required=True, help='File to write JSON examples to.')
    parser.add_argument('--uid', type=str, nargs='*', help='Only print chats from these uids')
    parser.add_argument('--surveys', type=str, help='If provided, writes a file containing results from user surveys.')
    parser.add_argument('--batch-results', type=str, help='If provided, write a mapping from chat_id to worker_id')
    args = parser.parse_args()
    schema = Schema(args.schema_path)
    # scenario_db = ScenarioDB.from_dict(schema, read_json(args.scenarios_path), Scenario)
    scenario_db = ScenarioDB.from_dict(schema, read_json(args.scenarios_path))

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    DatabaseReader.dump_chats(cursor, scenario_db, args.output, args.uid)
    if args.surveys:
        # DatabaseReader.dump_surveys(cursor, args.surveys)
        log_surveys_to_json(cursor, args.surveys)
    # TODO: move this to db_reader
    if args.batch_results:
        log_worker_id_to_json(args.db, args.batch_results)