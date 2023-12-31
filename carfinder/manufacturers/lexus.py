"""Get data from Lexus."""
import uuid
from dataclasses import dataclass
from typing import Any

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from carfinder.manufacturers import BaseManufacturer
from carfinder.utils import get_valid_usa_distance, random_user_agent

QUERY_MODELS = """
query {
  models(zipCd: "90210", brand: "L") {
    modelCode
    series
  }
}
"""

QUERY_VEHICLES = """
query {
  locateVehiclesByZip(
    zipCode: "ZIP_CODE"
    brand: "LEXUS"
    pageNo: PAGE_NUMBER
    pageSize: 250
    seriesCodes: "MODEL_NAME"
    distance: DISTANCE
    leadid: "RANDOM_UUID"
  ) {
    pagination {
      pageNo
      pageSize
      totalPages
      totalRecords
    }
    vehicleSummary {
      vin
      stockNum
      brand
      marketingSeries
      year
      isTempVin
      dealerCd
      dealerCategory
      distributorCd
      holdStatus
      weightRating
      isPreSold
      dealerMarketingName
      dealerWebsite
      isSmartPath
      distance
      isUnlockPriceDealer
      transmission {
        transmissionType
      }
      price {
        advertizedPrice
        nonSpAdvertizedPrice
        totalMsrp
        sellingPrice
        dph
        dioTotalMsrp
        dioTotalDealerSellingPrice
        dealerCashApplied
        baseMsrp
      }
      options {
        optionCd
        marketingName
        marketingLongName
        optionType
        packageInd
      }
      mpg {
        city
        highway
        combined
      }
      model {
        modelCd
        marketingName
        marketingTitle
      }
      media {
        type
        href
        imageTag
        source
      }
      intColor {
        colorCd
        colorSwatch
        marketingName
        nvsName
        colorFamilies
      }
      extColor {
        colorCd
        colorSwatch
        marketingName
        colorHexCd
        nvsName
        colorFamilies
      }
      eta {
        currFromDate
        currToDate
      }
      engine {
        engineCd
        name
      }
      drivetrain {
        code
        title
        bulletlist
      }
      family
      cab {
        code
        title
        bulletlist
      }
      bed {
        code
        title
        bulletlist
      }
    }
  }
}
"""

LEXUS_HEADERS = headers = {
    "origin": "https://www.lexus.com",
    "referrer": "https://www.lexus.com/",
    "user-agent": random_user_agent(),
}


@dataclass
class Lexus(BaseManufacturer):
    """For Lexus lookups."""

    brand: str = "lexus"

    def _run_query(self, query: str) -> dict[str, Any]:
        """Run a graphql query.

        Args:
            query: The graphql query to run.

        Returns:
            The result of the query as a dict.
        """
        transport = RequestsHTTPTransport(url="https://api.search-inventory.toyota.com/graphql", headers=LEXUS_HEADERS)
        client = Client(transport=transport)
        return client.execute(gql(query))

    def _get_vehicles_page(self, model_name: str, page_number: int) -> list[str]:
        """Get a page of Lexus vehicles.

        Args:
          model_name: Model name to query
          page_number: Page number to query (default: 1)
        """
        query = QUERY_VEHICLES
        query = query.replace("ZIP_CODE", "90210")
        query = query.replace("PAGE_NUMBER", f"{page_number}")
        query = query.replace("MODEL_NAME", model_name)
        query = query.replace("DISTANCE", get_valid_usa_distance())
        query = query.replace("RANDOM_UUID", str(uuid.uuid4()))

        result = self._run_query(query)
        return list(result["locateVehiclesByZip"]["vehicleSummary"])

    def get_models(self) -> list[str]:
        """Get a list of Lexus models.

        Returns:
            A list of Lexus models.
        """
        result = self._run_query(QUERY_MODELS)
        return list(result["models"])

    def get_vehicles(self, model_name: str) -> list[str]:
        """Get a list of vehicles from Lexus matching a model_name.

        Args:
            model_name: Model name of the car, such as `4runner`.

        Returns:
            A list of vehicles from Lexus matching a model_name.
        """
        vehicles: list[str] = []

        for page_number in range(1, 100):
            # Get a page of vehicles.
            result = self._get_vehicles_page(model_name, page_number)

            # Add the page of vehicles to our running list.
            vehicles.extend(result)

            # Stop if our page is empty.
            if len(result) == 0:
                break

        return vehicles
