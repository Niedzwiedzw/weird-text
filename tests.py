from unittest import TestCase
from unittest import main as run_tests

from weird_text import WeirdText

BASE_TEST = ('This is a long looong test sentence,\n'
             'with some big (biiiiig) words!')


class TestTest(TestCase):
    def test_tests(self):
        self.assertEqual(True, True)


class TestBasicInput(TestCase):
    def assertWeirdTexted(self, normal, encoded):
        self.assertEqual((normal[0], normal[-1]), (encoded[0], encoded[-1]))

    def test_single_word_encoding(self):
        word = 'omnipotence'
        self.assertWeirdTexted(word, WeirdText().encode_word(word))
        
    def test_reading_from_encoded_text(self):
        input_text = 'some text'
        encoded = f'''{WeirdText._encoding_boundary}{input_text}{WeirdText._encoding_boundary}'''
        self.assertEqual(input_text, WeirdText._get_text(encoded)[0])

    def test_decoding(self):
        self.assertEqual(WeirdText.decode_text(WeirdText.encode_text(BASE_TEST)), BASE_TEST)

    def test_encoding(self):
        encoded_text = WeirdText.encode_text(BASE_TEST)

        self.assertNotEqual(BASE_TEST, WeirdText.encode_text(BASE_TEST))
        for normal, encoded in zip(BASE_TEST.split(' '), WeirdText._get_text(encoded_text)[0].split(' ')):
            self.assertWeirdTexted(normal, encoded)

    def test_exception_for_improperly_formated(self):
        from weird_text import WeirdTextDecodingException

        text = f'---not weird---\n{BASE_TEST}\n---not weird---\nsome random words'
        with self.assertRaises(WeirdTextDecodingException):
            WeirdText.decode_text(text)


if __name__ == '__main__':
    run_tests()
