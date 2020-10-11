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
from classes import (
    PatheCinema,
    PatheTimetable,
    PatheSeats
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

    def get_cinemas(self, get_raw_json: bool = False) -> list or dict:
        raw_json = self.get_json_request(CINEMAS_REQ_PATH)
        if get_raw_json:
            return raw_json
        return [PatheCinema(cinema_json) for cinema_json in raw_json]
    
    def get_labels(self) -> dict:
        """Experimental"""
        return self.get_json_request(LABELS_REQ_PATH)

    def get_timetable(self, cinemas: list, date: str, get_raw_json: bool = False) -> PatheTimetable or dict:
        """Get all movies running on a specific date.

        Getting the seat information per `PatheSchedule` requires an API request per schedule.
        By default, this will not be done, so in order to get seat information for your schedules,
        you will need to find a smart way to populate all `PatheSchedule`'s with their `.seats` attribute.
        For example, through threading, and a small time delay, so as to not overwhelm Pathe's API.

        The way to do a single schedule would be:
        `pathe_schedule1.seats = get_seats(pathe_schedule.id)`

        :param cinemas: list of `PatheCinema`'s
        :param cinemas: str containing date in format `YYYY-MM-DD`"""
        raw_json = self.get_json_request(
            MOVIES_REQ_PATH,
            url_params = {
                "ids": cinemas_to_req_str(cinemas),
                "date": date
            }
        )
        if get_raw_json:
            return raw_json
        return PatheTimetable(raw_json, cinemas)
    
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
    # Testing purposes
    try:
        api = PatheApi()
        cinemas = api.get_cinemas()
        timetable = api.get_timetable(cinemas, get_current_date())
        for cinema in timetable.cinemas:
            print(cinema)
        for movie in timetable.movies:
            print(movie)
        for schedule in timetable.schedules:
            print(schedule)
        print(timetable.days)
        print(timetable)
        if timetable.schedules:
            timetable.schedules[0].seats = api.get_seats(timetable.schedules[0].id)
            print(timetable.schedules[0].seats)
            print(f"Total seats: {api.count_total_seats(seats=timetable.schedules[0].seats)}")
            print(f"Available seats: {api.count_available_seats(seats=timetable.schedules[0].seats)}")
    except Exception as e:
        print(f"Test failed :( -> {e}")
