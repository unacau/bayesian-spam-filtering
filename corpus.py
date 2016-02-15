import os
import codecs

__author__ = 'Igor Ekishev'

PATH = '/home/expirience/Rph/uloha_SPAM/1'


class Corpus():
    def __init__(self, path):
        self.path = path
        self.dir_content = os.listdir(self.path)

    def emails(self):
        self.delete_special_files()
        for i in range(len(self.dir_content)):
            with codecs.open(self.path + '/' + self.dir_content[i], "r",encoding='utf-8', errors='ignore') as file:
                filename = self.dir_content[i]
                body = file.read()
                yield filename, body

    def delete_special_files(self):
        for element in self.dir_content:
            if "!" in element:
                self.dir_content.remove(element)

if __name__ == "__main__":
    corpus = Corpus(PATH)
    count = 0

    for fname, body in corpus.emails():
        print(fname)
        print(body)
        print('---------------------')
        count += 1
    print('Finished: ', count, 'files processed.')