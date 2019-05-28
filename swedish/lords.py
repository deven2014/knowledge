#!/usr/bin/env python3

import sys
import lib.translator.translator as translator
import lib.imemory.imemory as imemory
import time

"""
Author: Liang Deng
Date: 2019-01-03
Version: 0.1
Revesion history:
2019-01-03, initiated version. v0.1
2019-02-14, added simple ui mode. v0.2
2019-02-18, correct ui mode. v0.2
2019-05-25, rewrite LearnWords class for iMemory engine support v0.3
"""
def getchar():
    try:
        # for Windows-based systems 
        import msvcrt 
        # If successful, we are on Windows 
        return msvcrt.getch() 
    except ImportError: 
        # for POSIX-based systems (with termios & tty support) 
        import tty, sys, termios 
    # raises ImportError if unsupported 

    fd = sys.stdin.fileno() 
    oldSettings = termios.tcgetattr(fd) 
    try: 
        tty.setcbreak(fd) 
        answer = sys.stdin.read(1) 
    finally: 
        termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings) 
    return answer 

class OLearnWords:
    m_fn_sv = 'dict-sv'
    m_fn_en = 'dict-en'
    m_policy = ''
    m_f_path = './' # file path of the dictionary files, exclude file name
    m_words_sv = []
    m_words_en = []
    m_start_index = 0
    m_cursor = 0
    m_review_words = []
    # if simple_ui is 1 not show any remind information
    m_simple_ui = 0

    def __init__(self, policy, simple_ui = 0, learn_index = 0):
        """
        - default policy is SIMPLE
        - further policys may be added in the furture
        """
        self.m_f_path = './' 
        self.m_policy = policy
        self.m_simple_ui = simple_ui
        self.m_start_index = int(learn_index)
        self.m_cursor = int(learn_index)
        print(self.__str__())
        self.output_config()
        self.load_dict()

    def __str__(self):
        return('Learn words class V0.2. \nAuthor Liang Deng 2019.02.')

    def output_config(self):
        print("\n------------------------------------")
        print("   Work dir: ", self.m_f_path)
        print("     Policy: ", self.m_policy)
        print("  Simple UI: ", self.m_simple_ui)
        print("Start index: ", self.m_start_index, '\n')

    def hint_print(self, *args):
        # simple ui will not print hint info
        #print('simple_ui is', self.m_simple_ui)
        if not self.m_simple_ui:
            print(*args)

    def hint_print_words(self, *args):
        # simple ui will not print hint info
        if not self.m_simple_ui:
            print(*args, end='', flush=True)

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
        #print(self.m_words_sv[0], self.m_words_sv[1], self.m_words_sv[2])
        print('Second language dict length is: ', len(self.m_words_en))
        #print(self.m_words_en[0], self.m_words_en[1], self.m_words_en[2])

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
        print(cur, sv[cur], end='', flush=True)
        self.hint_print('\n -- Enter or \'y\' to indicate you know it. otherwise type \'n\'')
        s = getchar()
        #s = input()
        #print('user input:', s)
        if s == '\n' or s == 'y':
            self.hint_print_words('Explantation:')
            print(' ', en[cur])
            self.hint_print(' -- Enter or \'y\' to indicate your answer is correct. otherwise type \'n\' or any key')
            s = getchar()
            #s = input()
            #print('user input:', s)
            if s == 'n':
                #print('Keep this word to forgot list.')
                self.hint_print('review words: ', self.m_review_words)
                return
        else:
            #print('Keep this word to forgot list.')
            self.hint_print_words('Explantation:')
            print(' ', en[cur])
            self.hint_print('review words: ', self.m_review_words)
            return

        # Remove this word from review list since the user know it.
        self.m_review_words.remove(cur)
        self.hint_print('review words: ', self.m_review_words)


    def learn_word(self, cur):
        # Learn a word in normal
        sv = self.m_words_sv
        en = self.m_words_en
        print(cur, sv[cur], end='', flush=True)
        self.hint_print('\n -- Enter \'y\' to indicate you know it. otherwise type \'n\'')
        #s = input()
        s = getchar()
        #print('user input:', s)
        if s == '\n' or s == 'y':
            self.hint_print_words('Explantation:')
            print(' ', en[cur])
            self.hint_print(' -- Enter or \'y\' to indicate your answer is correct. otherwise type \'n\' or any key')
            s = getchar()
            #s = input()
            #print('user input:', s)
            if s == 'n':
                #print('Add this word to forgot list.')
                self.m_review_words.append(cur)
                self.hint_print('review words: ', self.m_review_words)
        else:
            #print('Add this word to forgot list.')
            self.m_review_words.append(cur)
            self.hint_print_words('Explantation:')
            print(' ', en[cur])
            self.hint_print('review words: ', self.m_review_words)

        self.m_cursor -= 1

