from __future__ import print_function
from six.moves import input

import string
import sys

from langdetect import detect_langs


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
            return dectext
    print('Tried all shifts from -25 to 25 but failed to decrypt text! Here are the attempts:')
    count = 0
    for a in attempts:
        count += 1
        print('Attempt {}: {}'.format(count, a))
    sys.exit(3)


def check_if_text_is_encrypted(text):
    confidence_threshold = 0.95

    guesses = detect_langs(text)
    probabilities = {}
    for g in guesses:
        probabilities[g.prob] = g.lang

    confident_guess = None
    confidence_of_top_guess = max(probabilities.keys())
    if confidence_of_top_guess > confidence_threshold:
        confident_guess = probabilities[confidence_of_top_guess]

    if confident_guess:
        if confident_guess != 'en':
            return True  # yep still encrypted
        else:
            return False  # it has been decrypted
    else:
        return True  # no guess was confident enough, assume it's still encrypted


def main(argv):
    args = argv[1:]
    if len(args) != 1:
        print('Wrong number of arguments: {} instead of 1. Usage: python brute.py "The text you want to decrypt"'.format(len(args)))
        sys.exit(1)

    from langdetect import DetectorFactory
    DetectorFactory.seed = 0

    if not check_if_text_is_encrypted(args[0]):
        print('Warning: your text appears to already be decrypted. This program thinks it\'s regular English already.')
        c = input('Do you wish to continue? [y or Y for yes, any other text for No, assuming yes]:')
        if c and c != 'y' and c != 'Y':
            print('OK, you have chosen not to continue. Exiting.')
            sys.exit(2)

    print(decrypt_encrypted_text(args[0]))


if __name__ == "__main__":
    main(sys.argv)
