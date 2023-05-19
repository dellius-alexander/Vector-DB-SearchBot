import json
from typing import List


def get_attribute(__object__: object, __attributes__: List[str]):
    """
    Get an attribute(s) from an object.

    Parameters
    ----------
    __object__ : object
        The object to get the attribute(s) from.
    __attributes__ : List[str]
        The attribute(s) to get from the object.

    Returns
    -------
    object
        The attribute(s) from the object.
    """
    return [a for a in dir(__object__) if a in __attributes__]


