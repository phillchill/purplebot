from markovBot import *
from twython import Twython
import re
import time

API_KEY = 'BoP0mE4gtGZlh1me29lug'
API_SECRET = 'xteLnU2uu3KEKxZx8hc1wfPic0gs5JvosmRP9VBA6c'
ACCESS_TOKEN = '2417467056-2aZr2bQSGaDcRnbqR7QAHC95TXXSPbyQr2jONYa'
ACCESS_TOKEN_SECRET = 'LBKmR3OXxVFiLEM9zeiYNe0tKwUyiFdfmz27ts36AuhHW'

CORPUS_PATH_DEMOCRAT = './data/corpora/tweets-democratic.txt'
CORPUS_PATH_REPUBLICAN = './data/corpora/tweets-republican.txt'

GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
URLINTEXT_PAT = re.compile(ur'https?://[^\s<>"]+|\w+\.[^\s<>"]+')

def stripURLs(text):
	text = text.replace("http : /", "http:/")
	urls = [ mgroups[0] for mgroups in URLINTEXT_PAT.findall(text) ]
	for url in urls:
		text = text.replace(url, "")
	return text

def concat_symbols(text):
	text = text.replace("# ", "#")
	text = text.replace(" :", ":")
	text = text.replace(" ,", ",")
	# text = text.replace("@ ", "@") # prevent @mentions to prevent suspension!
	text = text.replace(" '", "'")
	text = text.replace(" ?", "?")
	text = text.replace(" !", "!")
	text = text.replace("$ ", "$")
	text = text.replace("`` ", "``")
	return text

def main():
	twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	rawText1 = open(CORPUS_PATH_REPUBLICAN, 'rb').read()
	rawText2 = open(CORPUS_PATH_DEMOCRAT, 'rb').read()

	# combine texts by summing equal parts
	minLength = min(len(rawText1), len(rawText2))
	combinedText = rawText1[:minLength] + rawText2[:minLength]

	print "now generating RepubliCrat tweet..."
	myMarkov = MarkovBot(combinedText,3)

	while 1:
		genText = myMarkov.generate_text()
		sentence = ' '.join(genText)
		tweetText = myMarkov.ensure_tweet_length(sentence)
		tagText = concat_symbols(tweetText)

		finalText = tagText


		try:
			twitter.update_status(status=finalText)
		except Exception, e:
			raise e
			# continue

		print "\n*****\n"
		print finalText
		print "\n*****\n"

		time.sleep(600)


if __name__ == '__main__':
	main()