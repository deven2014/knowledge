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
        with open(index_file, 'w+') as index_fd:
            try:
                index_data = json.load(index_fd)
                print(index_data)
            except:
                self.simplelog('Index file load failure!')
                index_data = {}
                index_data['index'] = 1
            index_data['index'] += 1
            json.dump(index_data, index_fd)
        return True

    # Interfaces 
    def add_user_data(self, uid, desc):
        return 0

    def reset_word(self, text, dataindex):
        return 0

    def get_user_data(self, uid, dataindex):
        return 0

    def get_user_learning_history(self, uid, dataindex):
        return 0
