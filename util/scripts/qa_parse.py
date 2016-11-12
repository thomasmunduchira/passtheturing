import re
import zipfile
from pymongo import MongoClient
import string

URI = "mongodb://admin:alanturing9448@ds151707.mlab.com:51707/passtheturing"

mc = MongoClient(URI)
db = mc.passtheturing

pairs = {}

def parsePairs(file):
	results = []
	questions = []
	responses = []

	#qa pairs
	results = re.findall(r'[A-Za-z,;\'\"\\\s]+-*[A-Za-z,;\'\"\\\s]+[?][^.!]+[.!]', file, re.M)
	
	#split off questions, remove newlines, trailing dashes and whitespace
	results = [re.split(r'[?]', result, 1, re.M) for result in results]
	questions = [re.sub(r'[\n\r]+', ' ', question[0] + '?').lstrip() for question in results]
	questions = [re.findall(r'[A-Za-z,;\'\"\\\s]+-*[A-Za-z,;\'\"\\\s]+[?]', question, re.M) for question in questions]
	for question in questions:
		if len(question) == 0:
			question.append("SFj;SPIFHPISFHSPFHSPFHSOGN:LWOGIPWGBPIWGBIPWGBWGW?")
	questions = [question[0].lstrip() for question in questions]

	#find answers in latter half of split, remove newlines, trailing dashes and whitespace
	answers = [re.findall(r'[A-Za-z,;\'\"\\\s]+-*[A-Za-z,;\'\"\\\s]+[.!]', answer[1], re.M) for answer in results]
	for answer in answers:
		if len(answer) == 0:
			answer.append("Lol.")
	answers = [re.sub(r'[\n\r]+', ' ', answer[0]).lstrip() for answer in answers]
	answers = [re.findall(r'[A-Za-z,;\'\"\\\s]+-*[A-Za-z,;\'\"\\\s]+[.!]', answer, re.M) for answer in answers]
	for answer in answers:
		if len(answer) == 0:
			answer.append("Lol.")
	answers = [answer[0].lstrip() for answer in answers]
	
	#fill dict
	for i in range(0, len(questions)):
		pairs[questions[i]] = answers[i];

	#print formatted pairs
	for pair in pairs:
		print(pair, pairs[pair])

		pair_clean = pair.translate(None, string.punctuation).lower().strip()

		check_existing = db.dialogue.find_one({"query_clean" : pair_clean})

		if check_existing != None:
			update = True
			for response in check_existing['responses']:
				if clean(pairs[pair]) == response[2]:
					update = False
			if update:
				db.dialogue.update({"query_clean" : pair_clean}, {"$push" : {"responses" : [pairs[pair], 0, clean_input(pairs[pair])]}})

		if "?" in pair:
			query_type = "question"
		else:
			query_type = "statement"

		db.dialogue.insert({"query" : pair,
							"query_type" : query_type,
							"query_clean" : clean_input(pair),
							"responses" : [[pairs[pair], 0, clean_input(pairs[pair]) ]] })

def parseZip(zipInput):
	with zipfile.ZipFile(zipInput,'r') as zip:
		parsePairs(zip.read(zip.infolist()[0]))

def parseTxt(txtInput):
	with open(txtInput) as fileStream: 
		parseTxt(fileStream.read())

def clean_input(s):
	return s.translate(None, string.punctuation).lower().strip()

#testCase		
parseZip('C:/Users/Vincent/Desktop/Turing/passtheturing/util/scripts/subs/StarWars6.zip')

