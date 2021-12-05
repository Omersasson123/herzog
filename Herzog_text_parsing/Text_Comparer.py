import re
from nltk.corpus import stopwords
import pandas as pd
import scipy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


gloveFile = "data/glove.6B.50d.txt"
pd.set_option("display.max_rows", None, "display.max_columns", None)


def loadGloveModel(gloveFile):
    print ("Loading Glove Model")
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print ("Done.",len(model)," words loaded!")
    return model


def preprocess(raw_text):
    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split
    words = letters_only_text.lower().split()

    # remove stopwords
    stopword_set = set(stopwords.words("english"))
    cleaned_words = list(set([w for w in words if w not in model]))
    #cleaned_words = list(set([w for w in words if w not in stopword_set]))

    return cleaned_words



def cosine_distance_between_two_words(word1, word2):
    return 1 - scipy.spatial.distance.cosine(model[word1], model[word2])


def cosine_distance_wordembedding_method(s1, s2):
    vector_1 = np.mean([model[word] for word in preprocess(s1)],axis=0)
    vector_2 = np.mean([model[word] for word in preprocess(s2)],axis=0)
    cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
    return round((1-cosine)*100, 2)


def calculate_heat_matrix_for_two_sentences(s1,s2):
    s1 = preprocess(s1)
    s2 = preprocess(s2)
    result_list = [[cosine_distance_between_two_words(word1, word2) for word2 in s2] for word1 in s1]
    result_df = pd.DataFrame(result_list)
    result_df.columns = s2
    result_df.index = s1
    return result_df


def heat_map_matrix_between_two_sentences(s1,s2):
    df = calculate_heat_matrix_for_two_sentences(s1,s2)
    fig, ax = plt.subplots(figsize=(5,5))
    ax_blue = sns.heatmap(df, cmap="YlGnBu")
    # ax_red = sns.heatmap(df)
    score = cosine_distance_wordembedding_method(s1, s2)
    return score, ax_blue


ss2 = 'Established in 1923, Fremont High School is a WASC‐accredited, ' \
      'four‐year public high school that offers a comprehensive educational' \
      ' program to students from Sunnyvale and Cupertino in the heart of Silicon Valley.' \
      ' Former Secretary of Education Arne Duncan, who visited FHS in May of 2013, noted, ' \
      'This school reflects, I think, the best of the United States. It’s incredibly diverse,' \
      ' with many first‐generation college‐goers, many who are new to the country who are chasing' \
      ' the American Dream and a high‐quality education. Over 100 teachers and 40 staff members' \
      ' support our diverse student body. FHS has a modified block schedule with each class meeting' \
      ' three times per week: twice for a longer block and once for a shorter 52‐minute block. ' \
      'There is a Flex period twice a week where students can designate their location to ' \
      'access teachers for support or enrichment activities.'
ss1 = ' automates the creation of AI-powered conversational interfaces for enterprises' \
      ' to support the customer journey across all digital touch points. The company solution ' \
      'uses natural language understanding to allow people to have two-way conversations, using' \
      ' both voice and chat, that simplify their access to information.  provides organizations ' \
      'with frictionless deployment and maintenance processes by automatically building a knowledge ' \
      'graph out of their existing content without any integrations, playbooks, or training data.  is ' \
      'aiming to enable enterprises to converse easily, convert more, and collect actionable customer ' \
      'insights along the way.'

ss3 = ' aims to develop and bring to market medical-grade cannabis using a genomic approach.' \
      ' The company will initially focus on creating improved cannabis varieties, focusing on yield,' \
      ' stability, and specific metabolite composition. The company is a subsidiary of . ' \
      ' development efforts will be based on the utilization of ’s computational' \
      ' predictive biology platform, which has already demonstrated success in addressing similar' \
      ' objectives for other crops.'


class Comparer():
    def __init__(self, data=None):
        self.model = loadGloveModel(gloveFile)
        self.data = {}
        for sent in data:
            cleaned = self.preprocess(sent)
            val = self.score(cleaned)
            print(cleaned, val)
            self.data[sent] = val

    ''' 
    Compare a dataset to itself.
    '''
    def __init__(self, names, data):
        assert len(names) == len(data)
        self.model = loadGloveModel(gloveFile)
        self.data = {}
        for i in range(len(names)):
            comp = ''.join([str(elem) for elem in data[i]])
            cleaned = self.preprocess(comp)
            val = self.score(cleaned)
            print(cleaned, val)
            self.data[names[i]] = val

    '''
    Compare two datasets
    '''
    def __init__(self, names0, data0, names1, data1):
        #assert len(names0) == len(names1) == len(data1) == len(data0)
        self.model = loadGloveModel(gloveFile)
        self.data = [{}, {}]
        for i in range(len(names0)):
            comp0 = ''.join([str(elem) for elem in data0[i]])
            cleaned0 = self.preprocess(comp0)
            val0 = self.score(cleaned0)
            self.data[0][names0[i]] = val0

        for i in range(len(names1)):
            comp1 = ''.join([str(elem) for elem in data1[i]])
            cleaned1 = self.preprocess(comp1)
            val1 = self.score(cleaned1)
            self.data[1][names1[i]] = val1


    def preprocess(self, raw_text):
        # keep only words
        letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

        # convert to lower case and split
        words = letters_only_text.lower().split()

        # remove stopwords
        # stopword_set = set(stopwords.words("english"))
        cleaned_words = list(set([w for w in words if w in self.model]))
        # cleaned_words = list(set([w for w in words if w not in stopword_set]))

        return cleaned_words

    def score(self, sentence):
        vec = [self.model[word] for word in sentence]
        return np.mean(vec, axis=0)

    def compare_all_data(self):
        df = None

        if len(self.data) == 1:
            df = pd.DataFrame(columns=self.data.keys(), index=self.data.keys())
            for s1 in self.data:
                for s2 in self.data:
                    score = self.compare_processed(self.data[s1], self.data[s2])
                    #print(s1, s2, score)
                    df.loc[s1][s2] = score
        elif len(self.data) == 2:
            #df = pd.DataFrame(columns=self.data[0].keys(), index=self.data[1].keys())
            df = pd.DataFrame()

            #
            # print("data")
            # print(self.data[0].keys())
            # print(self.data[1].keys())
            #
            #
            # print(df)


            for s1 in self.data[0].keys():
                for s2 in self.data[1].keys():
                    score = self.compare_processed(self.data[0][s1], self.data[1][s2])
                    df.at[s1, s2] = score
                    #df[s1][s2] = score
        #print(df)
        return df



    def compare_raw(self, s1, s2):
        vector_1 = np.mean([self.model[word] for word in preprocess(s1)], axis=0)
        vector_2 = np.mean([self.model[word] for word in preprocess(s2)], axis=0)
        cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
        return round((1 - cosine) * 100, 2)

    def compare_processed(self, a1, a2):

        cosine = scipy.spatial.distance.cosine(a1, a2)

        return round((1 - cosine) * 100, 2)


# model = loadGloveModel(gloveFile)
# heat_map_matrix_between_two_sentences(ss1, ss2)
#
# heat_map_matrix_between_two_sentences(ss1, ss3)
#
# heat_map_matrix_between_two_sentences(ss2, ss3)
#


