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


    def boolean_search_by_incidence_matrix(self, query):
        and_separ = 'AND'
        or_separ = 'OR'
        not_separ = 'NOT'
        separators = [and_separ, or_separ, not_separ]
        operators = {
            and_separ
        }
        for word in query.split(' '):
            pass
