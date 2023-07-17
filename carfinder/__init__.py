"""Factory for classes for each car manufacturer."""
from typing import List, Type

from carfinder.manufacturers import BaseManufacturer
from carfinder.manufacturers.lexus import Lexus
from carfinder.manufacturers.toyota import Toyota

available_manufacturers: List[Type[BaseManufacturer]] = [Lexus, Toyota]


class UnknownManufacturer(Exception):
    """Exception when someone asks for an unknown manufacturer."""

    def __init__(self, manufacturer_name: str):
        """Print a friendly message describing the problem."""
        super().__init__(f"Invalid manufacturer name: {manufacturer_name}")


def client(manufacturer_name: str) -> BaseManufacturer:
    """Return the correct client for the specified manufacturer."""
    for mfr_class in available_manufacturers:
        if mfr_class.brand == manufacturer_name:
            return mfr_class()
    raise UnknownManufacturer(manufacturer_name)
