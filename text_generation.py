import random
import re
from collections import Counter

import numpy as np
from nltk import ngrams, word_tokenize
from os.path import exists
from helpers import set_pos_tag, ALINEA_TAG

UNKNOWN_TAG = 'UNKNOWN'


def get_preprocessed():
    with open('processed_data/lotr.txt', 'r', encoding="utf8") as file_object:
        data = file_object.read()
        return data


def create_vocabulary(words):
    return list(set(words))


def count_words(words, _vocab):
    counter = Counter(words)
    return [(word, counter[word]) for word in _vocab]


def replace_unknown(text, counts):
    # check if unknown was computed before; if so: read from file
    if file_exists('processed_data/unknown/lotr_' + str(INIT['unknown_treshold']) + '.txt'):
        with open('processed_data/unknown/lotr_' + str(INIT['unknown_treshold']) + '.txt', 'r', encoding="utf8") as file_object:
            replaced_unknown_words = file_object.read()
            return replaced_unknown_words
    else:
        possible_unknowns = [count_tuple[0] for count_tuple in counts if count_tuple[1] <= INIT['unknown_treshold']]
        replaced_unknown_words = text
        for word in possible_unknowns:
            regex = r' ' + word + ' '
            replaced_unknown_words = re.sub(regex, ' ' + UNKNOWN_TAG + ' ', replaced_unknown_words)
        write_to_file(replaced_unknown_words, 'processed_data/unknown/lotr_' + str(INIT['unknown_treshold']) + '.txt')
        return replaced_unknown_words


def make_unknown(text, _vocab):
    unknowned_text = text
    words = text.split()
    for word in words:
        if word not in _vocab:
            regex = r' ' + word + ' '
            unknowned_text = re.sub(regex, ' ' + UNKNOWN_TAG + ' ', unknowned_text)
    return unknowned_text


def get_ngrams(text, n):
    _grams = ngrams(text.split(), n)
    word_index = n - 1
    return [(gram[0:word_index], gram[word_index]) for gram in _grams]


def get_last_ngram(text):
    words = text.split()
    split_index = len(words) - INIT['n'] + 1
    return tuple(words[split_index:])


def get_count_grams(_grams):
    counter = Counter(_grams)
    return [(gram, counter[gram]) for gram in _grams]


def write_to_file(text, filename):
    with open(filename, "w", encoding='utf8') as f:
        f.write(text)
        f.close()
        print('Wrote to file!')


def file_exists(filename):
    return exists(filename)


def get_log_probability(word, context, _grams, _gram_dict, _gram_dict_count, _vocab):
    count_with_word = 0
    if context in _gram_dict and word in _gram_dict[context]:
        count_with_word = _gram_dict[context][word]
    count_without_word = 0
    if context in _gram_dict_count:
        count_without_word = _gram_dict_count[context]
    return np.log((count_with_word + 1) / (count_without_word + len(_vocab)))


# Hyper parameters that should be initialized before running
# - unknown threshold is currently not really used
# - n is the amount of n-grams, 3 works well
# - randomness is from how many words a word will be picked, 2 works well
INIT = {
    'unknown_treshold': 1,
    'n': 3,
    'randomness': 2
}


# fetch the preprocessed text in its entirity and as word list
preprocessed_text = get_preprocessed()
preprocessed_word_list = preprocessed_text.split()

# get the vocab from the text
vocab = create_vocabulary(preprocessed_word_list)
print('Len of vocab: ', len(vocab))

# count the occurrence of each word in the vocab and replace unknown words
count_words = count_words(preprocessed_word_list, vocab)
count_words.sort(key=lambda y: y[1])
replaced_unknown = replace_unknown(preprocessed_text, count_words)

# list the n-grams
grams = get_ngrams(preprocessed_text, INIT['n'])

# create dicts of grams with counts
n_grams = {}
n_gram_dict = {}
n_gram_dict_count = {}
print('1')
for i in range(2, INIT['n'] + 1):
    n_grams[i] = get_ngrams(preprocessed_text, i)
    print(i)
    gram_dict = {}
    gram_dict_counts = {}
    for gram in n_grams[i]:
        key = gram[0]
        word = gram[1]

        # If we don't know the combination of context words -> init
        if key not in gram_dict:
            gram_dict[key] = {}
            gram_dict_counts[key] = 0

        # if we didn't have the follow word yet -> init
        if word not in gram_dict[key]:
            gram_dict[key][word] = 0

        gram_dict[key][word] += 1
        gram_dict_counts[key] += 1
    n_gram_dict[i] = gram_dict
    n_gram_dict_count[i] = gram_dict_counts

# ask input
input_sentence = input('Start the sentence: ')

# process input
pos_input = set_pos_tag(input_sentence)
unknowned_input = make_unknown(pos_input, vocab)
generated_text = unknowned_input
last_word = ''

# generate complementary
while last_word != ALINEA_TAG:
    gram_input = get_last_ngram(generated_text)

    # loop through n's to find suitable ngrams
    lower_gram = INIT['n']
    probabilities = []
    words_have_prob = False
    while lower_gram != 1 and not words_have_prob:
        # compute probability for each word in vocab
        probabilities = [(word, get_log_probability(word, gram_input, n_grams[lower_gram], n_gram_dict[lower_gram], n_gram_dict_count[lower_gram], vocab))
                         for word in vocab]
        unknown_prob = get_log_probability(UNKNOWN_TAG, tuple([UNKNOWN_TAG for i in range(0, lower_gram - 1)]), n_grams[lower_gram], n_gram_dict[lower_gram], n_gram_dict_count[lower_gram], vocab)

        # sort probabilities
        probabilities.sort(key=lambda y: y[1])
        split_index = len(probabilities) - INIT['randomness']
        probable_words = probabilities[split_index:]

        # check if all words did not occur in this n gram before
        for word in probable_words:
            if word[1] != unknown_prob:
                words_have_prob = True

        if words_have_prob:
            break
        lower_gram -= 1

    if not words_have_prob:
        # split_index = len(count_words) - INIT['randomness']
        # probable_words = count_words[split_index:]
        probable_words = [(word, 0) for word in random.sample(vocab, INIT['randomness'])]
        # Choosing word from frequently occurring words does not work
        # Choose random word from vocab

    # choose word randomly from x highest words
    random_index = random.randint(0, len(probable_words) - 1)
    last_word = probable_words[random_index][0]
    generated_text += probable_words[random_index][0] + ' '
    print('Generated: ', generated_text)

print('The generated text is: ', generated_text)


