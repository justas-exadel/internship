import math
import re

def clean_string(text_list):
    final_text = []
    length = len(text_list)
    n = 1
    for item in text_list:
        final_text.append(f"{item}({n}/{length})")
        n = n + 1
    return final_text

def fitted_text(text, max_length=30):
    text_chars = len(text)
    add_space = math.ceil((text_chars/max_length*5+text_chars)/max_length)
    tail = 5 + 2 * (len(str(add_space))-1)
    a = 0
    c = 0
    best_string = []
    bad_words = []
    optiman_length = max_length - tail - 5
    for i in range(0, len(text), optiman_length):
        fixing_text = []
        c += optiman_length
        d = text[a:c]
        fixing_text.append(d)
        a += optiman_length
        clean_text = re.compile(r'.+\s')
        try:
            if bad_words:
                full_word = bad_words[0] + fixing_text[0]
                fixing_text[0] = full_word
                bad_words = []
            res = clean_text.search(fixing_text[0])
            f = res.group()
            g = f"{f}"
            best_string.append(g)
            y = fixing_text[0].replace(g, "")
            fixing_text[0] = y
            bad_words.append(fixing_text[0])
        except AttributeError:
            best_string.append(fixing_text[0])

    if bad_words:
        best_string.append(f'{bad_words[0]} ')
    if len(best_string[-1]) + len(best_string[-2]) <= optiman_length:
        best_string[-2] = best_string[-2] + best_string[-1]
        best_string.pop()
    text_fixed = clean_string(best_string)
    return text_fixed


if __name__ == '__main__':
    print(fitted_text('Planet’s SkySats deployedsequentiallyabout 12 and a half minutes after liftoff, and the Starlink satellites deployed approximately 46 minutes after liftoff.', 35))



