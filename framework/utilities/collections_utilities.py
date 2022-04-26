from typing import Any
from collections.abc import Iterable


class CollectionUtilities:

    @classmethod
    def to_list(cls, obj: Any) -> list:
        """
        Convert object to list 

        @return: object of list type

        @param: any variable
        """

        if cls.is_iterable(obj):
            return obj
        else: 
            return [obj]

    @classmethod
    def is_iterable(cls, obj: Any) -> bool:
        """
        Determines object is iterable or no

        NOTE: any string are considered as non-iterable

        @return: True if object can be iterable, else - False

        @param: any variable
        """

        return isinstance(obj, Iterable) and not isinstance(obj, str)
