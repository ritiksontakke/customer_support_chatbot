import requests
from config import API_BASE_URL


def login(email: str, password: str):
    """
    Login to FastAPI backend.
    """

    url = f"{API_BASE_URL}/auth/login"

    response = requests.post(
        url,
        data={
            "username": email,
            "password": password,
        },
    )

    if response.status_code == 200:
        return response.json()

    return None

from api import signup

def register(
    username,
    email,
    password,
):
    return signup(
        username,
        email,
        password,
    )