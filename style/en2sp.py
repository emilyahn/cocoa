# from polyglot.text import Text
import spacy
from nltk.tokenize import wordpunct_tokenize

""" Convert English to Spanglish! """

__author__ = 'eahn1'

nlp_en = spacy.load('en')
nlp_sp = spacy.load('es')

def read_tables():
	with open("data/chat_prev/bot_rule.txt") as f:
		en_orig = f.readlines()
	with open("data/chat_prev/sp_bot_rule.txt") as f:
		sp_orig = f.readlines()
	return dict([('en', en_orig), ('sp', sp_orig)])

# idx&txt params are redundant but to-be-modified later
def sp_matrix_eng_nouns(eng_txt, tables_dct, idx):
	""" eng_txt: string of words (not list)
		tables_dct: contains 2 tables, keys = en,sp
		idx: int of which index in table is this sentence
	"""
	eng_doc = nlp_en(unicode(eng_txt, "utf-8"))
	# eng_pos = [token.pos_ for token in eng_doc]

	sp_txt = tables_dct['sp'][idx]
	sp_doc = nlp_sp(unicode(sp_txt, "utf-8"))
	# sp_pos = [token.pos_ for token in sp_doc]

	for en_token in eng_doc:
		en_pos = en_token.pos_
		if en_pos in ['NOUN', 'PROPN']:
			pass

sent_sp = "¿Tiene alguna ingeniería de interiores y electrónica?"
sent_en = "Do you have any laser tag or spanish?"

# polyglot syntax
# text = Text(sent)
# words = text.words
# tags = text.pos_tags

doc = nlp_en(unicode(sent_en, "utf-8"))

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)  