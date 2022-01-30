import json
import os
import re
import inflect
from tqdm import tqdm

inflect_engine = inflect.engine()


def walk_file(filename, dictionary):
    with open(filename, 'r', encoding='utf-8') as file:
        prepared_words = set()
        for line in file:
            for word in re.findall(r"[\W_]*([a-zA-z']+)[\W_]*", line):
                if word:
                    word = word.lower()
                    singular_word = inflect_engine.singular_noun(word)
                    prepared_words.add(singular_word if singular_word else word)
        dictionary.update(prepared_words)
    return dictionary


def save_to_json(filename, dictionary):
    with open(filename, 'w') as file:
        json.dump(list(dictionary), file)


def save_to_plain_text(filename, dictionary):
    with open(filename, 'w') as file:
        file.write(' '.join(dictionary))


def process_files():
    res = set()
    filenames = os.listdir('files')
    for filename in tqdm(filenames):
        filename = f'files/{filename}'
        walk_file(filename, res)
    save_to_json('dict.json', res)
    save_to_plain_text('dict.txt', res)
    return filenames


#process_files()
