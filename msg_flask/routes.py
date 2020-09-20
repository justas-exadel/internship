from flask import Flask, render_template
import math
import re
import textwrap
from forms import Message_Form
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(33)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/split_message", methods=['GET', 'POST'])
def message_text():
    form = Message_Form()
    if form.validate_on_submit():
        text_data = form.text.data
        length_data = form.max_length.data
        splitted_msg = Message_Splitter(text_data, length_data).format()
        return render_template("msg_splitted.html", form=False,
                               data=splitted_msg)
    return render_template("index.html", form=form)


class Message_Splitter:
    MIN_TAIL_LENGTH = 6
    text_msg = []
    msg = ""

    def __init__(self, text: str, max_length: int):
        self.text = text
        self.max_length = max_length
        self.optimal_length = self.optimal_msg_length()

    def check_max_len(self):
        if self.max_length < 11:
            print(
                "Maximum length cannot be lower than 11.")
            exit()

    def optimal_msg_length(self) -> int:
        text_chars = len(self.text)
        msg_count = math.ceil(text_chars / self.max_length)
        msg_count_with_tail = math.ceil(
            (msg_count * self.MIN_TAIL_LENGTH + text_chars) / self.max_length)
        tail = self.MIN_TAIL_LENGTH + 2 * (len(str(msg_count_with_tail)))
        optimal_len = self.max_length - tail
        return optimal_len

    def split_long_word(self, word: str) -> list:
        sep_word = textwrap.wrap(word, width=self.optimal_length)
        sep_word_list = [x for x in sep_word]
        return sep_word_list

    def add_word(self, word: str):
        if len(self.msg) + len(word) + 1 <= self.optimal_length:
            self.msg += f"{word} "
        else:
            self.add_msg()
            self.msg += f"{word} "

    def add_msg(self):
        if len(self.msg) < 2:
            pass
        else:
            self.text_msg.append(self.msg)
            self.msg = ""

    def valid_word(self, word: str) -> bool:
        if len(word) > self.optimal_length:
            words = self.split_long_word(word)
            for w in words:
                self.add_word(w)
            return False
        else:
            return True

    def add_tail(self, text_msg: list) -> list:
        length = len(text_msg)
        final_text = []
        n = 1
        for item in text_msg:
            text_with_tail = f"{item.strip()} ({n}/{length})"
            final_text.append(text_with_tail)
            n = n + 1
        return final_text

    def format(self):
        self.check_max_len()
        splitted_msg = self.text.split()
        for item in splitted_msg:
            valid = self.valid_word(item)
            if valid is True:
                self.add_word(item)
        if len(self.msg) > 0:
            self.add_msg()
        msg_with_tail = self.add_tail(self.text_msg)
        check_result = self.valid_msg_length(msg_with_tail)
        return check_result

    def valid_msg_length(self, msg_text: list) -> list:
        for msg in msg_text:
            msg_index = msg_text.index(msg)
            next_item = msg_index + 1
            try:
                next_word = msg_text[next_item].split()
                if len(msg + " " + next_word[0]) <= self.max_length:
                    self.format_final_msg(msg_text, msg_index)
            except IndexError:
                pass
        new_text_list = self.format_tail(msg_text)
        msg_with_tail = self.add_tail(new_text_list)
        return msg_with_tail

    def check_regex(self, word: str) -> bool:
        find_word = re.search(re.escape(word), self.text)
        if find_word is None:
            return False
        else:
            return True

    def format_final_msg(self, msg_text: list, msg_index: int) -> list:
        next_msg = msg_text[msg_index + 1].split()
        next_element = next_msg[0]
        current_msg = msg_text[msg_index].split()
        current_msg.insert(-1, next_element)
        check_word = self.check_regex(current_msg[-3] + (current_msg[-2]))
        if check_word is True:
            current_msg[-2] = current_msg[-3] + current_msg[-2]
            del current_msg[-3]
        msg_text[msg_index] = " ".join(current_msg)
        del next_msg[0]
        if len(next_msg) == 1:
            del msg_text[msg_index + 1]
        else:
            msg_text[msg_index + 1] = " ".join(next_msg)
        self.valid_msg_length(msg_text)
        return msg_text

    def format_tail(self, msg_list: list) -> list:
        new_msg_list = []
        pattern = re.compile(r'\s\W\d+/\d+\W')
        for item in msg_list:
            res = re.sub(pattern, "", item)
            new_msg_list.append(res)
        return new_msg_list


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
