"""Small utility functions."""
from secrets import randbelow

from fake_useragent import UserAgent


def random_user_agent() -> str:
    """Choose a user agent from a list of commonly used agents."""
    user_agent = UserAgent(browsers=["edge", "firefox", "chrome", "safari"])
    return str(user_agent.random)


def get_valid_usa_distance() -> str:
    """Return a valid distance for USA lookups."""
    return str(5823 + randbelow(1000))
