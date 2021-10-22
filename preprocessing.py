import json
from helpers import ALINEA_TAG, PUNC, set_pos_tag


# Opens data file and loads all chapters after each other into one string
def get_chapter_data():
    with open('data/LordOfTheRingsBook.json', 'r', encoding="utf8") as file_object:
        data = json.load(file_object)
        print(data)
        _raw_chapter_text = ALINEA_TAG + ' '
        for chapter in data:
            _raw_chapter_text += chapter['ChapterData']
        return _raw_chapter_text


# Removes punctuation from a given text
def remove_punctuation(text):
    _no_punctuation_text = text
    for ele in PUNC:
        if ele in _no_punctuation_text:
            _no_punctuation_text = _no_punctuation_text.replace(ele, "")
    return _no_punctuation_text


# Adds alinea tag to denote the fenceposts between alineas
def set_alinea_tag(text):
    _alinea_tag_text = text
    print(repr(_alinea_tag_text))
    _alinea_tag_text = _alinea_tag_text.replace("\r\n", ' ' + ALINEA_TAG + ' ')
    return _alinea_tag_text


def write_to_file(text):
    f = open("processed_data/preprocessing.py.txt", "w", encoding='utf8')
    f.write(text)
    f.close()


raw_chapter_text = get_chapter_data()
# no_punctuation_text = remove_punctuation(raw_chapter_text)
alinea_tag_text = set_alinea_tag(raw_chapter_text)
pos_tag_text = set_pos_tag(alinea_tag_text)
write_to_file(pos_tag_text)



