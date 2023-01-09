import re

from django.http import HttpResponse, JsonResponse
from django.views import View

from api_app.nasa import NasaAPI, NasaAPIException


class ObjectsView(View):
    DATE_TIME_FORMAT = "YYYY-MM-DD"

    @staticmethod
    def _is_valid_date_format(date: str) -> bool:
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date))

    def _get_date_range(self, query_params: dict) -> tuple:
        """
        Fetch start and end dates from query_params and validate them

        :param query_params: query dict with start date and end date keys
        :return:  (start_date, end_date)
        """

        start_date = query_params.get("start_date")
        end_date = query_params.get("end_date")

        if not start_date or not end_date:
            raise ValueError

        if not self._is_valid_date_format(start_date) or not self._is_valid_date_format(
            end_date
        ):
            raise ValueError

        return start_date, end_date

    def get(self, request):
        try:
            start_date, end_date = self._get_date_range(request.GET)
        except ValueError:
            return HttpResponse(
                f"Invalid date format, please follow next format: {self.DATE_TIME_FORMAT}"
                f"or you forgot to add `start_date` or `end_date`",
                status=400,
            )

        nasa_api = NasaAPI()
        try:
            objects = nasa_api.get_earth_objects(start_date, end_date)
        except NasaAPIException:
            return HttpResponse(
                f"Ooopss... Something went wrong on NASA server, try to check this endpoint later",
                status=500,
            )
        return JsonResponse({"data": objects})
