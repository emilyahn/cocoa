# script to process mturk results

# 0) check params
out_name=fig8_0_all4 #_nobatch
out_folder=turk/${out_name}
time_stamp=2018-07-25-15-04-31
chat_db=${out_folder}/${out_name}.db
# chat_db=turk/struct_0629.db
scenarios=data/scenarios_0720_social.json
schema=data/schema_0720_social.json

# batch_file=${out_folder}/struct_0629_batch_fix.csv
# batch_arg="--batch-results $batch_file"
batch_arg=""


# 1) COPY SQL DB TO LOCAL
mkdir -p $out_folder
scp aws:~/cocoa/web_output/${time_stamp}/chat_state.db $chat_db

# 2) handle mturk codes, verify workers, write logs to chat & surv files
PYTHONPATH=. python src/web/dump_db_neg.py --db $chat_db --output ${out_folder}/${out_name}_chat.json  --schema-path $schema --scenarios-path $scenarios --surveys ${out_folder}/${out_name}_surv.json $batch_arg

# 3) visualize data
PYTHONPATH=. python src/scripts/visualize_data.py --scenarios-path $scenarios --schema-path $schema --transcripts ${out_folder}/${out_name}_chat.json --html-output ${out_folder}/${out_name}.html --survey_file ${out_folder}/${out_name}_surv.json

# misc temporary commands
# PYTHONPATH=. python src/web/dump_db_neg.py --db turk/amt_struct2_0629_buggy/struct_0629.db --output turk/amt_struct2_0629_buggy/struct_0629_trim_chat.json  --schema-path data/schema_0618_struct.json --scenarios-path data/scenarios_0618_struct.json --surveys turk/amt_struct2_0629_buggy/struct_0629_trim_surv.json --batch-results turk/amt_struct2_0629_buggy/struct_0629_batch_fix.csv