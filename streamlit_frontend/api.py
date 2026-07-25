import requests
from config import API_BASE_URL

BASE_URL = API_BASE_URL

def stream_chat(query, thread_id, token):

    response = requests.post(
        f"{API_BASE_URL}/query",
        json={
            "query": query,
            "thread_id": thread_id,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
        stream=True,
    )

    if response.status_code == 401:
        raise Exception("🔒 Your session has expired. Please log in again.")

    if response.status_code == 403:
        raise Exception("🚫 You are not authorized to perform this action.")

    if response.status_code >= 500:
        raise Exception("⚠️ Server error. Please try again later.")

    response.raise_for_status()

    return response


def signup(username, email, password, product, issue_description):
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json={
            "username": username,
            "email": email,
            "password": password,
            "product": product,
            "issue_description": issue_description,
            "status": "Open",
            "role": "customer",
        },
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        try:
            detail = response.json().get("detail")
        except Exception:
            detail = None

        if detail:
            raise Exception(detail)

        if response.status_code == 500:
            raise Exception("⚠️ Our server encountered an unexpected error. Please try again in a few moments.")

        raise Exception(f"Request failed (HTTP {response.status_code})")

    return response.json()