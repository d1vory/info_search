import pygtrie
from tqdm import tqdm

from lab_02.dictionary_builder import DictionaryBuilder


class WordToken:
    def __init__(self, word, occurrences):
        self.word = word
        self.occurrences = occurrences

    @staticmethod
    def build_permutations(word, include_dollar=True):
        if include_dollar:
            word = word + "$"
        permutations = [word]
        for i in range(0, len(word)):
            gram = word[i:] + word[:i]
            permutations.append(gram)
        return permutations

    @classmethod
    def transform_joker(cls, word):
        word = word + "$"
        if '*' not in word:
            return word
        permutations = cls.build_permutations(word, include_dollar=False)
        for perm in permutations:
            if perm.endswith('*'):
                return perm[:-1]
        return word


class PermutationIndex(DictionaryBuilder):

    def __init__(self, files_dir='files'):
        self.document_words = dict()
        self.filenames = []
        self.combined_dictionary = {}
        self.filenames_count = 0
        self.words_count = 0
        self.create_combined_dictionary(files_dir)

        self.inverted_index = pygtrie.Trie()
        self.document_ids = dict(zip(self.filenames, range(self.filenames_count)))

        self.build_inverted_index()

    def build_inverted_index(self):
        for word in tqdm(self.combined_dictionary):
            occurences = {self.document_ids.get(filename) for filename in self.filenames if
                          word in self.document_words[filename]}
            for permutation in WordToken.build_permutations(word):
                self.inverted_index[permutation] = WordToken(word, occurences)

    def boolean_search_inverted_index(self, query):
        from lab_02.query_token import PermutationIndexQueryToken
        res = self.boolean_search(query, PermutationIndexQueryToken)
        return [self.filenames[i] for i in res]
