"""Very basic tests for carfinder."""
import pytest

from carfinder import UnknownManufacturer, client


def test_invalid_manufacturer():
    """Test that an invalid manufacturer raises an exception."""
    with pytest.raises(UnknownManufacturer):
        client("delorean")
