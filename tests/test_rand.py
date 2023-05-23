import json

from src.utils import get_attribute


def test_object_attributes(__object__: object = "Hello World!"):
    """ Test the get_attribute function. """
    resp = get_attribute(__object__, ['__str__', '__len__'])
    assert resp == ["__len__", "__str__"]
    print("\nResponse:")
    print(resp)
