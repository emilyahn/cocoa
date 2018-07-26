import json
import csv
from collections import defaultdict

# worker_ids_file = "18content_batch_results_worker_ids.json"
# chat_file = "18content_0615_chat.json"
# survey_file = "18content_0615_surv.json"
# mturk_csv = "18content_batch_results.csv"
# outfile = "18content_qual.tsv"
worker_ids_file = "19struct_batch_worker_ids.json"
chat_file = "19struct_0621_chat.json"
survey_file = "19struct_0621_surv.json"
mturk_csv = "19struct_batch.csv"
outfile = "19struct_qual.tsv"


def read_mturk_csv():
	reader = csv.reader(open(mturk_csv, 'r'))
	header = reader.next()
	# worker_idx = header.index('WorkerId')
	code_idx = header.index('Answer.surveycode')
	duration_idx = header.index('WorkTimeInSeconds')
	submit_idx = header.index('SubmitTime')  # ex: Mon Jun 18 02:41:52 PDT 2018
	mturk_metadata = defaultdict(dict)

	for row in reader:
		# workerid = row[worker_idx]
		code = row[code_idx]
		mturk_metadata[code]["duration"] = row[duration_idx]
		mturk_metadata[code]["submit"] = row[submit_idx]

	return mturk_metadata

worker_ids = json.load(open(worker_ids_file))
mturk_metadata = read_mturk_csv()
chat_info = json.load(open(chat_file))
survey_info = json.load(open(survey_file))
# import pdb; pdb.set_trace()
new_dict = defaultdict(dict)
worker_to_chat_dict = defaultdict(list)

for chat_id, items in worker_ids.iteritems():
	if len(items) == 1:
		worker_id = "[none]"
		new_dict[chat_id] = {}

	else:
		worker_id = items["1"]
		if items["1"] is None:
			worker_id = items["0"]

		hit_code = items["mturk_code"]
		new_dict[chat_id] = {}
		new_dict[chat_id]["duration"] = float(mturk_metadata[hit_code]["duration"]) / 60
		new_dict[chat_id]["submit"] = mturk_metadata[hit_code]["submit"]

	worker_to_chat_dict[worker_id].append(chat_id)

# for worker_id, chatidlist in worker_to_chat_dict.iteritems():
# 	if len(chatidlist) > 1:
# 		print worker_id, chatidlist

# go through list of chat dicts
for full_chat in chat_info:
	this_chatid = full_chat["uuid"]
	this_style = full_chat["scenario"]["styles"]
	outcome = full_chat["outcome"]["reward"]  # 0 or 1

	new_dict[this_chatid]["style"] = this_style
	new_dict[this_chatid]["outcome"] = outcome

# go through survey
for chat_id, items in survey_info[1].iteritems():
	values_dict = items["0"]
	if len(items["0"]) == 0:
		values_dict = items["1"]

	new_dict[chat_id]["questions"] = values_dict

# import pdb; pdb.set_trace()
# print new_dict[u'C_326dc1a4bb484d469981966acd08d6f0'].keys()
# print new_dict[u'C_326dc1a4bb484d469981966acd08d6f0']['questions'].keys()

header = ['chat_id', 'worker_id']
cats = ['style', 'submit', 'duration', 'outcome']
questions = [u'n00_gender', u'n01_i_understand', u'n02_cooperative', u'n03_human', u'n04_understand_me', u'n05_chat', u'n06_texts', u'n07_tech', u'n08_learn_spa', u'n09_learn_eng', u'n10_age', u'n11_ability_spa', u'n12_ability_eng', u'n13_country', u'n14_online_spa', u'n15_online_eng', u'n16_online_mix', u'n17_comments']
all_cats = header
all_cats.extend(cats)
all_cats.extend(questions)

with open(outfile, 'w') as f:
	f.write('\t'.join(all_cats) + '\n')
	for worker_id, chat_list in worker_to_chat_dict.iteritems():
		for chat_id in chat_list:
			if chat_id == '': continue
			if new_dict[chat_id] == {}: continue
			line = '{}\t{}\t'.format(chat_id, worker_id)
			for cat in cats:
				if cat in new_dict[chat_id]:
					item = new_dict[chat_id][cat]
				else:
					item = ''

				line += '{}\t'.format(item)

			for question in questions:
				if "questions" not in new_dict[chat_id]:
					import pdb; pdb.set_trace()
				answer = new_dict[chat_id]["questions"][question]
				if type(answer) == unicode:
					answer = answer.encode('utf-8')
				line += '{}\t'.format(answer)

			f.write(line.strip() + '\n')









