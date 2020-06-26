import datetime
import urllib.parse

from utils import log


def url_validator(url: str) -> bool:
    """Validate if a given string is a URL"""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def date_validator(date: str) -> bool:
    """Checks if the given string is in the correct date format and not in past.
       Date format: YYYY-MM-DD HH:MM"""
    try:
        datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")

        if datetime_obj < datetime.datetime.now():
            return False
        return True
    except ValueError:
        return False


def check_if_date_is_today(date: str) -> bool:
    """Checks if the given date (as string) is today"""
    datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")

    if datetime_obj.date() == datetime.datetime.now().date():
        return True
    return False


def check_if_date_is_this_week(date: str) -> bool:
    """Checks if the given date (as string) is in this week"""
    datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")

    if datetime_obj.date() < datetime.datetime.now().date() + datetime.timedelta(
        days=7
    ):
        return True
    return False
