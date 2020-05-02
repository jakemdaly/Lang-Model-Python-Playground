from utils import *

def main():

	file = 'LRRH.txt'
	training_data = txtToSentences(file)
	EmpericalUnigramLanguageModel(training_data)


if __name__=='__main__':
	main()