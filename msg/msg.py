import math
import re


class Message_Splitter:

    def __init__(self, text, max_length):
        self.text = text
        self.max_length = max_length

    def format_msg(self):
        text_chars = len(self.text)
        msg_count = math.ceil(text_chars / self.max_length)
        msg_count_with_tail = math.ceil(
            (msg_count * 6 + text_chars) / self.max_length)
        tail = 6 + 2 * (len(str(msg_count_with_tail)) - 1)
        optimal_length = self.max_length - tail

        good_text = []
        text_cleaned = self.text.split(" ")

        msg_fitted = ""

        def add_text(max_len=self.max_length):
            striped_text = msg_fitted.strip()
            if striped_text != "":
                good_text.append(striped_text)
            else:
                pass

        def add_message(message):
            msg_fitted + message.strip()

        for word in text_cleaned:
            if len(f'{msg_fitted} {word}') <= optimal_length:
                msg_fitted = f'{msg_fitted} {word}'
                add_message(msg_fitted)
            elif len(f'{msg_fitted} {word}') > optimal_length:
                add_text()
                msg_fitted = word

        if msg_fitted:
            add_message(msg_fitted)
            add_text()

        def add_tail(text_list: list, max_length, length=None) -> list:
            def chck_max_msg(final_text):
                length = len(final_text)
                pattern = re.compile(r'(\d+)(?!.*\d)')
                res = pattern.search(final_text[0])
                result = res.group()
                if len(final_text) != int(result):
                    new_list = []
                    for item in final_text:
                        x = re.sub('(\d+)(?!.*\d)', str(length), item)
                        new_list.append(x)
                    return new_list
                return final_text

            final_text = []
            if length == None:
                length = len(text_list)
            n = 1
            for item in text_list:
                index_item = text_list.index(item)

                final_text.append(f"{item} ({n}/{length})")
                n = n + 1

                if len(final_text[-1]) <= max_length:
                    if index_item + 1 <= text_list.index(text_list[-1]):
                        # try to add next element and check if does it fit

                        if len(
                                f'{final_text[-1]} {text_list[index_item + 1]}') <= max_length:
                            split_msg = final_text[-1].split()
                            split_msg.insert(-1, text_list[index_item + 1])
                            final_text[-1] = " ".join(
                                split_msg)  # insert additional word into final_text list
                            text_list[index_item + 1] = text_list[
                                index_item + 1].replace(
                                text_list[index_item + 1],
                                "").strip()  # delete inserted word from text_list

                            if text_list[
                                index_item + 1] == "":  # if text_list item is empty after deleting - item popped
                                text_list.pop(index_item + 1)

                            # if next word from next message fits - fixing text_list
                            string_parts = final_text[-1].split()
                            result = string_parts[-2]  # before tail

                            if text_list[index_item] == text_list[-1]:
                                text_list.append("")

                            text_list[
                                index_item + 1] = f'{result} {text_list[index_item + 1]}'.strip()  # insert into text_list additional word before tail
                            text_list[index_item] = text_list[
                                index_item].replace(result, "").strip()
                            final_text[-1] = final_text[-1].replace(result,
                                                                    "").replace(
                                "  ", " ")

                elif len(final_text[-1]) > max_length:
                    # doesn't fit one long word
                    words_list = final_text[-1].split()

                    tail_len = len(words_list[-1])
                    cut_word_edge = max_length - tail_len - 1

                    splitted_word = text_list[index_item][:cut_word_edge]

                    final_text[-1] = " ".join([splitted_word, words_list[-1]])

                    try:
                        text_list[
                            index_item + 1] = f'{text_list[index_item][len(splitted_word):]} {text_list[index_item + 1]}'.strip()  # insert into text_list additional word
                    except IndexError:
                        text_list.append(
                            f'{text_list[index_item][len(splitted_word):]}')  # insert into text_list additional word
                    text_list[index_item] = splitted_word

            return chck_max_msg(final_text)

        return add_tail(good_text, max_length=self.max_length)


if __name__ == '__main__':
    print(Message_Splitter(
        "Splits long message to multiple messages in order to fit within an arbitrary message length limit (useful for SMS, Twitter, etc.).",
        25).format_msg())
