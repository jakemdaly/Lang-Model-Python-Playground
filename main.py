"""
main module for building classes
"""

from utils import *

def main():

	# You can use a small text file here to train your models
	file = 'LRRH.txt'
	training_data = txtToSentences(file)

	# # OR use a simple sentence to play with an even smaller model
	# training_data = ["The mean wolf got hungry and so he ate something"]

	# Instantiate model
	lrrh_unigram = EmpericalUnigramLanguageModel(training_data)

	# Test example
	test_sentence = "The wolf ate the grandma"
	log_prob = lrrh_unigram.getNgramLogProbability(test_sentence)

	print('Log probability of "%s":\n\t%s'%(test_sentence,log_prob))

if __name__=='__main__':
	main()