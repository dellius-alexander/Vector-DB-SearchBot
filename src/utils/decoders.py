from src.myLogger.Logger import getLogger as GetLogger
log = GetLogger(__name__)


class IWordDecoder:
    floats: list = None
    decoded_word: str = None


class WordDecoder(IWordDecoder):
    """
    This class is used to decode a list of floats into a word.

    Attributes:
        floats (list): A list of floats to decode.
        decoded_word (str): The decoded word.

    Methods:
        decode(floats: list = None): Decodes the list of floats into a word.

    """
    _state: IWordDecoder = None

    # Initialize the class
    def __init__(self, floats: list = None):
        self.floats = floats
        self.decoded_word = self.decode(self.floats)
        self._state = self

    # Create a method to decode the floats
    def decode(self, floats: list = None) -> str or None:
        """
        Decodes the list of floats into a word.

        :param floats: A list of floats to decode.
        :return: The decoded word.

        """
        try:

            floats = floats if floats is not None else self.floats
            if floats is None:
                raise ValueError('No floats were provided to decode.')
            # Create a list of characters to store the decoded characters
            characters = []
            # Iterate through each float in the list of floats
            for float_val in floats:
                # Calculate the ASCII value from the float
                char_val = int(float_val * 256)
                # Append the decoded character to the list
                characters.append(chr(char_val))
            # Join the characters to form the decoded word
            self.decoded_word = "".join(characters)
            # Return the decoded word
            return self.decoded_word
        except Exception as e:
            log.error(e)
            return None

    def __dict__(self):
        return [{"WordDecoder": {
            "floats": self.floats,
            "decoded_word": self.decoded_word
        }}]

    def __str__(self):
        return str(self.__dict__())

    def __setstate__(self, state) -> None:
        self._state = state

    def __getstate__(self) -> IWordDecoder:
        return self._state
