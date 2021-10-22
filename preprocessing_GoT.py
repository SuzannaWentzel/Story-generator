import os
from helpers import ALINEA_TAG, PUNC, set_pos_tag


# Opens data file and loads all chapters after each other into one string
def get_chapter_data():
    temp = ALINEA_TAG + " "
    for file in os.listdir("./data/GoT/Book1/Chapter_copies"):
        with open('./data/GoT/Book1/Chapter_copies/' + file, 'r', encoding="utf8") as file_object:
            temp += file_object.read()
    for file in os.listdir("./data/GoT/Book2/Chapter_copies"):
        with open('./data/GoT/Book2/Chapter_copies/' + file, 'r', encoding="utf8") as file_object:
            temp += file_object.read()
    for file in os.listdir("./data/GoT/Book3/Chapter_copies"):
        with open('./data/GoT/Book3/Chapter_copies/' + file, 'r', encoding="utf8") as file_object:
            temp += file_object.read()
    return temp


# Removes punctuation from a given text
def remove_punctuation(text):
    _no_punctuation_text = text
    for ele in PUNC:
        if ele in _no_punctuation_text:
            _no_punctuation_text = _no_punctuation_text.replace(ele, "")
    return _no_punctuation_text


def write_to_file(text):
    f = open("processed_data/GoT.txt", "w", encoding='utf8')
    f.write(text)
    f.close()


raw_chapter_text = get_chapter_data()
# no_punctuation_text = remove_punctuation(raw_chapter_text)
pos_tag_text = set_pos_tag(raw_chapter_text)
write_to_file(pos_tag_text)
