import os
import json

# data dir, can be extend for configurable
DATA_PATH = './data'
UID_2_INDEX_FILE = 'uid2index.json'
WORD_2_INDEX_FILE = 'word2index.json'
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
        self.words = []
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
        if not (language in language_dict_files):
            self.simplelog("language dict configuration miss!")
            return False

        language_dict_file = os.path.join(DATA_PATH, 
                self.language_dict_files[language])

        with open(index_file, 'r') as index_fd:
            # Read word list to a tuple 

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

    # Interfaces 
    def reset_word(self, text, dataindex):
        return 0

    def set_user_desc(self, uid, desc):
        return 0

    def get_user_learning_history(self, uid, dataindex):
        return 0
