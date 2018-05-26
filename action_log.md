### 13 Feb
using [fast_align](https://github.com/clab/fast_align) tool


```sh
py style/format_to_align.py data/chat_prev/en_rule.txt data/chat_prev/sp_rule.txt style/en-sp_rule.txt
cd style/
fast_align -i en-sp_rule.txt -d -o -v > en2sp.align
fast_align -i en-sp_rule.txt -d -o -v -r > sp2en.align
```

### 19 Feb
```sh
fast_align -i en-sp_rule.txt -d -v -o -p probs.en2sp > align.en2sp
fast_align -i en-sp_rule.txt -d -v -o -r -p probs.sp2en > align.sp2en
atools -i align.en2sp -j align.sp2en -c grow-diag-final-and > aligned.gdfa
```

### 20 Feb
* new databases in `data/{names,loc,hobbies,time}.txt`
* new schema: `data/mini_schema.json`
* new scenario: `data/mini_scenarios.json`
```sh
PYTHONPATH=. python src/scripts/generate_schema.py --schema-path data/mini_schema.json
PYTHONPATH=. python src/scripts/generate_scenarios.py --schema-path data/mini_schema.json --scenarios-path data/mini_scenarios.json --num-scenarios 10 --random-attributes --random-items --alphas 0.3 1 3
# to run full with new schema
PYTHONPATH=. python src/web/start_app.py --port 5000 --schema-path data/mini_schema.json --scenarios-path data/mini_scenarios.json --config data/web/app_params.json
```

### 3 April
```sh
PYTHONPATH=. python src/scripts/generate_schema.py --schema-path data/mini_schema.json
PYTHONPATH=. python src/scripts/generate_scenarios.py --schema-path data/mini_schema.json --scenarios-path data/mini_scenarios.json --num-scenarios 10 --random-attributes --random-items --alphas 0.3 1 3 --min-items 8 --max-items 8
```

### 10 April
created:
* data/mini_schema_style.json
* data/mini_scenarios_style.json
added param of style to scenarios. Num of scenarios in json = (--num-scenarios * num_styles) -- styles determined by list in `src/scripts/generate_schema.py`

### 20 May
```sh
chat_db=turk/chat_state.db
out_name=pilot0
scenarios=data/scenarios_0519_10items.json
schema=data/schema_0519.json
# handle mturk codes, verify workers
PYTHONPATH=. python src/web/dump_db_neg.py --db $chat_db --output turk/${out_name}_chat.json  --schema-path $schema --scenarios-path $scenarios --surveys turk/${out_name}_surv.json --batch-results turk/Batch_3239361_batch_results.csv
# visualize data
PYTHONPATH=. python src/scripts/visualize_data.py --scenarios-path $scenarios --schema-path $schema --transcripts turk/${out_name}_chat.json --html-output turk/${out_name}.html --survey_file turk/${out_name}_surv.json
```
