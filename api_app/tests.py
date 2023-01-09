from unittest.mock import patch

from django.test import TestCase

from api_app.nasa import NasaAPI, NasaAPIException
from .views import ObjectsView


class NasaAPITestCase(TestCase):
    def test__get_response_data(self):
        # Test successful request
        with patch("requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = {"key": "value"}

            api = NasaAPI()
            response_data = api._get_response_data("2019-01-01", "2019-01-02")
            self.assertEqual(response_data, {"key": "value"})
            mock_get.assert_called_with(
                api.BASE_URL,
                params={
                    "start_date": "2019-01-01",
                    "end_date": "2019-01-02",
                    "api_key": api.API_KEY,
                },
            )

        # Test request with failed response
        with patch("requests.get") as mock_get:
            mock_get.return_value.ok = False

            api = NasaAPI()
            with self.assertRaises(NasaAPIException):
                api._get_response_data("2019-01-01", "2019-01-02")

    def test__calculate_average_size(self):
        api = NasaAPI()
        sizes = {"estimated_diameter_min": 10, "estimated_diameter_max": 20}
        average_size = api._calculate_average_size(sizes)
        self.assertEqual(average_size, "15.00")

    def test_split_dates_by_7_days_batch(self):
        # Test with a date range of less than 7 days
        start_date = "2022-01-01"
        end_date = "2022-01-03"
        expected_output = [("2022-01-01", "2022-01-03")]
        self.assertEqual(
            NasaAPI._split_dates_by_7_days_batch(start_date, end_date), expected_output
        )

        # Test with a date range of exactly 7 days
        start_date = "2022-01-01"
        end_date = "2022-01-07"
        expected_output = [("2022-01-01", "2022-01-07")]
        self.assertEqual(
            NasaAPI._split_dates_by_7_days_batch(start_date, end_date), expected_output
        )

        # Test with a date range of more than 7 days
        start_date = "2022-01-01"
        end_date = "2022-01-10"
        expected_output = [("2022-01-01", "2022-01-07"), ("2022-01-08", "2022-01-10")]
        self.assertEqual(
            NasaAPI._split_dates_by_7_days_batch(start_date, end_date), expected_output
        )


class ObjectsViewTestCase(TestCase):
    def test_is_valid_date_format(self):
        # Test for validating inputted date
        view = ObjectsView()
        self.assertTrue(view._is_valid_date_format("2022-01-01"))
        self.assertFalse(view._is_valid_date_format("2022-01-01 12:00:00"))
        self.assertFalse(view._is_valid_date_format("2022-01-01 12:00:00 PM"))
        self.assertFalse(view._is_valid_date_format("2022/01/01"))
        self.assertFalse(view._is_valid_date_format("01-01-2022"))

    def test_get_date_range(self):
        # Test date range
        view = ObjectsView()
        query_params = {"start_date": "2022-01-01", "end_date": "2022-01-03"}
        start_date, end_date = view._get_date_range(query_params)

        self.assertEqual(start_date, "2022-01-01")
        self.assertEqual(end_date, "2022-01-03")

        query_params = {"start_date": "2022-01-01 12:00:00", "end_date": "2022-01-03"}
        with self.assertRaises(ValueError):
            view._get_date_range(query_params)

    def test_get_invalid_date_format(self):
        # Test GET request with invalid date format
        response = self.client.get(
            "/api/objects/",
            {"start_date": "2022-01-01 12:00:00", "end_date": "2022-01-03"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b"Invalid date format, please follow next format: YYYY-MM-DD"
            b"or you forgot to add `start_date` or `end_date`",
        )

    def test_get_success(self):
        # Test successful GET request
        return_value = [
            {
                "name": "(2021 AX3)",
                "size_estimate": 0.03,
                "date": "2022-01-12",
                "distance": 30361046.065845396,
            }
        ]

        with patch.object(NasaAPI, "get_earth_objects", return_value=return_value):
            response = self.client.get(
                "/api/objects/", {"start_date": "2022-01-01", "end_date": "2022-01-03"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"data": return_value})
