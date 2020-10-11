import urllib
from datetime import date


def get_current_date():
    """Returns date in format of YYYY-MM-DD"""
    return str(date.today().strftime("%Y-%m-%d"))

def cinemas_to_req_str(cinemas: list):
    """Return a string of cinema id's which can be used in `PatheApi.get_movies()`.
    
    :param cinemas: list of `PatheCinema`'s.
    """
    req_str = ""
    for cinema in cinemas:
        req_str += f"{cinema.id},"
    return req_str[:-1] if req_str else req_str


# def dates_to_req_str(dates: list):
#     """Return a string of dates which can be used in `PatheApi.get_movies()`.
    
#     :param cinemas: List of strs containing dates in format `YYYY-MM-DD`.
#     """
#     req_str = ""
#     for date in dates:
#         req_str += f"{date},"
#     return req_str[:-1] if req_str else req_str
