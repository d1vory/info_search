from lab_04.permutation_index import WordToken


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
    def get_representation(self) -> set:
        if self.representation is None:
            index = self.data.get_index_of_word(self.word)
            self.representation = self.data.inverted_index[index]
        return self.representation

    def __and__(self, other):
        a = self.get_representation()
        b = other.get_representation()
        kek = f'{self.word} and {other.word}'
        res = a.intersection(b)
        return self.__class__(kek, self.data, representation=res)

    def __or__(self, other):
        a = self.get_representation()
        b = other.get_representation()
        kek = f'{self.word} or {other.word}'
        res = a.union(b)
        return self.__class__(kek, self.data, representation=res)

    def __invert__(self):
        a = self.get_representation()
        kek = f'not_{self.word[::-1]}'
        res = {document_id for document_id in self.data.document_ids.values() if document_id not in a}
        return self.__class__(kek, self.data, representation=res)


class DictInvertedIndexQueryToken(InvertedIndexQueryToken):
    def get_representation(self) -> set:
        if self.representation is None:
            self.representation = self.data.inverted_index.get(self.word, set())
        return self.representation


class PermutationIndexQueryToken(InvertedIndexQueryToken):
    def get_representation(self) -> set:
        if self.representation is None:
            word = WordToken.transform_joker(self.word)
            self.representation = set()
            try:
                for _, word_token in self.data.inverted_index.iteritems(word):
                    print('found word: ', word_token.word)
                    self.representation = self.representation.union(word_token.occurrences)
            except KeyError:
                pass
        return self.representation
