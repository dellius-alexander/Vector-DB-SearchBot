import numbers
import traceback
from json import JSONEncoder
from typing import Union, List, Any

import numpy as np

from ..myLogger.Logger import getLogger as GetLogger
import random

log = GetLogger(__name__)


class IWordEncoder:
    text: str = None
    encoded_word_reshaped: list = None
    encoded_word: list = None
    normalize_encoded_word: list = None

    def encode(self, text: str = None) -> list or None:
        """
        Encodes the word into a list of floats.

        :param text: The text to encode.
        :return: The encoded word.

        """
        pass


class WordEncrypt:
    # special key to encrypt the encoded word
    encoded_word: list = None
    encoding_key: dict = None
    encrypted_word: list = None
    decrypted_word: list = None

    def __init__(self):
        self.encoding_key = {
            "key": random.uniform(0.0, 1.0),
        }

    def encrypt(self, encoded_word: list = None) -> list or None:
        """
        Encrypts the encoded word.
        """
        try:
            encoded_word = encoded_word if encoded_word is not None else self.encoded_word
            # Calculate the sum of the encoded word
            sum_word = sum(encoded_word) ** self.encoding_key["key"]
            # Create a list to store the encrypted word
            self.encrypted_word = []
            # Iterate through each value in the encoded word
            for val in encoded_word:
                # Calculate and append the encrypted value to the list
                self.encrypted_word.append(val / sum_word)
            return self.encrypted_word
        except Exception as e:
            log.error(e)
            return None

    def decrypt(self, encrypted_word: list = None) -> list or None:
        """
        Decrypts the encrypted encoded word.
        """
        try:
            encrypted_word = encrypted_word if encrypted_word is not None else self.encrypted_word
            # Calculate the sum of the encoded word
            sum_word = sum(self.encoded_word) ** self.encoding_key["key"]
            # Create a list to store the decrypted word
            self.decrypted_word = []
            # Iterate through each value in the encrypted word
            for val in encrypted_word:
                # Calculate and append the decrypted value to the list
                self.decrypted_word.append(val * sum_word)
            return self.decrypted_word
        except Exception as e:
            log.error(e)
            return None


