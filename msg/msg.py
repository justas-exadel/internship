import math
import re

def clean_string(text_list: list) -> list:
    final_text = []
    length = len(text_list)
    n = 1
    for item in text_list:
        final_text.append(f"{item}({n}/{length})")
        n = n + 1
    return final_text

def fitted_text(text: str, max_length=30) -> list:
    text_chars = len(text)
    add_space = math.ceil((text_chars/max_length*5+text_chars)/max_length)
    tail = 5 + 2 * (len(str(add_space))-1)
    optimal_length = max_length - tail - 5
    start = 0
    end = 0
    clean_strings = []
    bad_words = []
    for i in range(0, len(text), optimal_length):
        fixing_text = []
        end += optimal_length
        string = text[start:end]
        fixing_text.append(string)
        start += optimal_length
        clean_text = re.compile(r'.+\s')

        try:
            if bad_words:
                full_word = bad_words[0] + fixing_text[0]
                fixing_text[0] = full_word
                bad_words = []
            res = clean_text.search(fixing_text[0])
            result = res.group()

            if result[-1] == " ":
                result = result[:-1]
                clean = f"{result} "

            clean_strings.append(clean)
            muted_text = fixing_text[0].replace(clean, "")
            fixing_text[0] = muted_text
            bad_words.append(fixing_text[0])

        except AttributeError:
            clean_strings.append(fixing_text[0])

    if bad_words:
        clean_strings.append(f'{bad_words[0]} ')
    if len(clean_strings[-1]) + len(clean_strings[-2]) <= optimal_length:
        clean_strings[-2] = clean_strings[-2] + clean_strings[-1]
        clean_strings.pop()
    text_fixed = clean_string(clean_strings)
    return text_fixed


if __name__ == '__main__':

    print(fitted_text('Splits long message to multiple messages in order to fit within an arbitrary message length limit (useful for SMS, Twitter, etc.).', 22))


