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
PYTHONPATH=. python src/web/start_app.py --port 5000 --schema-path data/mini_schema.json --scenarios-path data/mini_scenarios.json --config data/web/app_params.json```

### 3 April
PYTHONPATH=. python src/scripts/generate_schema.py --schema-path data/mini_schema.json
PYTHONPATH=. python src/scripts/generate_scenarios.py --schema-path data/mini_schema.json --scenarios-path data/mini_scenarios.json --num-scenarios 10 --random-attributes --random-items --alphas 0.3 1 3 --min-items 8 --max-items 8
```