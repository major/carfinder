"""Testing the Toyota lookups."""
from unittest import mock

import pytest

from carfinder import client


class TestToyota:
    """Testing the Toyota lookups."""

    @pytest.mark.vcr()
    def test_get_models(self):
        """Verify that we can retrieve models from Toyota."""
        toyota = client("toyota")
        models = toyota.get_models()
        assert isinstance(models, list)
        assert len(models) > 0
        assert {"modelCode", "title"} == set(models[0])
        assert {"modelCode": "4runner", "title": "4Runner"} in models

    @pytest.mark.vcr()
    def test_get_vehicles_page(self):
        """Verify that we can retrieve a page of vehicles from Toyota."""
        toyota = client("toyota")
        vehicles = toyota.get_vehicles_page("supra", 1)
        assert isinstance(vehicles, list)
        assert len(vehicles) > 0

    def test_get_vehicles(self):
        """Test retrieving multiple vehicles."""
        toyota = client("toyota")
        with mock.patch.object(toyota, "get_vehicles_page") as mock_get_vehicles_page:
            mock_get_vehicles_page.side_effect = [
                [{"name": "vehicle1"}, {"name": "vehicle2"}, {"name": "vehicle3"}],
                [{"name": "vehicle4"}, {"name": "vehicle5"}, {"name": "vehicle6"}],
                [],
            ]
            vehicles = toyota.get_vehicles("supra")
            assert isinstance(vehicles, list)
            assert len(vehicles) == 6
            assert mock_get_vehicles_page.call_count == 3
            assert mock_get_vehicles_page.call_args_list == [
                mock.call("supra", 1),
                mock.call("supra", 2),
                mock.call("supra", 3),
            ]

    def test_get_vehicles_no_pages(self):
        """Test getting vehicles when no pages are returned."""
        toyota = client("toyota")
        with mock.patch.object(toyota, "get_vehicles_page") as mock_get_vehicles_page:
            mock_get_vehicles_page.side_effect = [["vehicle1"] for x in range(1, 10000)]
            vehicles = toyota.get_vehicles("supra")
            assert isinstance(vehicles, list)
            assert len(vehicles) == 99
            assert mock_get_vehicles_page.call_count == 99
