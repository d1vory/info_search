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
                    prepared_words.add(word)
                    #singular_word = inflect_engine.singular_noun(word)
                    #prepared_words.add(singular_word if singular_word else word)
        dictionary.update(prepared_words)
    return dictionary


def save_to_json(filename, dictionary):
    with open(filename, 'w') as file:
        json.dump(list(dictionary), file)


def save_to_plain_text(filename, dictionary):
    with open(filename, 'w') as file:
        file.write(' '.join(dictionary))


def create_words_set(files_dir: str):
    res = set()
    filenames = os.listdir(files_dir)
    for filename in tqdm(filenames):
        filename = f'{files_dir}/{filename}'
        walk_file(filename, res)
    return res


def process_files():
    res = create_words_set('files')
    save_to_json('dict.json', res)
    save_to_plain_text('dict.txt', res)
    return res


#process_files()
