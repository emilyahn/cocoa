import json
from collections import defaultdict
import unidecode
import spacy
from argparse import ArgumentParser


""" Script to process cocoa chat in JSON
	Note: We strip all accents from user's chat.
		Useful for matching lexicon, may hurt LID performance.
	Example use from top dir:
	python eval/eval_cm.py --chat_file turk/amt_soc1_0724/0720_social_chat.json
		--lid_outfile eval/auto_social_spdef.tsv
"""

nlp_en = spacy.load('en')


def scrape_chat_json(chat_filename):
	chat_info = json.load(open(chat_filename))
	full_dict = defaultdict(dict)
	# full_dict[chat_str]['style'] = 'en_lex', 'en2sp', etc
	# full_dict[chat_str]['text'] = list of str (each str = user utt in dialogue)

	for full_chat in chat_info:
		this_chatid = full_chat["uuid"]
		this_style = full_chat["scenario"]["styles"]
		out_list = []

		idx = 0
		if full_chat['agents']['0'] == 'rule_bot':
			idx = 1

		for event in full_chat['events']:
			if not event['action'] == 'message':
				continue  # e.g. action == 'select'

			agent = event['agent']
			if agent == idx:
				msg = event['data']
				# strip all accents from text, lowercase
				msg = msg.lower()
				msg = unidecode.unidecode(msg)
				out_list.append(unicode(msg))

		full_dict[this_chatid]['style'] = this_style
		full_dict[this_chatid]['text'] = out_list

	return full_dict


def auto_lid_tagging(chatdict, outfile):
	content_en = set()
	content_sp = set()
	with open('cocoa/data/en_dict.txt', 'r') as fin:
		for line in fin.readlines():
			eng = line.strip().decode('utf-8')
			content_en.add(eng)

	with open('cocoa/data/en_common_1k.txt', 'r') as fin:
		for line in fin.readlines():
			eng = line.strip().decode('utf-8')
			content_en.add(eng)

	with open('cocoa/data/sp_dict.txt', 'r') as fin:
		for line in fin.readlines():
			spa = line.strip().decode('utf-8')
			spa = unidecode.unidecode(spa)
			content_sp.add(spa)

	with open('cocoa/data/sp_common_1k.txt', 'r') as fin:
		for line in fin.readlines():
			spa = line.strip().decode('utf-8')
			spa = unidecode.unidecode(spa)
			content_sp.add(spa)

	def add_to_biling_dict(fname):
		with open(fname, 'r') as fin:
			for line in fin.readlines():
				eng, spa = line.strip().decode('utf-8').split('\t')
				for eng_word in eng.split():
					content_en.add(eng_word)
				for spa_word in spa.split():
					spa_word = unidecode.unidecode(spa_word)
					content_sp.add(spa_word)

	# add_to_biling_dict('cocoa/data/names.txt')
	add_to_biling_dict('cocoa/data/hobbies.txt')
	add_to_biling_dict('cocoa/data/loc.txt')
	add_to_biling_dict('cocoa/data/time.txt')
	add_to_biling_dict('cocoa/data/majors.txt')
	# DONE adding lexicon items

	out_list = []
	hyp_counts = [0, 0, 0]
	for chat_id in chatdict:
		for utt_i, utt in enumerate(chatdict[chat_id]['text']):
			doc_en = nlp_en(utt)
			for word_orig in doc_en:
				word = word_orig.text
				hypothesis_01 = 2
				# if word in content_en:
				# 	hypothesis_01 = 1
				# elif word in content_sp:
				# 	hypothesis_01 = 0

				# TRY FLIPPING DEFAULT
				if word in content_sp:
					hypothesis_01 = 0
				elif word in content_en:
					hypothesis_01 = 1

				# import pdb; pdb.set_trace()
				out_list.append(
					'\t'.join([
						chatdict[chat_id]['style'], chat_id,
						str(utt_i), word, str(hypothesis_01)
					])
				)
				hyp_counts[hypothesis_01] += 1

	print hyp_counts

	with open(outfile, 'w') as w:
		for line in out_list:
			w.write(line + '\n')


def main():
	parser = ArgumentParser('eval cocoa data')
	parser.add_argument(
		'--chat_file', type=str, required=True,
		help='Infile path to the chat json')
	parser.add_argument(
		'--lid_outfile', type=str, default=None,
		help='Outfile path. TSV of tokens w/ auto-generated LID tags')
	args = parser.parse_args()

	# import pdb; pdb.set_trace()
	chat_dict = scrape_chat_json(args.chat_file)
	if args.lid_outfile is not None:
		auto_lid_tagging(chat_dict, args.lid_outfile)

	# for chat_id in chat_dict:
	# 	print '{}\t{}'.format(chat_id, chat_dict[chat_id]['style'])

if __name__ == '__main__':
	main()
