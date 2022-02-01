import functools
import os

import numpy as np
from ordered_set import OrderedSet
from tqdm import tqdm

from lab_01 import walk_file


class DictionaryBuilder:
    def __init__(self):
        self.document_words = dict()
        self.filenames = os.listdir('files')
        for filename in tqdm(self.filenames):
            res = set()
            self.document_words[filename] = walk_file(f'files/{filename}', res)
        print('Dict by document is done!')

        self.combined_dictionary = sorted(OrderedSet(functools.reduce(set.union, self.document_words.values())))

        self.filenames_count = len(self.filenames)
        self.words_count = len(self.combined_dictionary)
        self.incidence_matrix = np.zeros(shape=(self.words_count, self.filenames_count), dtype=np.int8)

        self.inverted_index = []
        self.document_ids = dict(zip(self.filenames, range(self.filenames_count)))

        self.build_incidence_matrix()
        self.build_inverted_index()

    def build_incidence_matrix(self):
        for i in tqdm(range(self.words_count)):
            word = self.combined_dictionary[i]
            for j in range(self.filenames_count):
                if word in self.document_words[self.filenames[j]]:
                    self.incidence_matrix[i][j] = 1
        return self.incidence_matrix

    def build_inverted_index(self):
        for word in tqdm(self.combined_dictionary):
            occurences = {self.document_ids.get(filename) for filename in self.filenames if word in self.document_words[filename]}
            self.inverted_index.append(occurences)


    def get_index_of_word(self, word):
        low = 0
        high = self.words_count
        while low <= high:
            mid = (high + low) // 2
            if self.combined_dictionary[mid] < word:
                low = mid + 1
            elif self.combined_dictionary[mid] > word:
                high = mid - 1
            else:
                return mid
        return -1

    def boolean_search(self, query, token_cls):
        res = None
        method = None
        negate = False
        for word in query.split(' '):
            token = token_cls(word, self)
            separator = token.get_separator
            if separator:
                if token.is_negate:
                    negate = True
                else:
                    method = getattr(res, separator)
                continue
            if method and not token.is_negate:
                if negate:
                    token = ~token
                    negate =False
                res = method(token)
                method = None
                continue
            if not method:
                if negate:
                    token = ~token
                    negate = False
                if not res:
                    res = token
                else:
                    res = res + token
        return res.get_representation()

    def boolean_search_incidence_matrix(self, query):
        from lab_02.query_token import IncedenceMatrixQueryToken
        res = self.boolean_search(query, IncedenceMatrixQueryToken)
        return [self.filenames[i] for i in range(self.filenames_count) if res[i] == 1]

    def boolean_search_inverted_index(self, query):
        from lab_02.query_token import InvertedIndexQueryToken
        return self.boolean_search(query, InvertedIndexQueryToken)
