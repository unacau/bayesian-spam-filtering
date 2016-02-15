from corpus import Corpus
from utils import read_classification_from_file


__author__ = 'Igor Ekishev'


PATH = '/home/expirience/Rph/uloha_SPAM/1'
TRUTH = '/!truth.txt'
SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'
TOKENS = "abcdefghijklmnopqrstuvwxyz0123456789-$'"
WHITESPACE1 = '!@()#%^&*+}{][|/*":;.,<>?=\`$~_'
WHITE = [{'@': ' '}, {'/': ' '}]
REGEX = '(\s\d+\s)'  # RegEx for clear integers
REGEXIP = '(((1[0-9]{2})|(2[0-5]{2})|[0-9]{1,2})\.){3}(((1[0-9]{2})|(2[0-5]{2})|[0-9]{1,2}))'


class TrainingCorpus(Corpus):

    def get_class(self, filename):
        dic = read_classification_from_file(self.path+TRUTH)
        return dic[filename]

    def is_spam(self, filename):
        if self.get_class(filename) == SPAM_TAG:
            return True
        else:
            return False

    def is_ham(self, filename):
        if self.get_class(filename) == HAM_TAG:
            return True
        else:
            return False

    def spams(self):
        count = 0
        for filename, body in self.emails():
            if self.is_spam(filename):
                count += 1
                yield filename, body
        print(count, 'mails are spams')

    def hams(self):
        for filename, body in self.emails():
            if self.is_ham(filename):
                yield filename, body


if __name__ == "__main__":
    newTr = TrainingCorpus(PATH)
    newTr.process_spams()