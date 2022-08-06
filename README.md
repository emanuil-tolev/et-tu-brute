# A solution for the PROSA Bornhack 2022 code competition

This solution brute-forces the Caesar cipher, attempting key shifts from -25 to +25 (shifting the entire alphabet back or forward).

It then uses a list of all English words to try to understand when to stop breaking the cipher. It uses fuzzy matching from Python's core libraries in case the decrypted text is mangled (e.g. eas_ instead of easy, p^ramid instead of pyramid). If it fails to decrypt, it prints all 50 attempts at breaking the cipher and stops.

## Requirements

None. It runs on pure Python 2 and 3, no external libraries, dependencies or a Python virtual environment is needed. Python 2 and 3 are installed by default on Mac and Ubuntu/Debian systems and likely on many other Linux flavours.

## To run

```sh
python brute.py "The text you want to decrypt"
```

## Acknowledgements

Despite saying it has no external dependencies, the solution does bundle the [english-words](https://pypi.org/project/english-words/) Python library. This library has no other dependencies itself. It's used for knowing when to stop trying to break the cipher - when have we got some English rather than encrypted gibberish?