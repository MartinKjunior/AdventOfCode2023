import os

cwd = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
os.chdir(cwd)

with open('calibrationValues.txt') as f:
    content = f.readlines()

def find_digit(line, first = True):
    if first:
        for i, char in enumerate(line):
            if char.isdigit():
                return i, char
    else:
        for i, char in enumerate(line[::-1]):
            if char.isdigit():
                return len(line) - i - 1, char
    return None, None

def find_word(line, first = True):
    'first: True if first word, False if last word'
    found = []
    for word in list_of_word_nums:
        if first:
            idx = line.find(word)
        else:
            idx = line.rfind(word)
        if idx != -1:
            found.append((idx, word))
    try:
        if first:
            return min(found, key = lambda x: x[0])
        else:
            return max(found, key = lambda x: x[0])
    #if no words in line
    except ValueError:
        return None, None

def get_first_number(line):
    first_digit_index, first_digit = find_digit(line)
    first_word_index, first_word = find_word(line)
    #if one is not found, return the other
    if first_digit_index is None:
        return translate_dict[first_word]
    elif first_word_index is None:
        return first_digit
    #if both are found, return the one that comes first
    if first_digit_index < first_word_index:
        return first_digit
    else:
        return translate_dict[first_word]

def get_last_number(line):
    last_digit_index, last_digit = find_digit(line, first = False)
    last_word_index, last_word = find_word(line, first = False)
    #if one is not found, return the other
    if last_digit_index is None:
        return translate_dict[last_word]
    elif last_word_index is None:
        return last_digit
    #if both are found, return the one that comes first
    if last_digit_index > last_word_index:
        return last_digit
    else:
        return translate_dict[last_word]

list_of_word_nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
translate_dict = {word: str(i) for i, word in enumerate(list_of_word_nums, 1)}

total = 0
for line in content:
    total += int(get_first_number(line) + get_last_number(line))
print(total)