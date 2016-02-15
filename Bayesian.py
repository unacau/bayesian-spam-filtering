from utils import load_pickle

__author__ = 'Igor Ekishev'
# class for Bayesian approach


class Bayesian:
    def __init__(self):
        self.spams_dict = load_pickle('spams.pickle')
        self.hams_dict = load_pickle('hams.pickle')

    def spam_prob(self, word):
        prob = self.spams_dict[word] / self.spams_dict['count_spams']
        if prob > 1:
            return 1.0
        else:
            return prob

    def ham_prob(self, word):
        prob = self.hams_dict[word]/ self.hams_dict['count_hams']
        if prob > 1:
            return 1.0
        else:
            return prob

    def word_spamicity(self, word):
        # spamicity of the word which occurs only in spams is 0.99
        # and 0.01 for the words which occurs only in hams
        if self.spams_dict[word] > 2 and self.hams_dict[word] == 0:
            return 0.99
        elif self.spams_dict[word] == 0 and self.hams_dict[word] > 2:
            return 0.01
        elif word in self.spams_dict and word in self.hams_dict:
            if self.spams_dict[word] + self.hams_dict[word] >= 3:  # if the words occurs in both more than five
                return self.spam_prob(word) / ((self.ham_prob(word)) + self.spam_prob(word))
            else:
                return 0.5
        else:
            return 0.4

    def bayes_pred(self, tokens):
        up = 1.0  # Part of Bayes' Formula
        down = 1.0
        for element in tokens:
            up = up * element[1]
            down = down * (1 - element[1])
        if (up == 0 or down == 0):
            up = 0.5
        pred = up / (up + down)
        return pred


if __name__ == '__main__':
    bs = Bayesian()
    print(bs.word_spamicity(''))
    print(bs.bayes_pred([['corp', 0.05015218918286116], ['ad', 0.8954269122584158], ['fees', 0.8924405039664023], ['monthly', 0.8841708542713568], ['reply', 0.8770830555925877], ['em', 0.8745236799129015], ['zzzz', 0.8494448073154801], ['webnote', 0.8342620888010066], ['receiving', 0.8164224275246894], ['distance', 0.784981343283582], ['may', 0.7727272727272727], ['jmason', 0.23730741391789886], ['remove', 0.7587869963828288], ['subscription', 0.249185667752443], ['directed', 0.749183895538629]]))
    #print(bs.hams_dict)