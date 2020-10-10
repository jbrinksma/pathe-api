AUTH_TOKEN_HEADER_NAME = "X-Client-Token"
AUTH_TOKEN = "03f9f5feb3734c94831a972c932a7007"
API_MAIN_BASE_URL = "https://connect.pathe.nl/v1/"

CINEMAS_REQ_PATH = "cinemas"
LABELS_REQ_PATH = "labels"
MOVIES_REQ_PATH = "cinemas/schedules"
SEATS_REQ_PATH = "schedules/{}/seats"  # insert scheduleId


# Seat states
SEAT_AVAILABLE = 0
SEAT_UNAVAILABLE = 1
SEAT_TAKEN = 3

# Seat type
SEAT_TYPE_ANYONE = None
SEAT_TYPE_HANDICAPPED = "WC"
