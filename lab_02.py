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

        self.combined_dictionary = OrderedSet(functools.reduce(set.union, self.document_words.values()))

        self.filenames_count = len(self.filenames)
        self.words_count = len(self.combined_dictionary)
        self.incidence_matrix = np.zeros(shape=(self.words_count, self.filenames_count), dtype=np.int8)
        self.inverted_index = None

    def build_incidence_matrix(self):
        for i in tqdm(range(self.words_count)):
            word = self.combined_dictionary[i]
            for j in range(self.filenames_count):
                if word in self.document_words[self.filenames[j]]:
                    self.incidence_matrix[i][j] = 1
        return self.incidence_matrix

    def build_inverted_index(self):
        pass
