def read_phrases():
    with open('phrases.txt', encoding='utf-8') as file:
        phrases_array = file.readlines()
    return phrases_array