class LearnWords(object):
    """
    New LearnWords class using iMemory engine
    """

    def __init__(self, policy, simple_ui = 0, learn_index = 0):
        """
        """
        self.policy = policy
        self.firstloop = True 
        self.simple_ui = simple_ui
        self.start_index = int(learn_index)
        self.last_time = time.clock()
        print(self.__str__())
        self.output_config()

        # Initiate Translator and iMemory instances
        self.translator = translator.Translator('sv', 'en', False)
        self.imemory = imemory.iMemory('usr1', 'sv', False)

    def __str__(self):
        return('Learn words class V0.3. \nAuthor Liang Deng 2019.05.')

    def output_config(self):
        print("\n------------------------------------")
        print("     Policy: ", self.policy)
        print("  Simple UI: ", self.simple_ui)
        print("Start index: ", self.start_index, '\n')

    def hint_print(self, *args):
        # simple ui will not print hint info
        #print('simple_ui is', self.m_simple_ui)
        if not self.simple_ui:
            print(*args)

    def hint_print_words(self, *args):
        # simple ui will not print hint info
        if not self.simple_ui:
            print(*args, end='', flush=True)

    def show_menu(self):
        # Ask if need show user data
        if(self.firstloop):
            print('Will you want to view learning data?')
            print('1: Only learning data')
            print('2: Only learning history data')
            print('3: All data')
            print('n: No need', flush=True)
            s = getchar()
            if s == '1' or s == '3':
                self.imemory.print_user_learning_data()
            if s == '2' or s == '3':
                self.imemory.print_user_learning_history_data()

    def run(self):
        """
        """
        # First loop show menu 
        if(self.firstloop):
            self.show_menu()
            self.firstloop = False
            print('\nStart learn word\n')

        word, index = self.imemory.get_next_learn_word()
        word_translation = self.translator.query(word)
        word_answer = True

        print(word, flush=True, end='')
        # Record the learning start time
        self.last_time = time.clock()

        self.hint_print('\n -- Enter \'y\' to indicate you know it. otherwise type \'n\'')
        s = getchar()

        # Mastered a word
        if s == 'a':
            print(' ', word_translation)
            self.hint_print(' -- Mastered this word. Enter or \'y\' to indicate your answer is correct. otherwise type \'n\' or any key')
            s = getchar()
            if s == '\n' or s == 'y' or s == 'a':
                self.imemory.mastered_word(word)
                return 1

        if s == '\n' or s == 'y':
            self.hint_print_words(' Explantation:')
            print(' ', word_translation)
            self.hint_print(' -- Enter or \'y\' to indicate your answer is correct. otherwise type \'n\' or any key')
            s = getchar()
            if s == 'y':
                word_answer = True 
        else:
            word_answer = False
            self.hint_print_words('Explantation:')
            print(' ', word_translation)

        current_time = time.clock() 
        # Int() will not return the closer integer value
        learned_time = round((current_time - self.last_time) * 1000)
        self.last_time = current_time
        self.imemory.learn_word(word, learned_time, word_answer)

        return 1

if __name__ == '__main__':
    argc = len(sys.argv)
    engine_type = 'SIMPLE'
    ui_mode = 0
    index = -1
    #print('run cmd with argc:', argc)
    #for cmd in sys.argv:
    #    print(cmd)

    if argc == 1:
        engine_type = 'IMEMORY'
    else:
        engine_type = sys.argv[1]
        if engine_type == 'IMEMORY' and argc > 2:
            ui_mode = sys.argv[2]
        if engine_type == 'SIMPLE':
            if argc > 2:
                ui_mode = sys.argv[2]
            if argc > 3:
                index = sys.argv[3]

    print('Learning engine is ', engine_type)
    print(ui_mode, index)

    # TODO: LearnWord is a seperate module, in the furture there will be 
    # Other modules like LearnRead, etc.
    if engine_type == 'SIMPLE':
        lw = OLearnWords(engine_type, ui_mode, index)
    else:
        lw = LearnWords(engine_type, ui_mode, index)

    while lw.run():
        pass
    print('Learn words finished.')
