import Levenshtein as ls

import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
signals = ['calculate', 'get', 'find']

from nltk.util import ngrams

from spellchecker import SpellChecker

from .models import *

from bs4 import BeautifulSoup

import requests

data = [x['skill'] for x in list(BaseSkill.objects.all().values("skill"))]

spell = SpellChecker()

def clean_string(text):
	text = ''.join([word for word in text if word not in string.punctuation])
	text = text.lower()
	text = ' '.join([word for word in text.split() if word not in stopwords])
	text = ' '.join([word for word in text.split() if word not in signals])
	return text

def clean_string2(text):
	text = ''.join([word for word in text if word not in string.punctuation])
	text = text.lower()
	text = ' '.join([word for word in text.split() if word not in stopwords])
	return text

def correctspelling(s):
	s = " ".join([spell.correction(z) for z in s.split()])
	s = clean_string(s)
	return " ".join([spell.correction(z) for z in s.split()])

def cosine_sim_vectors(vec1, vec2):
	vec1 = vec1.reshape(1, -1)
	vec2 = vec2.reshape(1, -1)

	return cosine_similarity(vec1, vec2)[0][0]

def stringsim(sample):
	clean_sample = list(map(correctspelling, sample))

	vectorizer = CountVectorizer().fit_transform(sample)
	vectors = vectorizer.toarray()

	return cosine_sim_vectors(vectors[0], vectors[1])

def build_ngrams(text, n=2):
	ngramlist = []
	for t in text:
		t = clean_string(t)
		tokens = nltk.word_tokenize(t)
		for nl in list(nltk.ngrams(tokens, n)):
			ngramlist.append(nl)
	return ngramlist

data = [clean_string(d) for d in data]

tvx = TfidfVectorizer()
vx = tvx.fit_transform(data)

cvx = CountVectorizer(analyzer='word', ngram_range=(2, 2))
cv = cvx.fit_transform(data)

def extract_text_from_website(url):
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, "html5lib")
	text = soup.get_text()
	print(text)


	