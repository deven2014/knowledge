
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
        if(not self.load_data()):
            self.simplelog("Load user data failure!")
            mActive = False
            return None

    def __str__(self):
        return(self.mDesc + '\nVersion ' + self.mVersion)

    def simplelog(self, text):
        if(self.mDebug):
            print(text)

    def load_data(self):
        return False

    # Interfaces 
    def add_user_data(self, uid, desc):
        return 0

    def reset_word(self, text, dataindex):
        return 0

    def get_user_data(self, uid, dataindex):
        return 0

    def get_user_learning_history(self, uid, dataindex):
        return 0
