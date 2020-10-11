class PatheSeat:
    def __init__(self, json_seat: dict):
        self.id = json_seat["id"]
        self.name = json_seat["name"]
        self.state = json_seat["state"]
        self.type = json_seat["type"]
        self.x = json_seat["x"]
        self.y = json_seat["y"]
    
    def __repr__(self):
        return f"<PatheSeat(name={self.name}, state={self.state}, type={self.type})>"


class PatheSeatsRow:
    def __init__(self, row_json: dict):
        self.name = row_json["name"]
        self.seats = [PatheSeat(seat) for seat in row_json["seats"]]
    
    def __repr__(self):
        return f"<PatheSeatsRow(name={self.name}, contains {len(self.seats)} seats)>"


class PatheSeats:
    def __init__(self, seats_json: dict):
        seats_json = seats_json["blocks"][0]
        self.id = seats_json["id"]
        self.rows = [PatheSeatsRow(row) for row in seats_json["rows"]]
    
    def __repr__(self):
        return f"<PatheSeats(contains {len(self.rows)} rows)>"


class PatheCity:
    def __init__(self, city_json: dict):
        self.id = city_json["id"]
        self.name = city_json["name"]
        self.code = city_json["code"]
        self.province = city_json["province"]
    
    def __repr__(self):
        return f"<PatheCity(name={self.name})>"


class PatheSchedule:
    """Make sure to define `PatheSchedule().seats` with `PatheApi.get_seats()`"""
    def __init__(self, schedule_json: dict):
        self.id = schedule_json["id"]
        self.cinema_id = schedule_json["cinemaId"]
        self.movie_id = schedule_json["movieId"]
        self.movie_name = schedule_json["movieName"]
        self.tag = schedule_json["tag"]
        self.start = schedule_json["start"]
        self.end = schedule_json["end"]
        self.status = schedule_json["status"]

        self.seats = None  # This should be defined by PatheApi.get_seats


    def __repr__(self):
        return f"<PatheSchedule(movie_name={self.movie_name}, start={self.start})>"


class PatheMovie:
    def __init__(self, movie_json: dict):
        self.id = movie_json["id"]
        self.name = movie_json["name"]
        self.p_age = movie_json["pAge"]
        self.release_date = movie_json["releaseDate"]
        self.total_exhibitions = movie_json["totalExhibitions"]
        self.teaser = movie_json["teaser"]
    
    def __repr__(self):
        return f"<PatheMovie(name={self.name}, release_date={self.release_date})>"


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
    
    def __repr__(self):
        return f"<PatheCinema(name={self.name}, code={self.code}, city={self.city})>"


class PatheTimetable:
    def __init__(self, timetable_json: dict, cinemas: list):
        json_cinemas = [cinema["id"] for cinema in timetable_json["cinemas"]]
        self.cinemas = [cinema for cinema in cinemas if cinema.id in json_cinemas]
        self.days = timetable_json["days"]
        self.movies = [PatheMovie(movie_json) for movie_json in timetable_json["movies"]]
        self.noscheduletext = timetable_json["noscheduletext"]
        self.schedules = [PatheSchedule(schedule_json) for schedule_json in timetable_json["schedules"]]
        self.shownoscheduledate = timetable_json["shownoscheduledate"]
        self.type = timetable_json["type"]
    
    def __repr__(self):
        return f"<PatheTimetable(days={self.days})>"