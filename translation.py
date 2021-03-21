"""
This module provides all the necessary functionality to work with translation.
"""

from deep_translator import GoogleTranslator


class TranslationException(Exception):
    """This exception will be raised in case there is a failure with the translator"""

    def __init__(self, *args, **kwargs):
        """This constructor is in charge of passing the necessary arguments to the base class"""
        super(TranslationException, self).__init__(args, kwargs)


class PlainTextTranslator:
    """This class is used to translate plain text from one language to another."""

    def __init__(self, source: str, target: str):
        """Start the basic settings of the translator"""
        super(PlainTextTranslator, self).__init__()
        if source == target:
            self.__translator = None
            raise TranslationException()
        else:
            self.__translator = GoogleTranslator(source=source, target=target)

    def translate(self, text):
        if self.__translator is not None:
            return self.__translator.translate(text)
        else:
            return "Translation failed"
