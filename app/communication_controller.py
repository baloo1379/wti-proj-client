import requests


SERVER_NAME = 'baloo.local'


def download_job() -> dict:
    r"""
    GET /job/queue

    :return: dict: Data from server queue
    """
    url = f"http://{SERVER_NAME}/job/queue"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        raise ConnectionError(f"Response from server: {r.status_code} {r.json().get('error')}")


def send_warming_up(idx):
    r"""
    POST /job/<idx>

    :return: bool:
    """
    url = f"http://{SERVER_NAME}/job/{idx}"
    data = {
        'status': 'warming up'
    }
    r = requests.post(url, json=data)
    if r.status_code == 200:
        return r.json()
    else:
        raise ConnectionError(f"Response from server: {r.status_code} {r.json().get('error')}")


def send_result(idx, result):
    url = f"http://{SERVER_NAME}/job/{idx}"
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
    url = f"http://{SERVER_NAME}/job/{idx}"
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
