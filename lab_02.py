import os

import numpy as np
from tqdm import tqdm
import functools
from ordered_set import OrderedSet

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

    def build_incidence_matrix(self):
        for i in tqdm(range(self.words_count)):
            word = self.combined_dictionary[i]
            for j in range(self.filenames_count):
                if word in self.document_words[self.filenames[j]]:
                    self.incidence_matrix[i][j] = 1
        return self.incidence_matrix

    def build_inverted_index(self):
        for word in tqdm(self.combined_dictionary):
            occurences = [self.document_ids.get(filename) for filename in self.filenames if word in self.document_words[filename]]
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

    @classmethod
    def boolean_search_by_incidence_matrix(self, query):
        res = None
        method = None
        negate = False
        for word in query.split(' '):
            token = QueryToken(word)
            if method:
                if negate:
                    token = ~token
                    negate =False
                res = method(token)
                method = None
                continue
            separator = token.get_separator
            if separator:
                if token.is_negate:
                    negate = True
                    continue
                method = getattr(res, separator)
            else:
                if not res:
                    res = token
                else:
                    res = res + token
        return res

class QueryToken:
    and_separ = 'AND'
    or_separ = 'OR'
    not_separ = 'NOT'
    separators = {
        'AND': '__and__',
        'OR': '__or__',
        'NOT': '__invert__'
    }

    def __init__(self, word):
        self.word = word

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word

    @property
    def get_separator(self):
        return self.separators.get(self.word, False)

    @property
    def is_negate(self):
        return self.word == self.not_separ

    def __add__(self, other):
        return QueryToken(f'{self.word} {other.word}')

    def __or__(self, other):
        kek = f'{self.word} or {other.word}'
        print(kek)
        return QueryToken(kek)

    def __and__(self, other):
        kek = f'{self.word} and {other.word}'
        print(kek)
        return QueryToken(kek)

    def __invert__(self):
        kek = f'not {self.word[::-1]}'
        print(kek)
        return QueryToken(kek)



