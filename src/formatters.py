from impl import AbstractFormatter


def available_character(character: str):
    return 48 <= ord(character) <= 57 or 65 <= ord(character) <= 122


class PlainTextFormatter(AbstractFormatter):
    """Provides a formatter for plain texts, rearranging by paragraphs and removing strange characters from the text"""

    def __init__(self):
        """Default constructor"""
        super(PlainTextFormatter, self).__init__()

    def format(self, text: str) -> str:
        """Format text, clean up weird characters and rearrange it"""
        old_text = text.replace("\r", "")
        new_text = ""
        counter = 0
        for character in old_text:
            if character == "-" and old_text[counter + 1] == "\n":
                new_text += ""
            else:
                if character == "\n":
                    if old_text[counter - 1] == ".":
                        new_text += "\n\n"
                    elif old_text[counter - 1] == ":":
                        new_text += "\n"
                    if old_text[counter + 1] == " ":
                        new_text += "  "
                else:
                    new_text += character
            counter += 1
        return new_text