class WordEncoder(IWordEncoder, WordEncrypt):
    """
    This class is used to encode a word into a list of floats.

    Attributes:
        encoded_word_reshaped (list): The encoded word resized and reshaped.
        encoded_word (list): The encoded word.
        text (str): The text to encode.

    Methods:
        encode(): Encodes the word into a list of floats.
    """
    _state: IWordEncoder = None

    # Initialize the class
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.encoded_word = self.encode()
        self.encrypted_word = self.encrypt()
        self.decrypted_word = self.decrypt()
        self.encoding_key = {
            "key": random.uniform(0.0, 1.0),
        }
        self.normalize_encoded_word = self.normalize()
        self.encoded_word_reshaped = None
        self._state = self
        log.info("\nInitial state: ")
        log.info(f"\n{self._state}")

    # Create a method to encode the word
    def encode(self, text: Union[List[Any], str] = None) -> list or None:
        """
        Encodes the word into a list of floats.

        :param text: The text to encode.
        :return: The encoded word.

        """
        try:
            text = text.__str__() if text is not None else self.text.__str__()
            if text is None:
                raise ValueError('No text was provided to encode.')
            # Create a list of characters to store the characters of the given word
            characters = []
            if isinstance(text, list) and len(text) >= 1:
                # Iterate through each character in the given word
                for char in text:
                    # check if the character is a array
                    if len(char.split()) > 1:
                        for c in char.split():
                            if len(c) > 1:
                                for cc in c:
                                    # Append the ASCII value of each character to the list
                                    characters.append(ord(cc))
                            else:
                                # Append the ASCII value of each character to the list
                                characters.append(ord(c))
                    else:
                        # Append the ASCII value of each character to the list
                        characters.append(ord(char))
            elif isinstance(text, str) and len(text) >= 1:
                # Iterate through each character in the given word
                for char in text:
                    # Append the ASCII value of each character to the list
                    characters.append(ord(char))
            else:
                raise ValueError('The text provided is not valid.')
            # Create a list of floats to store the floating point numbers
            floats = []
            # Iterate through each character in the list of characters
            for char in characters:
                # Calculate the floating point number from the ASCII value
                float_val = float(char) / 256
                # Append the floating point number to the list
                floats.append(float_val)
            # Store the encoded word
            self.encoded_word = floats
            # Return the list of floats
            return self.encoded_word
        except Exception:
            log.error(traceback.format_exc())
            return None

    # Create a method to resize and reshape the encoded word
    def resize_and_reshape(self, size: Union[int, tuple], encoded_word=None):
        try:
            encoded_word = np.array(encoded_word, dtype=float) if encoded_word is not None else \
                np.array(self.encoded_word, dtype=float)
            # Get the original array shape
            original_shape = encoded_word.shape
            log.info(f"\nOriginal shape: {original_shape}")
            log.info(f"\nOriginal size: {np.prod(original_shape)}")
            log.info(f"\nNew size: {np.prod(size)}")
            # Check if the new shape is compatible with the original shape
            if np.prod(a=size) <= np.prod(a=original_shape):
                # Resize
                resized_array = np.resize(encoded_word, size)
                # Reshape
                reshaped_array = np.reshape(resized_array, size)
                return reshaped_array
            # we pad if it the new size is greater than the original size
            elif np.prod(a=size) > np.prod(a=original_shape):
                padding = [float(a) for a in [0.0] * (np.prod(size) - np.prod(original_shape))]
                # add padding to the original array
                encoded_word = np.append(encoded_word, padding, axis=0)
                # Resize
                resized_array = np.resize(encoded_word, size)
                # Reshape
                reshaped_array = np.reshape(resized_array, size)
                return reshaped_array
            else:
                raise ValueError("\n\tReshape size is not compatible with the original shape. "
                                 f"\n\tOriginal shape: {original_shape}, "
                                 f"\n\tNew size: {np.prod(size)}")
        except Exception:
            log.error(traceback.format_exc())
            return None

    def resize_encoded_word(self, new_size: int, encoded_word=None):
        try:
            encoded_word = encoded_word if encoded_word is not None else self.encoded_word
            # Calculate the difference between the original and new sizes
            diff = len(encoded_word) - new_size
            # If the difference is negative (the new size is larger than the original size)
            if diff < 0 and not abs(diff) > len(encoded_word):
                # Add zeros to the beginning of the list to make up the difference
                encoded_word = [0] * abs(diff) + encoded_word
            # If the difference is positive (the new size is smaller than the original size)
            elif diff > 0:
                # Remove the extra values from the end of the list
                encoded_word = encoded_word[:diff]
            return encoded_word
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
            return None

    def reshape_encoded_word(self, new_size, encoded_word=None):
        try:
            encoded_word = encoded_word if encoded_word is not None else self.encoded_word
            # Use numpy to reshape the encoded word
            reshaped_word = np.reshape(encoded_word, (-1, new_size))
            # # Store the reshaped word
            # self.encoded_word_reshaped = reshaped_word
            return reshaped_word
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
            return None

    # Normalize the embedding
    def normalize(self, encoded_word: List[numbers.Number] = None) -> list or None:
        """
        Normalizes the encoded word.

        :return: None
        """
        encoded_word = encoded_word if encoded_word is not None else self.encoded_word
        # Calculate the sum of the encoded word
        sum_word = sum(encoded_word)
        # Create a list to store the normalized word
        normalized_word = []
        # Iterate through each value in the encoded word
        for val in encoded_word:
            # Calculate and append the normalized value to the list
            normalized_word.append(val / sum_word)
        # Store the normalized word
        self.normalize_encoded_word = normalized_word
        return normalized_word

    def un_normalize(self, encoded_word: list[float] = None, normalized_word: list[float] = None) -> list or None:
        """
        Un-normalizes the normalized encoded word.
        """
        encoded_word = encoded_word if encoded_word is not None else self.encoded_word
        normalized_word = normalized_word if normalized_word is not None else self.normalize()
        # Calculate the sum of the encoded word
        sum_word = sum(encoded_word)
        # Create a list to store the un-normalized word
        un_normalized_word = []
        # Iterate through each value in the normalized word
        for val in normalized_word:
            # Calculate and append the un-normalized value to the list
            un_normalized_word.append(val * sum_word)
        return un_normalized_word

    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)

    def __dict__(self):
        return [{"WordEncoder": {
            "text": self.text,
            "encoded_word": self.encoded_word,
            "encoded_word_reshaped": self.encoded_word_reshaped,
            "normalize_encoded_word": self.normalize_encoded_word,
            "encoding_key": self.encoding_key,
            "encrypted_word": self.encrypted_word,
            "decrypted_word": self.decrypted_word,
        }}]

    def __str__(self):
        return str(self.__dict__())

    def __setstate__(self, state) -> None:
        self._state = state

    def __getstate__(self) -> IWordEncoder:
        return self._state
