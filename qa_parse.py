import re
import zipfile

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
	questions = [re.findall(r'[A-Za-z,;\'\"\\\s]+-*[A-Za-z,;\'\"\\\s]+[?]', question, re.M)[0].lstrip() for question in questions]

	#find answers in latter half of split, remove newlines, trailing dashes and whitespace
	answers = [re.findall(r'[A-Za-z,;\'\"\\\s]+-*[A-Za-z,;\'\"\\\s]+[.!]', answer[1], re.M) for answer in results]
	answers = [re.sub(r'[\n\r]+', ' ', answer[0]).lstrip() for answer in answers]
	answers = [re.findall(r'[A-Za-z,;\'\"\\\s]+-*[A-Za-z,;\'\"\\\s]+[.!]', answer, re.M)[0].lstrip() for answer in answers]

	#fill dict
	for i in range(0, len(questions)):
		pairs[questions[i]] = answers[i];
	
	#print formatted pairs
	for pair in pairs:
		print(pair, pairs[pair])

def parseZip(zipInput):
	with zipfile.ZipFile(zipInput,'r') as zip:
		parsePairs(zip.read(zip.infolist()[0]))

def parseTxt(txtInput):
	with open(txtInput) as fileStream: 
		parseTxt(fileStream.read())

#testCase		
#parseZip('C:/Users/Vincent/Desktop/BreakfastZip.zip')
