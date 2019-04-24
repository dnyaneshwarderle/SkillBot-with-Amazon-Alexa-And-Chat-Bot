from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re
import string

def convertingdata():


	demoflag = False
	for i in range(1):
		example_sent = input("Kuch input toh de ..:p : ")

		translation = str.maketrans("","", string.punctuation);
		new = example_sent.translate(translation);
		lower = new.lower();
		
		print("User Value: ", example_sent)
		print("Converting to Lower and removing punctuation: ",lower)
		original = re.sub("\s\s+" , " ", lower)
		print("Space and punctuation removed: ", original)

	stop_words = set(stopwords.words('english'))
	# print("stopwords ki length: ",len(stop_words))
	word_tokens = word_tokenize(original)
	print("word_tokens ki length: ",len(word_tokens))

	filtered_sentence = [w for w in word_tokens if not w in stop_words]
	filtered_sentence = []


	for w in word_tokens:
		if w not in stop_words:
			filtered_sentence.append(w)
			if len(stop_words) >= 0:
				# print("Length: ",len(filtered_sentence))
				demoflag = True
				# print("Valid")
			else:
				demoflag = False

	if demoflag:
		print("Valid")
	else:
		print("Invalid")
	print("Fileterd Sentence: ",filtered_sentence)

data=convertingdata()
