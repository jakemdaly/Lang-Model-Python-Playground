from abc import ABC, abstractmethod
import numpy as np
from math import log10

null = 0

class NgramLanguageModel(ABC):

	"""
	NgramLanguageModel abstract base class. All NgramLanguageModels inherit from this.
	"""

	start = '<s>'
	stop = '</s>'

	@abstractmethod
	def __init__():
		pass

	@abstractmethod
	def getOrder():
		pass

	@abstractmethod
	def getNgramLogProbability(ngramIntArr, fromInt, toInt):
		pass

	@abstractmethod
	def getCount(ngramIntArr):
		pass


class EmpericalUnigramLanguageModel(NgramLanguageModel):

	"""
	Empircal unigram model. Inherits NgramLanguageModel class.
	
	__init__
	:param trainingData:	List of strings to train the data on. Strings are sentences

	"""

	def __init__(self, trainingData):

		self.total = 0
		self.wordCounter = np.empty(10)

		print("Building EmpericalUnigramLanguageModel...")

		sent = 0

		for s in trainingData:
			sent += 1
			stoppedSentence = listOfWords(s)
			stoppedSentence = [self.start] + stoppedSentence + [self.stop]
			for word in s:
				index = EnglishWordIndexer().getIndexer().addAndGetIndex(word)
				if (index >= len(self.wordCounter)):
					self.wordCounter = copyOf(self.wordCounter, len(self.wordCounter)*2)
				self.wordCounter[index] += 1

		print("Done building EmpericalUnigramLanguageModel.")
		self.wordCounter = copyOf(self.wordCounter, EnglishWordIndexer().getIndexer().size())
		total = sum(self.wordCounter)


	def getOrder():
		return(1)

	def getNgramLogProbability(ngramIntArr, fromInt, toInt):
		
		if (toInt - fromInt != 1):
			print("WARNING: to - from > 1 for EmpericalUnigramLanguageModel")
		word = ngramIntArr[fromInt]
		return(log10(1) if (word < 0 or word >= len(self.wordCounter)) else log10(self.wordCounter[word]/(self.total + 1.0)))


	def getCount(ngramIntArr):
		
		if (len(ngramIntArr)>1):
			return(0)
		word = ngramIntArr[0]
		if (word < 0 or word >= len(self.wordCounter)):
			return(0)
		return(self.wordCounter[word])

class EnglishWordIndexer():

	def __init__(self):
		self.indexer = StringIndexer()

	def getIndexer(self):
		return(self.indexer)

class StringIndexer():

	def __init__(self):
		self.serialVersionUID = -8769544079133660516
		self.objects = []
		self.indexes = TIntOpenHashMap()

	def get(self, index):
		return(self.objects[index])

	def size(self):
		return(len(self.objects))

	def indexOf(self, obj):
		if not isinstance(obj, str):
			return(-1)
		index = self.indexes.get(obj)
		return(index)

	def addAndGetIndex(self, elem):
		index = self.indexes.get(elem)
		if (index >= 0):
			return(index)

		# self.size()?
		newIndex = size()
		objects.add(elem)
		indexes.put(elem, newIndex)
		return(newIndex)

	#NOT IMPLEMENTED:
	# def add(elem)


class TIntOpenHashMap():

	def __init__(self, initialCapacity=10, loadFactor = .7):
		self.size = 0
		self.MAX_LOAD_FACTOR = loadFactor
		cap = max(5, int(initialCapacity/loadFactor))
		self.values = np.array([-1]*cap)
		self.keys = np.array(['']*cap)

	def put(self, k, v):
		if (self.size/len(keys) > MAX_LOAD_FACTOR):
			rehash()
		return(putHelp(k, v, self.keys, self.values))

	def putHelp(self, k, v, keyArray, valueArray):
		pos = getInitialPos(k, keyArray)
		curr = keyArray[pos]
		while (curr != null and not(curr == k)):
			pos += 1
			if (pos == len(keyArray)):
				pos = 0
			curr = keyArray[pos]
		valueArray[pos] = v
		if (curr==null):
			size += 1
			keyArray[pos] = k;
			return(True)
		return(False)


	def getInitialPos(self, k, keyArray):
		hash_val = hash(k)
		pos = hash_val % len(keyArray)
		if (pos < 0):
			pos += len(keyArray)
		return(pos)

	def find(self, k):
		pos = self.getInitialPos(k, self.keys)
		curr = self.keys[pos]
		while (curr != null and not(curr == k)):
			pos += 1
			if (pos == len(self.keys)):
				pos = 0
			curr = self.keys[pos]
		return(pos)

	def get(self, k):
		pos = self.find(k)
		return(pos)

	def increment(self, k, c):
		pos = find(k)
		currKey = self.keys[pos]
		if (currKey==null):
			put(k, c)
		else:
			self.values[pos] += 1

	# Implement later if needed... for now throw false assert
	def Entry():
		print("\nFunction not yet defined\n")
		assert(False)

	def EntryIterator():
		print("\nFunction not yet defined\n")
		assert(False)

	def MapIterator():
		print("\nFunction not yet defined\n")
		assert(False)
		
	def rehash():
		print("\nFunction not yet defined\n")
		assert(False)

def copyOf(arr, new_len):
	ret = np.empty(new_len)
	try:
		ret[:len(arr)] = arr
	except:
		print("copyOf: arr length longer than new array length")
	return(ret)

def txtToSentences(text_file):

	with open(text_file) as reader:
		sentences = [s for s in reader]

	sentences = [sen for sen in sentences if sen != '\n']

	for s in range(len(sentences)):
		
		sentences[s] = sentences[s].replace('\n', '')
		#TODO: Not sure how java project deals with periods yet. 
		sentences[s] = sentences[s].replace('.', '')
	
	return(sentences)

def listOfWords(sentence):

	return(sentence.split(' '))