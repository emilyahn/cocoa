import json
# import sys
import langid
import cld2


# returns only what human said from complete json chat file
def read_human_from_json(infile):
	read_list = json.load(open(infile))
	out_list = []

	for chat in read_list:
		idx = 0
		# if chat['agents']['0']=='human':
		if chat['agents']['0'] == 'bot':
			idx = 1
		for event in chat['events']:
			if not event['action'] == 'message':
				continue  # e.g. action == 'select'
			msg = event['data']
			agent = event['agent']
			if agent == idx:
				out_list.append(msg)

	return out_list

chat_file = "web_output/log1_03-19_chats.json"

# infile = sys.argv[1]
read_human_from_json(chat_file)
# langid.classify("tengo una hermana") -> 'es' (GOOD)
# langid.classify("tengo un amigo") -> 'it' (BAD!!!!)
# langid.classify("tengo") -> 'en' (BAD)
# langid.classify("quien eres tu") -> 'es' (GOOD. can handle wrong accents)

# CLD2

# isReliable, textBytesFound, details = cld2.detect("This is my sample text")
# print('  reliable: %s' % (isReliable != 0))
# print('  textBytes: %s' % textBytesFound)
# print('  details: %s' % str(details))

# The output looks like so:
#  reliable: True
#  textBytes: 24
#  details: (('ENGLISH', 'en', 95, 1736.0), ('Unknown', 'un', 0, 0.0), ('Unknown', 'un', 0, 0.0))

