"""This is exercise 4."""
__author__ = "Jack Shaw"


def obfuscate(text: str) -> str:
    """This will make the inputted text more difficult to read."""
    # Replaces 'the' with 'and', and 'and' with 'the'.
    text = text.replace("the", "TEMP_VALUE")
    text = text.replace("and", "the")
    text = text.replace("TEMP_VALUE", "and")

    # Takes every third letter and makes it uppercase.
    temp_text = ""
    for index, char in enumerate(text):
        if (index + 1) % 3 == 0:
            temp_text += char.upper()
        else:
            temp_text += char
    text = temp_text

    # Reverse every fifth word and then applies a shift cipher with key 1 on every other word.
    word_number = 1
    iteration = 0
    key = 1
    temp_text = ""
    for word in text.split(" "):
        if word_number % 5 == 0:
            word = word[::-1]
        word_number += 1
        if iteration % 2 != 0:
            temp_word = ""
            for letter in word:
                number = ord(letter)
                number += key
                letter = chr(number)
                temp_word += letter
        else:
            temp_word = word
        temp_text += temp_word + " "
        iteration += 1
    text = temp_text[:-1]  # Removes an extra space on the end
    return text
