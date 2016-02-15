import os
import re
import pickle
import email
import csv

__author__ = 'Igor Ekishev'

REGEX_EMAIL = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'


def read_classification_from_file(path):
    mails_classification = {}
    with open(path, encoding="utf-8") as my_file:
        if os.stat(path).st_size > 0:
            while True:
                theline = my_file.readline()
                if len(theline) == 0:
                    break
                split_line = theline.split()
                mails_classification[split_line[0]] = split_line[1]

            return mails_classification
        else:
            return dict()


def tag_it(path, fname, tag):
    with open(path+'/!prediction.txt', 'a', encoding="utf-8") as file:
        file.writelines(fname + ' ' + tag + '\n')


def load_pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def process_file(path):
    with open(path) as file:
        line = file.readlines()
        for el in line:
            tmp = el.split()
            yield tmp[0], tmp[1]
            print(el.split())


def crf(path):
    with open(path, 'w', encoding='utf-8') as file:
        for tag, fname in process_file('/home/expirience/Rph/uloha_SPAM/TRAINING/!label.txt'):
            if tag == '0':
                file.writelines(fname + ' SPAM\n')
            if tag == '1':
                file.writelines(fname + ' OK\n')


def find_sender(text):
    msg = email.message_from_string(text)
    sender = re.findall(REGEX_EMAIL, msg['From'])
    if len(sender) > 0:
        sender = str.lower(sender[0])
    return sender


def create_csv(filename, dict):
    with open(filename, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for key, value in dict.items():
            writer.writerow([key, value])


def create_csv_from_list(filename, list):
    with open(filename, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for first, second in list:
            writer.writerow([first, second])


def create_pickle(filename, obj):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)

if __name__ == '__main__':
    #print(read_classification_from_file('/home/expirience/Rph/uloha_SPAM/1/!truth.txt'))
    #print(read_classification_from_file_upd('/home/expirience/Rph/uloha_SPAM/TRAINING/SPAMTrain.label'))
    #process_file('/home/expirience/Rph/uloha_SPAM/TRAINING/!truth.txt')
    crf('/home/expirience/Rph/uloha_SPAM/TRAINING/!truth.txt')