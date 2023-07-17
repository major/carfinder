"""Testing the Lexus lookups."""
from unittest import mock

import pytest

from carfinder import client


class TestLexus:
    """Testing the Lexus lookups."""

    @pytest.mark.vcr()
    def test_get_models(self):
        """Verify that we can retrieve models from Lexus."""
        lexus = client("lexus")
        models = lexus.get_models()
        assert isinstance(models, list)
        assert len(models) > 0
        assert {"modelCode", "series"} == set(models[0])
        assert {"modelCode": "is", "series": "IS"} in models

    @pytest.mark.vcr()
    def test_get_vehicles_page(self):
        """Verify that we can retrieve a page of vehicles from Lexus."""
        lexus = client("lexus")
        vehicles = lexus._get_vehicles_page("RCF", 1)
        assert isinstance(vehicles, list)
        assert len(vehicles) > 0

    def test_get_vehicles(self):
        """Test retrieving multiple vehicles."""
        lexus = client("lexus")
        with mock.patch.object(lexus, "_get_vehicles_page") as mock_get_vehicles_page:
            mock_get_vehicles_page.side_effect = [
                ["vehicle1", "vehicle2", "vehicle3"],
                ["vehicle4", "vehicle5", "vehicle6"],
                [],
            ]
            vehicles = lexus.get_vehicles("RCF")
            assert isinstance(vehicles, list)
            assert len(vehicles) == 6
            assert mock_get_vehicles_page.call_count == 3
            assert mock_get_vehicles_page.call_args_list == [
                mock.call("RCF", 1),
                mock.call("RCF", 2),
                mock.call("RCF", 3),
            ]

    def test_get_vehicles_no_pages(self):
        """Test getting vehicles when no pages are returned."""
        lexus = client("lexus")
        with mock.patch.object(lexus, "_get_vehicles_page") as mock_get_vehicles_page:
            mock_get_vehicles_page.side_effect = [["vehicle1"] for x in range(1, 10000)]
            vehicles = lexus.get_vehicles("RCF")
            assert isinstance(vehicles, list)
            assert len(vehicles) == 99
            assert mock_get_vehicles_page.call_count == 99
