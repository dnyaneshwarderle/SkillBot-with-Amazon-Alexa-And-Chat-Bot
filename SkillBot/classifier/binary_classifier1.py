import os
import json
import pandas
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk, pdb
import re
import string

class BinaryClassifier:

	def __init__(self):
	    self.training_data_path = "./data/training"
	    self.model_path = "./model/model.sav"
	    self.vectorizer = TfidfVectorizer(max_features=10)
	    self.mapping_class = ({"general": 1, "greeting": 0, "test": 2, "learn": 3})
	    self.training()

	def data_loader(self):
	    x_train = []
	    y_train = []
	    # pdb.set_trace()
	    for each_path in os.listdir(self.training_data_path):
	        with open(self.training_data_path+"/"+each_path) as fp:
                    data = fp.readlines()
                    for each_line in data[:10]:
                        x_train.append(each_line.rstrip("\n"))
                        y_train.append(each_path[:-4])
	    # print (json.dumps(x_train, indent=4))
	    # print (json.dumps(y_train, indent=4))

	    return x_train, y_train

	def training(self):

	    x_train, y_train = self.data_loader()

	    x_train_vec = self.vectorizer.fit_transform(x_train)

	    df = pandas.DataFrame(y_train)
	    # pdb.set_trace()
	    df = df.replace(self.mapping_class)
	    # df = df.replace({"general": 1, "greeting": 0})
	    y_train_vec = list(df[0])

	    clf = SVC(C=1, kernel="linear", probability=True)
	    clf.fit(x_train_vec, y_train_vec)

	    pred = clf.predict(x_train_vec)

	    print ("Model accuracy is ", accuracy_score(y_train_vec, pred))

	    pickle.dump(clf, open(self.model_path, 'wb'))


	def tester(self, text):
		class_dct  = {
			"label": "",
			"score": 0
		}

		test_observation = self.vectorizer.transform([text])
		model = pickle.load(open(self.model_path, 'rb'))
		prediction = model.predict(test_observation)
		pred_prob = model.predict_proba(test_observation)

		print ("Prediction ", prediction, pred_prob)
		for label, label_map in self.mapping_class.items():
			if label_map in prediction:
				class_dct["label"] = label
				print(label)
				class_dct["score"] = pred_prob[0][label_map]
				break

		return class_dct



if __name__=="__main__":
    obj = BinaryClassifier()
    while True:
	    obj.tester(input("Q: "))
    # obj.tester("hi")
