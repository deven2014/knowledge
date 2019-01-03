#!/usr/bin/env python3

import sys

"""
Author: Liang Deng
Date: 2019-01-03
Version: 0.1
Revesion history:
2019-01-93, initiated version. v0.1
"""

class LearnWords:
    m_fn_sv = 'dict-sv'
    m_fn_en = 'dict-en'
    m_policy = ''
    m_f_path = './' # file path of the dictionary files, exclude file name
    m_words_sv = []
    m_words_en = []
    m_start_index = 0
    m_cursor = 0
    m_review_words = []

    def __init__(self, learn_index, path='./', policy = 'SIMPLE'):
        """
        - default policy is SIMPLE
        - further policys may be added in the furture
        """
        self.m_f_path = path
        self.m_policy = policy
        self.m_start_index = int(learn_index)
        self.m_cursor = int(learn_index)
        print(self.__str__())
        self.load_dict()

    def __str__(self):
        return('Learn words class V0.1. \nAuthor Liang Deng 2019.01.')

    def load_dict(self):
        """
        Load the dictionary files into two lists.
        """
        fn_sv = self.m_f_path + self.m_fn_sv
        fn_en = self.m_f_path + self.m_fn_en
        with open(fn_sv) as fsv:
            sv = fsv.read()
        with open(fn_en) as fen:
            en = fen.read()

        self.m_words_sv = sv.split('\n')
        self.m_words_en = en.split('\n')

        print('Load dictionary file finished. ')
        print('First language dict length is: ', len(self.m_words_sv))
        print(self.m_words_sv[0], self.m_words_sv[1], self.m_words_sv[2])
        print('Second language dict length is: ', len(self.m_words_en))
        print(self.m_words_en[0], self.m_words_en[1], self.m_words_en[2])

    def get_cursor(self):
        length = len(self.m_review_words)
        if length and (length > 10 or self.m_cursor < 0):
            return(1, self.m_review_words[0])
        return(0, self.m_cursor)

    def run(self):
        flag, cur = self.get_cursor() 
        if self.m_start_index == cur:
            # First word
            print('Start learn words in index ', cur)
        else:
            #print('cursor is ', cur)
            if cur < 0:
                return 0
        if flag:
            self.review_word(cur)
        else:
            self.learn_word(cur)
        return 1 

    def review_word(self, cur):
        # Review a word 
        sv = self.m_words_sv
        en = self.m_words_en
        print(cur, sv[cur], '\n\n -- Enter or \'y\' to indicate you know it. otherwise type \'n\'')
        s = input()
        #print('user input:', s)
        if s == '' or s == 'y':
            print('Explantation: ', en[cur], '\n\n -- Enter or \'y\' to indicate your answer is correct. otherwise type \'n\' or any key')
            s = input()
            #print('user input:', s)
            if s == 'n':
                #print('Keep this word to forgot list.')
                print('review words: ', self.m_review_words)
                return
        else:
            #print('Keep this word to forgot list.')
            print('Explantation: ', en[cur])
            print('review words: ', self.m_review_words)
            return

        # Remove this word from review list since the user know it.
        self.m_review_words.remove(cur)
        print('review words: ', self.m_review_words)


    def learn_word(self, cur):
        # Learn a word in normal
        sv = self.m_words_sv
        en = self.m_words_en
        print(cur, sv[cur], '\n\n -- Enter or \'y\' to indicate you know it. otherwise type \'n\'')
        s = input()
        #print('user input:', s)
        if s == '' or s == 'y':
            print('Explantation: ', en[cur], '\n\n -- Enter or \'y\' to indicate your answer is correct. otherwise type \'n\' or any key')
            s = input()
            #print('user input:', s)
            if s == 'n':
                #print('Add this word to forgot list.')
                self.m_review_words.append(cur)
                print('review words: ', self.m_review_words)
        else:
            #print('Add this word to forgot list.')
            self.m_review_words.append(cur)
            print('Explantation: ', en[cur])
            print('review words: ', self.m_review_words)

        self.m_cursor -= 1

if __name__ == '__main__':
    argc = len(sys.argv)
    path = ''
    print('run cmd with argc:', argc)
    for cmd in sys.argv:
        print(cmd)
    
    if argc < 2:
        print ('The legal command takes at least one parameter as index.')
        exit()

    if argc > 2:
        path = sys.argv[2]

    lw = LearnWords(sys.argv[1], path)
    while lw.run():
        pass
    print('Learn words finished.')
