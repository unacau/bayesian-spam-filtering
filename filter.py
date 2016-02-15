from trainingcorpus import TrainingCorpus
from collections import Counter
import time
from corpus import Corpus
from Bayesian import Bayesian
from utils import load_pickle, find_sender, create_pickle, create_csv
from tokenizer import tokenize

start_time = time.time()
# MyFilter class
# MyFilter can learn from data
# it creates 3 data files:
#   spams.pickle stores the number each word occurs in SPAMS
#   hams.pickle stores the number each word occurs in HAMS
#   sender_bl.pickle stores email addresses of SPAM senders
# filter has already learned at big data sets, and because of it
# I'll comment train method. Data is really come from the learning process
# it can be easy checked by calling train method
# test method check if sender is in Blacklist
# and then use Bayesian approach to determine if the email is SPAM or HAM


class MyFilter:
    def __init__(self):
        self.counter_spams = Counter()
        self.counter_hams = Counter()
        self.subject_bl = []
        self.sender_bl = []

    def train(self, path):
        # train_corp = TrainingCorpus(path)
        # count_spams = 0
        # count_hams = 0
        #
        # # learn from spams and hams
        # # in case of SPAMS find sender and create Blacklist for them
        # # tokenize text and count how much each word occurs in text
        # for fname, body in train_corp.spams():
        #     count_spams += 1
        #     sender = find_sender(body)
        #     self.sender_bl.append(sender)
        #     create_pickle('sender_bl', self.sender_bl)
        #     self.counter_spams.update(tokenize(body))
        # for fname, body in train_corp.hams():
        #     count_hams += 1
        #     self.counter_hams.update(tokenize(body))
        #
        # self.counter_spams['count_spams'] += count_spams  # add to dictionary number of spams
        # self.counter_hams['count_hams'] += count_hams     # and hams
        #
        # # save all information with .pickle
        # create_pickle('sender_bl.pickle', self.sender_bl)
        # create_pickle('spams.pickle', self.counter_spams)
        # create_pickle('hams.pickle', self.counter_hams)
        #
        # create_csv('spam_words.csv', self.counter_spams)
        # create_csv('ham_words.csv', self.counter_hams)
        pass

    def test(self, path):
        corp = Corpus(path)
        bs = Bayesian()
        count = 0
        sender_bl = load_pickle('sender_bl.pickle')
        # scan email and define if msg is SPAM or HAM
        # first check if sender occurs in sender Blacklist
        # then count spamicity of the word using the Bayes approach
        for fname, body in corp.emails():
            sender = find_sender(body)
            if sender in sender_bl:
                self.tag_it(path, fname, 'SPAM')
                continue

            spamicity_list = []
            count += 1
            tokens = tokenize(body)
            # compute spamicity for each word and create list of the values
            for el in tokens:
                word_spamicity = [el, bs.word_spamicity(el)]
                spamicity_list.append(word_spamicity)
            # prepare list for Bayes
            spamicity_list = [list(i) for i in set(map(tuple, spamicity_list))]  # remove duplicates from list
            spamicity_list.sort(key=lambda x: abs(0.5 - x[1]), reverse=True)
            prediction = bs.bayes_pred(spamicity_list[:15])  # Consider only 15 'words'
            if prediction > 0.9 or sender in sender_bl:
                self.tag_it(path, fname, 'SPAM')
            else:
                self.tag_it(path, fname, 'OK')

    def tag_it(self, path, fname, tag):
        with open(path + '/!prediction.txt', 'a', encoding="utf-8") as file:
            file.writelines(fname + ' ' + tag + '\n')


if __name__ == '__main__':
    # filter = MyFilter()
    # # filter.train(PATH)
    # filter.test(PATH)
    # print("--- %s seconds ---" % (time.time() - start_time))
    f = MyFilter()
    print(f.sender_bl)
