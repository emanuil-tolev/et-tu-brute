from __future__ import print_function
from six.moves import input

from difflib import get_close_matches
import string
import sys

from english_words import english_words_lower_alpha_set

# See check_is_encrypted function below for explanation of these constants
WORD_SIMILARITY_CUTOFF = 0.7
SENTENCE_IS_ENGLISH_CONFIDENCE_CUTOFF = 0.9


def caesar_crack_attempt(offset, enctext):
    dectext = ''
    for char in enctext:
        # only attempt to shift the letter if it's a letter, not a space or punctuation
        if char in string.ascii_letters:
            letter_int = ord(char)
            dectext += chr(letter_int + offset)
        else:
            dectext += char
    return dectext


def decrypt_encrypted_text(enctext):
    attempts = []
    for offset in range(-25, 26):
        dectext = caesar_crack_attempt(offset, enctext)
        attempts.append(dectext)
        if not check_if_text_is_encrypted(dectext):
            print("Decrypted! Here:\n\n")
            print(dectext)
            sys.exit(0)
    print('Tried all shifts from -25 to 25 but failed to decrypt text! Here are the attempts:')
    count = 0
    for a in attempts:
        count += 1
        print('Attempt {}: {}'.format(count, a))
    sys.exit(3)


def check_if_text_is_encrypted(text):
    filtered_text = ''
    # remove everything that's not a letter or a space after lowercasing
    for char in text.lower():
        if char in string.ascii_lowercase + ' ':
            filtered_text += char

    words = filtered_text.split(' ')
    confidence = 0.0
    for word in words:
        # Using Python's standard builtin difflib library to check if a word is an English word.
        # Some encrypted examples are missing letters, like "Wh_ is it eas_ to hack ..."
        # "eas_" isn't a 100% match to "easy", but it is a 75% match. So we set similarity cutoff to 70%.
        # This is arbitrary - the default is 60% for example. We want good enough but accurate for most
        # sentences.
        if get_close_matches(word, english_words_lower_alpha_set, 1, WORD_SIMILARITY_CUTOFF):
            # Confidence based on length e.g. for a single-word sentence, if the word is English, then we have
            # 100% confidence the sentence is English. If one word in a 4-word sentence is English, then we
            # only have 25% confidence the sentence is English. If two words in a 10-word sentence are English,
            # then we have 20% confidence the sentence as a whole is English, and so on.
            confidence += 1.0 / len(words)

    # still considered encrypted unless we're 90+% sure it's English
    return True if confidence < SENTENCE_IS_ENGLISH_CONFIDENCE_CUTOFF else False


def main(argv):
    args = argv[1:]
    if len(args) != 1:
        print('Wrong number of arguments: {} instead of 1. Usage: python brute.py "The text you want to decrypt"'.format(len(args)))
        sys.exit(1)

    if not check_if_text_is_encrypted(args[0]):
        print('Warning: your text appears to already be decrypted. This program thinks it\'s regular English already.')
        c = input('Do you wish to continue? [y or Y for yes, any other text for No, assuming yes]:')
        if c and c != 'y' and c != 'Y':
            print('OK, you have chosen not to continue. Exiting.')
            sys.exit(2)

    decrypt_encrypted_text(args[0])


if __name__ == "__main__":
    main(sys.argv)
