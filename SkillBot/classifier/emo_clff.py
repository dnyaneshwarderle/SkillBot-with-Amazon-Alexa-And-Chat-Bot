from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from nltk.stem.porter import PorterStemmer
import _pickle as cPickle


class EmoClf:

    def __init__(self):
        self.model_path = "./model.joblib"
        self.stemmer = PorterStemmer()
        self.clf, self.cv = self.trainer()


    def trainer(self):
        # import pdb; pdb.set_trace()
        if not os.path.exists(self.model_path):
            reviews_train = self.data_loader()
            reviews_train_clean = self.clean(reviews_train)
            stemmed_reviews_list = self.get_stemmed_text(reviews_train_clean)
            clf, cv = self.stemmed_review(stemmed_reviews_list)
            self.feat_to_coeff(clf, cv)
            joblib.dump(clf, self.model_path)
            with open('./storage.bin', 'wb') as f:
                cPickle.dump(cv, f)
        else:
            clf = joblib.load(self.model_path)
            with open('storage.bin', 'rb') as f:
                cv = cPickle.load(f)

        return clf, cv


    def tester(self, query):
        
        reviews_train_clean = self.clean([query])
        stemmed_reviews_list = self.get_stemmed_text(reviews_train_clean)
        vectorized_test = self.cv.transform(stemmed_reviews_list)
        pred_proba = self.clf.predict_proba(vectorized_test)
        # print (pred_proba)
        emotion_dct = {"positive":pred_proba ,"negative":1-pred_proba}
        return emotion_dct

    def data_loader(self):
        reviews_train = []

        with open('./data/training/full_train.txt','r') as fp:
            reviews_train =  [each_line.strip() for each_line in fp.readlines()[:]]

        return reviews_train


    def preprocess_reviews(self, reviews):
        REPLACE_NO_SPACE = re.compile(r"(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
        REPLACE_WITH_SPACE = re.compile(r"(<br\s*/><br\s*/>)|(\-)|(\/)")
        NO_SPACE = ""
        SPACE = " "
        reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
        reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]

        return reviews

    def clean(self, reviews_list):
        reviews_list_clean = self.preprocess_reviews(reviews_list)
        return reviews_list_clean

    def get_stemmed_text(self, corpus):

        return  [' '.join([self.stemmer.stem(word) for word in review.split()]) for review in corpus]


    def stemmed_review(self, stemmed_reviews_list):
        #reviews_train

        cv = CountVectorizer(binary=True)
        cv.fit(stemmed_reviews_list)
        X = cv.transform(stemmed_reviews_list)
        target = [1 if i < 12500 else 0 for i in range(25000)]

        X_train, X_val, y_train, y_val = train_test_split(X, target, train_size = 0.75)

        clf = LogisticRegression(C=0.05)
        clf.fit(X, target)
        # print ("Final Accuracy: %s"
        #     % accuracy_score(target, clf.predict(X_test)))
        return clf, cv


    def feat_to_coeff(self, clf, vectorized):

        feature_to_coef = { word: coef for word, coef in zip(
        vectorized.get_feature_names(), clf.coef_[0] )}

        for best_positive in sorted(
            feature_to_coef.items(),
            key=lambda x: x[1],
            reverse=True)[:30]:
                print (best_positive)

        print("\n\n")
        for best_negative in sorted(
            feature_to_coef.items(),
            key=lambda x: x[1])[:30]:
                print (best_negative)


if __name__=="__main__":
    obj = EmoClf()
    while True:
        obj.tester(input("Q: "))