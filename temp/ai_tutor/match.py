from __future__ import print_function
from fuzzywuzzy import fuzz
from unidecode import unidecode
from nltk.tokenize import WordPunctTokenizer
import string
from nltk.corpus import stopwords
import re

stop_words = set(stopwords.words('english'))


word_punct_tokenizer = WordPunctTokenizer()
punc = "_,,.!?:;()<>[]$=-/"
table = string.maketrans(punc," "*len(punc))

def prepro(sent):

	sent = sent.translate(table)
	tok_sent = [word for word in sent.split(" ") if word not in string.punctuation and word.isalnum() and len(word)>1 and word.lower() not in stop_words and not(re.match('^[\'-]', word))]
	if tok_sent:
		sentence = " ".join(tok_sent)
		return sentence  

def best_match(a, b):

	# tok_a = [tok for tok in a.split("_")]
	# tok_b = [tok for tok in b.split("_")]
	a = prepro(a)
	b = prepro(b)
	print(a, b)
	return fuzz.token_set_ratio(a, b)


if __name__ == '__main__':

	print(best_match("The_prophet_of_Mecca and Medina", "Mecca_Medina"))
