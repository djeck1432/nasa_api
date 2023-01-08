import logging
import re
from datetime import datetime, timedelta
from math import ceil

import requests
from django.conf import settings

logger = logging.getLogger("NasaAPI")


class NasaAPIException(Exception):
    pass


class NasaAPI:
    """
    All info about NASA API you can find here:
    https://api.nasa.gov/
    """

    API_KEY = "t4Eg5afv1fBtXa6lBWGH8wcTpxaQCgOUuvXGVmJ8" or settings.NASA_API_KEY
    BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

    @staticmethod
    def _split_dates_by_7_days_batch(start_date_str: str, end_date_str: str) -> list:
        """

        :param start_date_str: start date in str format
        :param end_date_str: end date in str format
        :return: list of tuple/s
        """
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        delta = end_date - start_date
        if not delta.days > 7:
            return [(start_date_str, end_date_str)]

        result = []
        num_batches = ceil(delta.days / 7)
        for index in range(num_batches):
            batch_start_date = start_date + timedelta(days=index * 7)
            delta_end_date = (end_date - batch_start_date).days
            if delta_end_date > 7:
                batch_end_date = batch_start_date + timedelta(days=6)
            else:
                batch_end_date = batch_start_date + timedelta(days=delta_end_date)

            result.append((batch_start_date.isoformat(), batch_end_date.isoformat()))

        return result

    def _get_response_data(self, start_date: str, end_date: str) -> dict:
        """
        Send requests with next params:
        `start_date` and `end_date` and `api_key`
        :param start_date: start date
        :param end_date: end date
        :return: response or raise error
        """
        query_params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.API_KEY,
        }
        response = requests.get(self.BASE_URL, params=query_params)
        if response.ok:
            return response.json()

        logger.error(f"Nasa API returned next error: {response.text}")
        raise NasaAPIException

    @staticmethod
    def _calculate_average_size(sizes: dict) -> str:
        """
        calculate average size based on min and max size
        :param sizes: min and max sizes
        :return: rounded
        """
        average_size = (
            sizes["estimated_diameter_min"] + sizes["estimated_diameter_max"]
        ) / 2
        return format(average_size, ".2f")

    def get_earth_objects(self, start_date: str, end_date: str) -> list:
        batch_dates = self._split_dates_by_7_days_batch(start_date, end_date)
        result = []
        for start_date_batch, end_date_batch in batch_dates:
            result.extend(
                self.get_earth_objects_batch(start_date_batch, end_date_batch)
            )

        return result

    def get_earth_objects_batch(self, start_date: str, end_date: str) -> list:
        """
        Get all earths objects
        :param start_date: start date of searching
        :param end_date: end date of searching
        :return: list of objects
        """
        data = self._get_response_data(start_date, end_date)

        approaching_objects = []
        for date in data["near_earth_objects"]:
            for obj in data["near_earth_objects"][date]:
                close_approach_data = obj["close_approach_data"][0]
                approaching_objects.append(
                    {
                        "name": obj["name"],
                        "size_estimate": self._calculate_average_size(
                            obj["estimated_diameter"]["kilometers"]
                        ),
                        "date": close_approach_data["close_approach_date"],
                        "distance": close_approach_data["miss_distance"]["kilometers"],
                    }
                )
        approaching_objects.sort(key=lambda x: x["distance"])
        return approaching_objects

    @staticmethod
    def _is_valid_date_format(date: str) -> bool:
        """
        Check if a string is in the YYYY-MM-DD date format.
        request example:
        `https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY`
        """
        date_regex = r"\d{4}-\d{2}-\d{2}"
        return bool(re.fullmatch(date_regex, date))
