import re

from tqdm import tqdm

from lab_02.dictionary_builder import DictionaryBuilder

def relu(x):
    return max(0, x)

class KGramIndex(DictionaryBuilder):
    @staticmethod
    def generate_grams(word, k):
        word = '$' + word + '$'
        for i in range(0, len(word) - k + 1):
            yield word[0 + i:3 + i]

    @staticmethod
    def transform_joker(word):
        #word = '$' + word + '$'
        word = '$' + word + '$'
        i = word.index('*')
        fst = word[relu(i-3):i]
        scnd = word[i + 1:i + 4]
        return f'{fst} AND {scnd}'


        # word = word.lower()
        # word = re.sub("[*]+", "*", word)
        # if len(re.findall("[*]", word)) > 2:
        #     return "Wrong request"
        # word = re.sub("[*]", "AND", word)
        # word = re.findall("[a-z]+|[AND]+", word)
        #return ' '.join(word)

    def __init__(self, files_dir='files', k=3):
        self.k = k
        self.document_words = dict()
        self.filenames = []
        self.combined_dictionary = {}
        self.filenames_count = 0
        self.words_count = 0
        self.create_combined_dictionary(files_dir)

        self.inverted_index = {}
        self.document_ids = dict(zip(self.filenames, range(self.filenames_count)))

        self.build_inverted_index()

    def build_inverted_index(self):
        for word in tqdm(self.combined_dictionary):
            occurences = {self.document_ids.get(filename) for filename in self.filenames if
                          word in self.document_words[filename]}
            for gram in self.generate_grams(word, self.k):
                if gram in self.inverted_index:
                    self.inverted_index[gram] = self.inverted_index[gram].union(occurences)
                else:
                    self.inverted_index[gram] = occurences

    def boolean_search_inverted_index(self, query):
        from lab_02.query_token import DictInvertedIndexQueryToken
        query = ' '.join([self.transform_joker(word) if '*' in word else word for word in query.split()])
        res = self.boolean_search(query, DictInvertedIndexQueryToken)
        return [self.filenames[i] for i in res]
