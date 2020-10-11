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


class PatheSeat:
    def __init__(self, json_seat: dict):
        self.id = json_seat["id"]
        self.name = json_seat["name"]
        self.state = json_seat["state"]
        self.type = json_seat["type"]
        self.x = json_seat["x"]
        self.y = json_seat["y"]


class PatheSeatsRow:
    def __init__(self, row_json: dict):
        self.name = row_json["name"]
        self.seats = [PatheSeat(seat) for seat in row_json["seats"]]


class PatheSeats:
    def __init__(self, seats_json: dict):
        seats_json = seats_json["blocks"][0]
        self.id = seats_json["id"]
        self.rows = [PatheSeatsRow(row) for row in seats_json["rows"]]


class PatheCity:
    def __init__(self, city_json: dict):
        self.id = city_json["id"]
        self.name = city_json["name"]
        self.code = city_json["code"]
        self.province = city_json["province"]


class PatheCinema:
    def __init__(self, cinema_json: dict):
        self.id = cinema_json["id"]
        self.name = cinema_json["name"]
        self.city = PatheCity(cinema_json["city"])
        self.city_id = cinema_json["cityId"]
        self.code = cinema_json["code"]
        self.address = cinema_json["address"]
        self.zipcode = cinema_json["zipcode"]
        self.lat = cinema_json["lat"]
        self.lon = cinema_json["lon"]
        self.phonenumber = cinema_json["phonenumber"]
        self.site_id = cinema_json["siteId"]
        self.ticket_sales_type_id = cinema_json["ticketSalesTypeId"]
        self.image = cinema_json["image"]


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

    def get_cinemas(self, get_raw_json: bool = False) -> list or dict:
        raw_json = self.get_json_request(CINEMAS_REQ_PATH)
        if get_raw_json:
            return raw_json
        return [PatheCinema(cinema_json) for cinema_json in raw_json]
    
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
    
    def get_seats(self, schedule_id: str, get_raw_json: bool = False) -> list or dict:
        raw_json = self.get_json_request(SEATS_REQ_PATH.format(schedule_id))
        if get_raw_json:
            return raw_json
        return PatheSeats(raw_json)
    
    def count_total_seats(self, seats: dict = None) -> int:
        """Supply either a seats dict or schedule_id

        :param seats: `PatheSeats`"""
        total_seats = 0
        for row in seats.rows:
            for _ in row.seats:
                total_seats += 1
        return total_seats
    
    def count_available_seats(self, seats: dict = None, handicapped: bool = False) -> int:
        """Supply either a seats dict or schedule_id

        :param seats: `PatheSeats`
        :param incl_handicapped: True if only handicapped seats should count"""
        available_seats = 0
        for row in seats.rows:
            for seat in row.seats:
                if seat.state == SEAT_AVAILABLE:
                    if handicapped and seat.type == SEAT_TYPE_HANDICAPPED:
                        available_seats += 1
                    elif not handicapped and seat.type == None:
                        available_seats += 1
        return available_seats


if __name__ == "__main__":
    # Test (Use existing schedule_id or you will get 400 error)
    api = PatheApi()
    cinemas = api.get_cinemas()
    seats = api.get_seats("3584161")
    print(f"Total seats: {api.count_total_seats(seats=seats)}")
    print(f"Available seats: {api.count_available_seats(seats=seats)}")
