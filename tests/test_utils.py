"""Test the small utility functions."""
from carfinder import utils


def test_random_user_agent():
    """Test that the random_user_agent function returns a string."""
    user_agent = utils.random_user_agent()
    assert isinstance(user_agent, str)
    assert user_agent.startswith("Mozilla/")
