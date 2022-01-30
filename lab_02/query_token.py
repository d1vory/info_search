from functools import cached_property

from lab_02.dictionary_builder import DictionaryBuilder


class QueryToken:
    and_separ = 'AND'
    or_separ = 'OR'
    not_separ = 'NOT'
    separators = {
        'AND': '__and__',
        'OR': '__or__',
        'NOT': '__invert__'
    }

    def __init__(self, word, data, representation=None):
        self.word = word
        self.data = data
        self.representation = representation

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
        return QueryToken(f'{self.word} {other.word}', self.data)

    def __or__(self, other):
        kek = f'{self.word} or {other.word}'
        print(kek)
        return QueryToken(kek, self.data)

    def __and__(self, other):
        kek = f'{self.word} and {other.word}'
        print(kek)
        return QueryToken(kek, self.data)

    def __invert__(self):
        kek = f'not_{self.word[::-1]}'
        return QueryToken(kek, self.data)

class IncedenceMatrixQueryToken(QueryToken):

    def get_representation(self):
        if self.representation is None:
            index = self.data.get_index_of_word(self.word)
            self.representation = self.data.incidence_matrix[index]
        return self.representation

    def __and__(self, other):
        a = self.get_representation()
        b = other.get_representation()
        kek = f'{self.word} and {other.word}'
        res = a & b
        return IncedenceMatrixQueryToken(kek, self.data, representation=res)

    def __or__(self, other):
        a = self.get_representation()
        b = other.get_representation()
        kek = f'{self.word} or {other.word}'
        res = a | b
        return IncedenceMatrixQueryToken(kek, self.data, representation=res)

    def __invert__(self):
        kek = f'not_{self.word[::-1]}'
        res = ~self.get_representation() + 2
        return IncedenceMatrixQueryToken(kek, self.data, representation=res)

class InvertedIndexQueryToken(QueryToken):
    pass