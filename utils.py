"""
Utilities for constructing language models, implemented in python
Some of the classes and methods in this file were originally implemented by Adam Pauls and Dan Klein of UC Berkley

Note:
	- The tokens undergo little processing. I did a few things like removing double quotes, end of sentence punctuation, splitting commas out from words
		- You can edit this to your liking in the method txtToSentences(text_file) at the bottom of the file.
	- I did not implement the testing classes of the original libraries
"""


from abc import ABC, abstractmethod
import pdb
from math import log10

null = -1

# Size of the wordCounter variable (list containing counts of unigrams)
wordCounterSize = 200 # For LRRH.txt, 200 is fine

class NgramLanguageModel(ABC):

	"""
	NgramLanguageModel abstract base class. All NgramLanguageModels inherit from this.
	"""

	start = '<s>'
	stop = '</s>'

	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def getOrder(self):
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
	:param trainingData:	List of strings to train the data on. Strings are sentences.
	"""

	def __init__(self, trainingData):

		self.total = 0
		self.wordCounter = [0]*200

		print("Building EmpericalUnigramLanguageModel...")

		sent = 0
		self.StrInd = StringIndexer()

		for s in trainingData:
			sent += 1
			stoppedSentence = listOfWords(s)
			stoppedSentence = [self.start] + stoppedSentence + [self.stop]
			for word in stoppedSentence:
				index = self.StrInd.addAndGetIndex(word)
				if (index >= len(self.wordCounter)):
					self.wordCounter = copyOf(self.wordCounter, len(self.wordCounter)*2)
				self.wordCounter[index] += 1

		print("Done building EmpericalUnigramLanguageModel.")
		self.wordCounter = copyOf(self.wordCounter, self.StrInd.size())
		self.total = sum(self.wordCounter)


	def getOrder(self):
		"""
		Get the order of the unigram model.

		:return 1: Unigram order is 1
		"""
		return(1)

	def getNgramLogProbability(self, testSentence):
		"""
		Use to compute the probability of testSentence, given the trained unigram model. For accurate results, use the
		same rules for formatting the sentences as the txtToSentences() function at the bottom of the file. For example,
		if the comma is broken out there, make sure to make your testSentence = "Hi , how are you"

		:param testSentence: Single string containing words, eg. "Hello how are you?"
		:return log_prob: log probability of sequence of words contained in testSentence given unigram model
		"""
		words = listOfWords(testSentence)
		log_prob = 0

		for word in words:
			indx = self.StrInd.indexOf(word)
			count = self.wordCounter[indx]
			if count==0:
				log_prob += 0
			else:
				log_prob += log10(count/(self.total+1))

		return(log_prob)


	def getCount(self, ngramIntArr):
		
		if (len(ngramIntArr)>1):
			return(0)
		word = ngramIntArr[0]
		if (word < 0 or word >= len(self.wordCounter)):
			return(0)
		return(self.wordCounter[word])


class StringIndexer:

	"""
	StringIndexer class used for managing the training data seen at train time.
	"""

	def __init__(self):
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
		newIndex = self.size()
		self.objects.append(elem)
		self.indexes.put(elem, newIndex)
		return(newIndex)


class TIntOpenHashMap:

	"""
	Hash map for storing keys. Rehash not yet implemented (data set is very small, so we can preallocate a large enough
	initial capacity and not worry about overloading the hash table
	"""

	def __init__(self, initialCapacity=wordCounterSize, loadFactor = .7):
		self.size = 0
		self.MAX_LOAD_FACTOR = loadFactor
		cap = max(5, int(initialCapacity/loadFactor))
		self.values = [-1]*cap
		self.keys = ['null']*cap

	def put(self, k, v):
		if (self.size/len(self.keys) > self.MAX_LOAD_FACTOR):
			self.rehash()
		return(self.putHelp(k, v, self.keys, self.values))

	def putHelp(self, k, v, keyArray, valueArray):
		pos = self.getInitialPos(k, keyArray)
		curr = keyArray[pos]
		while (curr != 'null' and not(curr == k)):
			pos += 1
			if (pos == len(keyArray)):
				pos = 0
			curr = keyArray[pos]
		valueArray[pos] = v
		if (curr=='null'):
			self.size += 1
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
		while (curr != 'null' and not(curr == k)):
			pos += 1
			if (pos == len(self.keys)):
				pos = 0
			curr = self.keys[pos]
		return(pos)

	def get(self, k):
		pos = self.find(k)
		return(self.values[pos])

	def increment(self, k, c):
		pos = self.find(k)
		currKey = self.keys[pos]
		if (currKey=='null'):
			self.put(k, c)
		else:
			self.values[pos] += 1

	# Implement later if needed... for now throw false assert
	def Entry(self):
		print("\nFunction not yet defined\n")
		assert(False)

	def EntryIterator(self):
		print("\nFunction not yet defined\n")
		assert(False)

	def MapIterator(self):
		print("\nFunction not yet defined\n")
		assert(False)
		
	def rehash(self):
		print("\nFunction not yet defined\n")
		assert(False)

def copyOf(arr, new_len):

	"""
	Used to extend the length of arr to size of new_len.
	:param arr: initial array to be resized
	:param new_len: size of the new array
	:return:
	"""

	ret = [0]*new_len
	try:
		ret[:len(arr)] = arr
	except:
		print("copyOf: arr length longer than new array length")
	return(ret)

def txtToSentences(text_file):

	"""
	Convert text file to a list of sentences. Perform any tokenization rules you need here.
	:param text_file:
	:return:
	"""

	with open(text_file) as reader:
		sentences = [s for s in reader]

	sentences = [sen for sen in sentences if sen != '\n']

	for s in range(len(sentences)):

		# Tokenization rules
		sentences[s] = sentences[s].replace('\n', '')
		sentences[s] = sentences[s].replace('.', '')
		sentences[s] = sentences[s].replace('!', '')
		sentences[s] = sentences[s].replace('?', '')
		sentences[s] = sentences[s].replace(',', ' ,')
		sentences[s] = sentences[s].replace('"', '')
	
	return(sentences)

def listOfWords(sentence):

	return(sentence.split(' '))