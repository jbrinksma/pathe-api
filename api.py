import requests
import json

from exceptions import (
    PatheApiException,
    REQUEST_FAILED
)
from config import (
    AUTH_TOKEN_HEADER_NAME,
    AUTH_TOKEN,
    API_MAIN_BASE_URL,

    CINEMAS_REQ_PATH,
    LABELS_REQ_PATH,
    MOVIES_REQ_PATH,
    SEATS_REQ_PATH,

    SEAT_AVAILABLE,
    SEAT_TYPE_HANDICAPPED
)
from utils import (
    get_current_date,
    cinemas_to_req_str
)


class PatheApi:
    def get_json_request(self, path, url_params: dict = None) -> dict:
        req = requests.get(
            API_MAIN_BASE_URL + path,
            headers = {AUTH_TOKEN_HEADER_NAME: AUTH_TOKEN},
            params = url_params
        )
        if req.status_code != 200:
            raise PatheApiException(REQUEST_FAILED)
        try:
            return json.loads(req.text)
        except ValueError:
            raise PatheApiException(REQUEST_FAILED)

    def get_cinemas(self) -> dict:
        return self.get_json_request(CINEMAS_REQ_PATH)
    
    def get_labels(self) -> dict:
        return self.get_json_request(LABELS_REQ_PATH)

    def get_movies(self, cinemas: dict, date: str) -> dict:
        """Get all movies running on a specific date

        :param cinemas: should be return of `PatheApi.get_cinemas()`
        :param cinemas: str containing date in format `YYYY-MM-DD`"""
        return self.get_json_request(
            MOVIES_REQ_PATH,
            url_params = {
                "ids": cinemas_to_req_str(cinemas),
                "date": date
            }
        )
    
    def get_seats(self, schedule_id: str) -> dict:
        return self.get_json_request(SEATS_REQ_PATH.format(schedule_id))
    
    def get_total_seats(self, seats: dict = None, schedule_id: int = None) -> int:
        """Supply either a seats dict or schedule_id

        :param seats: return of `PatheApi.get_seats()`
        :param schedule_id: if supplied, will do API request to get seats"""
        if not seats and not schedule_id:
            raise PatheApiException
        if schedule_id:
            seats = self.get_json_request(SEATS_REQ_PATH.format(schedule_id))

        total_seats = 0
        for row in seats["blocks"][0]["rows"]:
            for _ in row["seats"]:
                total_seats += 1
        return total_seats
    
    def get_available_seats(self, seats: dict = None, schedule_id: int = None, handicapped: bool = False) -> int:
        """Supply either a seats dict or schedule_id

        :param seats: return of `PatheApi.get_seats()`
        :param schedule_id: if supplied, will do API request to get seats
        :param incl_handicapped: True if only handicapped seats should count"""
        if not seats and not schedule_id:
            raise PatheApiException
        if schedule_id:
            seats = self.get_json_request(SEATS_REQ_PATH.format(schedule_id))

        available_seats = 0
        for row in seats["blocks"][0]["rows"]:
            for seat in row["seats"]:
                if seat["state"] == SEAT_AVAILABLE:
                    if handicapped and seat["type"] == SEAT_TYPE_HANDICAPPED:
                        available_seats += 1
                    elif not handicapped and seat["type"] == None:
                        available_seats += 1
        return available_seats


if __name__ == "__main__":
    # Test (Use existing schedule_id or you will get 400 error)
    api = PatheApi()
    cinemas = api.get_cinemas()
    seats = api.get_seats("3584161")
    print(f"Total seats: {api.get_total_seats(seats=seats)}")
    print(f"Available seats: {api.get_available_seats(seats=seats)}")
