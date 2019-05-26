import os
import json

# data dir, can be extend for configurable
MODULE_PATH = os.path.dirname(__file__)
DICT_PATH = os.path.join(MODULE_PATH, 'dict')

class Translator(object):
    """
    Translator is a class which can translator a word or text to another 
    language.
    """
    version = '1.0.0'
    desc = 'Tranlsator library.  translator a word or text to another language'

    # Configuration
    # Each dict name is 'lan1-lan2.dict'
    language_dict_files = {'sv': {'en': 'sv-en.dict'}}

    def __init__(self, src_language = 'en', dest_language = 'cn',
                 debug = False):
        self.src_language = src_language
        self.dest_language = dest_language
        self.dict = {}
        self.active = False
        self.debug = debug
        self.simplelog("Translator object created.")

        # Load module data according configuration
        if(not self.load_module_data()):
            self.simplelog("Load module data failure!")
            self.active = False
            return

        self.active = True 

    def __str__(self):
        return(self.desc + '\nVersion ' + self.version)

    def simplelog(self, text):
        if(self.debug):
            print(text)

    def load_module_data(self):
        """
        """
        src = self.src_language
        dest = self.dest_language
        if not (src in self.language_dict_files):
            self.simplelog("language dict configuration miss!")
            return False

        if not (dest in self.language_dict_files[src]):
            self.simplelog("language dict configuration miss!")
            return False

        dict_file = os.path.join(DICT_PATH,
                                 self.language_dict_files[src][dest])

        with open(dict_file, 'r') as dict_fd:
            # Read (src, dest) list to a tuple 
            content = dict_fd.read().split('\n')
            for item in content:
                word = item.split(',')
                # Transfer the dict item to (key, value) pair 
                if len(word) > 1:
                    self.dict[word[0]] = word[1].strip()

            return True
        return False

    # -- Interfaces -- 
    def query(self, word):
        if word not in self.dict:
            return('')
        else:
            return self.dict[word]
















