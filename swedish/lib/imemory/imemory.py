import os
import json

# data dir, can be extend for configurable
MODULE_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(MODULE_PATH, 'data')
UID_2_INDEX_FILE = 'uid2index.json'
WORD_2_INDEX_FILE = 'word2index.json'

# How long a mastered word should be reviewed at least once
WORD_MUST_REVIEW = 1000
# Maximum 100 words in learning.
LEARNING_WORD_WINDOW = 100
# Mastered score counting config, total 100
# 5,7,15,24,49. 25 times correct will get 100 score
MASTERED_SCORE_COUNT_CONFIG = (1, 1, 1, 1, 1,
                               1, 1, 1, 2, 2,
                               2, 3, 3, 3, 4,
                               4, 4, 5, 5, 6,
                               6, 7, 9,12,15)

class iMemory:
    """

    """
    version = '1.0.0'
    desc = 'iMemory library. Design for efficient memory for learning languages.'

    # Configuration
    language_dict_dir = 'dict'
    language_dict_files = {'en': 'en.list', 'sv': 'sv.list'}


    def __init__(self, uid, language = 'en', debug = False):
        self.learning_data = {}
        self.learning_history = {}
        self.words = None
        self.active = False
        self.language = language
        self.debug = debug
        self.simplelog("iMemory object created.")

        # Load module data according configuration
        if(not self.load_module_data(language)):
            self.simplelog("Load module data failure!")
            self.active = False
            return

        # Load user data
        if(not self.init_user_data(uid)):
            self.simplelog("Load user data failure!")
            self.active = False
            return
        self.active = True

    def __str__(self):
        return(self.desc + '\nVersion ' + self.version)

    def simplelog(self, text):
        if(self.debug):
            print(text)

    def load_module_data(self, language):
        """
        """
        if not (language in self.language_dict_files):
            self.simplelog("language dict configuration miss!")
            return False

        language_dict_file = os.path.join(DATA_PATH, self.language_dict_dir,
                self.language_dict_files[language])

        with open(language_dict_file, 'r') as dict_fd:
            # Read word list to a tuple 
            self.words = tuple(dict_fd.read().split('\n'))
            # Generate index for words
            self.words_index = dict(zip(self.words,range(len(self.words))))
            return True

    def init_user_data(self, uid):
        index_file = os.path.join(DATA_PATH, UID_2_INDEX_FILE)
        index_data = {}
        with open(index_file, 'r') as index_fd:
            try:
                index_data = json.load(index_fd)
            except:
                self.simplelog('Index file load failure!')
                index_data = {}
                index_data['index'] = 1

        # If find index by uid then initiate data by this index 
        if(uid in index_data):
            index = index_data[uid]
            ret = self.get_user_data(uid, index)
        else:    # Otherwise generate a new index by the uid
            index = index_data['index']
            # Generate a (uid, index) pair and add it to index data
            index_data[uid] = index_data['index'] 

            # Add a new learing data by uid and index, if successfully update
            # index data.
            ret = self.add_user_data(uid, index)
            if(ret):
                # Valid index add 1
                index_data['index'] += 1
                self.write_index_data(index_data)

        # If load user data successfully 
        if(ret):
            self.simplelog('load user learning data successfully.')
        else:
            self.simplelog('load user learning data failure!')
        return ret

    def write_index_data(self, index_data):
        """
        Save uid to index data to data file
        For internal use only.
        """
        index_file = os.path.join(DATA_PATH, UID_2_INDEX_FILE)
        with open(index_file, 'w+') as fd:
            try:
                json.dump(index_data, fd)
                self.simplelog('Index data saved.')
            except:
                self.simplelog('Index data is failure in saving!')

    def add_user_data(self, uid, dataindex):
        """
        Add a new user data file and initiate it
        For internal use only.
        """
        user_data_path = os.path.join(DATA_PATH, str(dataindex))
        user_data_file = os.path.join(user_data_path, str(dataindex))
        # If no user data dir then create it
        if os.path.isdir(user_data_path):
            self.simplelog('User data dir exists.')
        else:
            os.mkdir(user_data_path)

        # If there is index data file then add user data failure 
        if os.path.isfile(user_data_file):
            self.simplelog('User data file exists. add user data failure!')
            return False
        else:
            self.learning_data['uid'] = uid
            self.learning_data['dataindex'] = str(dataindex)
            self.learning_data['description'] = ''
            self.learning_data['new_word_index'] = 0
            self.learning_data['last_learned_word'] = ''
            self.learning_data['studying_words'] = []
            self.learning_data['mastered_words'] = []
            # All learned word statistics
            self.learning_data['learned_words'] = {}

            with open(user_data_file, 'w+') as fd:
                try:
                    json.dump(self.learning_data, fd)
                    self.simplelog('new user data saved.')
                    return True
                except:
                    self.simplelog('new user data is failure in saving!')
                    return False

    def get_user_data(self, uid, dataindex):
        """
        Get a new user data fro a user data file
        For internal use only.
        """
        user_data_path = os.path.join(DATA_PATH, str(dataindex))
        user_data_file = os.path.join(user_data_path, str(dataindex))
        # If no user data dir or user data file then then return false 
        if (not os.path.isdir(user_data_path) or
            not os.path.isfile(user_data_file)):
            self.simplelog('User data dir or file does not exist.')
            return False

        # If there is index data file then add user data failure 
        with open(user_data_file, 'r') as fd:
            try:
                self.learning_data = json.load(fd)
                self.simplelog('User data loaded successfully.')
                return True
            except:
                self.simplelog('User data loaded failure!')
                return False

    def save_data(self, datatype):
        dataindex = self.learning_data['dataindex']
        user_data_path = os.path.join(DATA_PATH, str(dataindex))
        user_data_file = os.path.join(user_data_path, str(dataindex))
        if datatype == 'LEARNING_DATA' or datatype == 'USER_DATA':
            with open(user_data_file, 'w+') as fd:
                try:
                    json.dump(self.learning_data, fd)
                    self.simplelog('User data saved.')
                    return True
                except:
                    self.simplelog('User data is failure in saving!')
                    return False
        return False

    # Interfaces 
    def reset_word(self, text, dataindex):
        return 0

    def set_user_desc(self, uid, desc):
        return 0

    def get_user_learning_history(self, uid, dataindex):
        return 0


    def get_next_new_word(self):
        """
        Require a new word for learning.
        """
        # No learned word index, return empty record 
        if 'new_word_index' not in self.learning_data:
            self.simplelog('No valid new word index!')
            return ('', -1)

        index = self.learning_data['new_word_index']
        word_text = self.words[index]

        # TODO: index may exceed the taximun words
        return (word_text, index)

    def learn_word(self, word, learned_time, answer):
        """
        Notify that the user has learned a word, requires update learning data
        of the user and relavent history data.
        """
        self.learning_data['last_learned_word'] = word
        # If it is a new word move new_word_index to next
        if( (self.words_index[word]) == self.learning_data['new_word_index']):
            self.learning_data['new_word_index'] += 1
        learned_words = self.learning_data['learned_words']
        learned_word = None

        # Add a new learned word item
        if word not in learned_words:
            learned_words[word] = {}
            learned_words[word]['ref_index'] = -1
            learned_words[word]['learn_history'] = ''
            learned_words[word]['ref_index'] = -1
            learned_words[word]['mastered_score'] = 0      # 0 - 100
            learned_words[word]['familiar_score'] = 1000   # 0 - 1000
            learned_words[word]['total_learned_time'] = 0  # seconds 
        learned_word = learned_words[word]
        history = learned_word['learn_history']
        learned_word['learn_history'] = self.generate_learn_history(history, answer)
        learned_word['mastered_score'] = self.count_mastered_score(word)
        learned_word['total_learned_time'] += learned_time
        # Save learning_data to data file
        self.save_data('LEARNING_DATA')

    def generate_learn_history(self, s, answer):
        new_flag = '0'      # represent False
        if answer:
            new_flag = '1'
        s += new_flag
        # Only stored last 20 records
        return s[-20:]

    def count_mastered_score(self, word):
        learned_words = self.learning_data['learned_words']
        learned_word_history = learned_words[word]['learn_history']
        length = len(learned_word_history)
        len_config = len(MASTERED_SCORE_COUNT_CONFIG)
        score = 0
        for i in range(0, length):
            index = length - i - 1
            value = learned_word_history[i]
            if value == '1':
                score += MASTERED_SCORE_COUNT_CONFIG[len_config -i - 1]
        return score

    def delete_word(self, word_text):
        """
        Completely delete a word in word list. Can't delete one word which has
        a history record
        """
        return 0
