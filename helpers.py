import nltk
from nltk import word_tokenize

ALINEA_TAG = 'ALINEA'
PUNC = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


# Returns if token is punctuation mark
def is_punctuation(token):
    if token in PUNC:
        return True
    return False


# Applies POS tag to words
def set_pos_tag(text):
    _pos_tag_text = ''
    tokens = word_tokenize(text)
    tagged_tokens = nltk.pos_tag(tokens)
    for token in tagged_tokens:
        if is_punctuation(token[0]) or token[0] == ALINEA_TAG:
            _pos_tag_text += token[0] + ' '
        else:
            _pos_tag_text += token[1] + '_' + token[0] + ' '
    return _pos_tag_text