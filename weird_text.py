import re
from typing import Match
from random import shuffle
from collections import Counter


def same(word_1: str, word_2: str) -> bool:
    """
    a simple helper function for checking if words match
    :param word_1: a word
    :param word_2: a word
    :return: boolean, do words consist of exactly same letters?
    """
    return Counter(list(word_1)) == Counter(list(word_2))


class WeirdTextDecodingException(Exception):
    """
    raised when trying to decode improperly formatted text
    """
    pass


class WeirdText:
    _encoding_boundary = '\n---weird---\n'

    def __init__(self):
        self.encoded_words = []

    @classmethod
    def encode_text(cls, text: str) -> str:
        """
        main encoding function
        :param text: the thing you want to encode
        :return: the same thing, but encoded
        """
        encoder = cls()
        words = text.split(' ')
        for i, word in enumerate(words):
            words[i] = encoder.encode_word(word)
        return f"{cls._encoding_boundary}" \
               f"{' '.join(words)}" \
               f"{cls._encoding_boundary}" \
               f"{' '.join(sorted(encoder.encoded_words))}"

    @classmethod
    def _get_text(cls, encoded_text: str) -> (str, str):
        """
        a helper function for getting the encoded text out of the wrapper
        :param encoded_text: a full string containing a "---weird---" wrapping
        :return: Tuple of (encoded_text, keys)
        """
        boundary = cls._encoding_boundary.replace('\\', '\\\\')
        regex = re.compile(boundary[1:] + r'(.*)' + boundary[:-1] + r'(.*)', re.DOTALL)

        try:
            return regex.search(encoded_text).group(1), regex.search(encoded_text).group(2)
        except AttributeError:
            raise WeirdTextDecodingException('Input is not formatted correctly')

    @classmethod
    def decode_text(cls, text: str) -> str:
        """
        main decoding function
        :param text: a full string containing a "---weird---" wrapping
        :return: decoded text
        """
        decoder = cls()
        encoded, keys = cls._get_text(text)
        decoder.encoded_words = [key.strip() for key in keys.split(' ')]
        words = encoded.split(' ')

        for i, word in enumerate(words):
            words[i] = decoder.decode_word(word)

        return ' '.join(words)

    def decode_word(self, word: str) -> str:
        """
        a helper function, shouldn't be used separately
        :param word: some encoded word, might have non-word characters around it
        :return: proper, decoded word
        """
        return re.sub('\w+', self._deshuffle_inside, word)

    def _deshuffle_inside(self, matchobj: Match[str]) -> str:
        """
        internal helper function, does the main job of decoding a word
        :warning: This one has side effect of removing substituted words from main encryption keychain.
        :param matchobj:
        :return: a proper, decoded word
        """
        word = matchobj.group(0)
        for i, key in enumerate(self.encoded_words):
            if same(key, word):
                self.encoded_words.pop(i)  # here the word is removed from keychain
                return key
        return word

    def encode_word(self, word: str) -> str:
        """
        a helper function, this one CAN be used on it's own.
        :param word: a normal word, can have non-word characters around it
                    e.g. (oops) will be properly translated to (opos)
        :return: encoded word
        """
        return re.sub(r'\w+', self._shuffle_inside, word)

    def _shuffle_inside(self, matchobj: Match[str]) -> str:
        """
        main helper function for encoding.
        :warning: this function has a side effect of putting substituted words
                  into the 'encoded_words' global array.
        :param matchobj: matched word
        :return: WeirdText-compliant, (encoded only if it can be).
        """
        word = matchobj.group(0)
        if len(word) <= 3:
            return word
        inside = list(word[1:-1])
        if len(set(inside)) == 1:
            return word
        while True:
            shuffle(inside)
            shuffled = word[0] + "".join(inside) + word[-1]
            if word != shuffled:
                self.encoded_words.append(word)
                return shuffled
