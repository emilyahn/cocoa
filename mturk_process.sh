# script to process mturk results

# 0) check params
out_name=18content_0615
time_stamp=2018-06-15-21-09-38
chat_db=turk/${out_name}.db
scenarios=data/scenarios_0614.json
schema=data/schema_0614.json

batch_file=turk/18content_batch_results.csv
batch_arg="--batch-results $batch_file"
# batch_arg=""


# 1) COPY SQL DB TO LOCAL
scp aws:~/cocoa/web_output/${time_stamp}/chat_state.db $chat_db

# 2) handle mturk codes, verify workers, write logs to chat & surv files
PYTHONPATH=. python src/web/dump_db_neg.py --db $chat_db --output turk/${out_name}_chat.json  --schema-path $schema --scenarios-path $scenarios --surveys turk/${out_name}_surv.json $batch_arg

# 3) visualize data
PYTHONPATH=. python src/scripts/visualize_data.py --scenarios-path $scenarios --schema-path $schema --transcripts turk/${out_name}_chat.json --html-output turk/${out_name}.html --survey_file turk/${out_name}_surv.json