import os
import json

# data dir, can be extend for configurable
g_data_path = './data'
g_uid2index_file = 'uid2index.json'
g_word2index_file = 'word2index.json'
class iMemory:
    """

    """
    mVersion = '1.0.0' 
    mDesc = 'iMemory library. Design for efficient memory for learning languages.'
    mDebug = False
    mLearningData = {}
    mLearningHistory = {}
    mActive = False
    def __init__(self, uid, debug = False):
        self.mDebug = debug
        self.simplelog("iMemory object created.")

        # Load data failure
        if(not self.load_data(uid)):
            self.simplelog("Load user data failure!")
            mActive = False
        mActive = True

    def __str__(self):
        return(self.mDesc + '\nVersion ' + self.mVersion)

    def simplelog(self, text):
        if(self.mDebug):
            print(text)

    def load_data(self, uid):
        index_file = os.path.join(g_data_path, g_uid2index_file)
        index_data = {}
        with open(index_file, 'r') as index_fd:
            try:
                index_data = json.load(index_fd)
                print(index_data)
            except:
                self.simplelog('Index file load failure!')
                index_data = {}
                index_data['index'] = 1

        # If find index by uid then initiate data by this index 
        if(uid in index_data):
            index = index_data[uid]
            mLearningData = self.get_user_data(uid, index)
        else:    # Otherwise generate a new index by the uid
            index = index_data['index']
            index_data['index'] += 1
            # Generate a (uid, index) pair and add it to index data
            index_data[uid] = index_data['index'] 
            
            # Add a new learing data by uid and index
            mLearningData = self.add_user_data(uid, index)

        # Update index if load user data successfully 
        if(mLearningData != {}):
            self.write_index_data(index_data)
        else:
            self.simplelog('load user learning data failure!')
            return False
        return True

    def write_index_data(self, index_data):
        """
        Save uid to index data to data file
        For internal use only. 
        """
        index_file = os.path.join(g_data_path, g_uid2index_file)
        with open(index_file, 'w+') as fd:
            try:
                json.dump(index_data, fd)
                self.simplelog('Index data saved.')
            except:
                self.simplelog('Index data is failure in saving!')

    def add_user_data(self, uid, dataindex):
        user_data_path = os.path.join(g_data_path, str(dataindex))
        user_data_file = os.path.join(user_data_path, str(dataindex)) 
        # If no index dir then create it
        if os.path.isdir(user_data_path):
            self.simplelog('User data dir exists.')
        else:
            os.mkdir(user_data_path)
        
        # If there is index data file then add user data failure 
        if os.path.isfile(user_data_file):
            self.simplelog('User data file exists. add user data failure!')
            return False
        else
            self.mLearningData['uid'] = uid
            self.mLearningData['dataindex'] = str(dataindex)

            with open(user_data_file, 'w+') as fd:
            try:
                json.dump(self.mLearningData, fd)
                self.simplelog('new user data saved.')
                return True 
            except:
                self.simplelog('new user data is failure in saving!')
                return False 

    def get_user_data(self, uid, dataindex):
        return 0

    # Interfaces 
    def reset_word(self, text, dataindex):
        return 0

    def set_user_desc(self, uid, desc):
        return 0

    def get_user_learning_history(self, uid, dataindex):
        return 0
