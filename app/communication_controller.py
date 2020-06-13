import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()


SERVER_NAME = getenv('SERVER_NAME', 'baloo.local')
API_KEY = getenv('API_KEY', 'empty')


def download_job() -> dict:
    url = f"http://{SERVER_NAME}/job/queue?api_key={API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        raise ConnectionError(f"Response from server: {r.status_code} {r.json().get('error')}")


def send_warming_up(idx):
    url = f"http://{SERVER_NAME}/job/{idx}?api_key={API_KEY}"
    data = {
        'status': 'warming up'
    }
    r = requests.post(url, json=data)
    if r.status_code == 200:
        return r.json()
    else:
        raise ConnectionError(f"Response from server: {r.status_code} {r.json().get('error')}")


def send_result(idx, result):
    url = f"http://{SERVER_NAME}/job/{idx}?api_key={API_KEY}"
    data = {
        'status': 'done',
        'result': result
    }
    r = requests.post(url, json=data)
    if r.status_code == 200:
        return r.json()
    else:
        raise ConnectionError(f"Response from server: {r.status_code} {r.json().get('error')}")


def send_error(idx):
    url = f"http://{SERVER_NAME}/job/{idx}?api_key={API_KEY}"
    data = {
        'status': 'failed',
    }
    r = requests.post(url, json=data)
    if r.status_code == 200:
        return r.json()
    else:
        raise ConnectionError(f"Response from server: {r.status_code} {r.json().get('error')}")


if __name__ == '__main__':
    download_job()
