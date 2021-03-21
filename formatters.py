from impl import AbstractFormatter


class PlainTextFormatter(AbstractFormatter):
    """Provides a formatter for plain texts, rearranging by paragraphs and removing strange characters from the text"""
    
    def __init__(self):
        """Default constructor"""
        super(PlainTextFormatter, self).__init__()

    def format(self, text: str) -> str:
        """Format text, clean up weird characters and rearrange it"""
        return text.replace("\r", "").replace("\n", "")
