import requests as rq
from requests.structures import CaseInsensitiveDict
import json
import pytest

home_url = "https://restful-booker.herokuapp.com"

# used in tests create_and_read and delete
data = [{
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-01-01",
        "checkout": "2019-01-01"
    },
    "additionalneeds": "Breakfast"}]

# used in tests update and partial_update
data_update = [(({
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-01-01",
        "checkout": "2019-01-01"
    },
    "additionalneeds": "Breakfast"}),
                ({
                    "firstname": "James",
                    "lastname": "Brown",
                    "totalprice": 111,
                    "depositpaid": True,
                    "bookingdates": {
                        "checkin": "2018-01-01",
                        "checkout": "2019-01-01"
                    },
                    "additionalneeds": "Breakfast"
                }))]


def test_ping():
    resp = rq.get(home_url + "/ping")
    assert resp.ok


@pytest.fixture
def cookie_auth():
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    data = '{"username":"admin","password":"password123"}'

    resp = rq.post(home_url + "/auth", headers=headers, data=data)
    token = json.loads(resp.text)["token"]
    # print(resp.status_code)
    # print(resp.text)
    return token, resp.ok


def test_auth(cookie_auth):
    assert cookie_auth[1]


@pytest.mark.parametrize("data", data)
def test_create_and_read(data):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = home_url + "/booking"

    data_str = str(json.dumps(data))

    resp = rq.post(url, headers=headers, data=data_str)
    assert resp.status_code == 200
    id = json.loads(resp.text)["bookingid"]

    resp = rq.get(url + "/" + str(id))
    assert resp.status_code == 200

    assert json.loads(resp.text) == data


@pytest.mark.parametrize("data,data_updated", data_update)
def test_update(cookie_auth, data, data_updated):
    cookie = cookie_auth
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = home_url + "/booking"

    data_str = str(json.dumps(data))

    resp = rq.post(url, headers=headers, data=data_str)
    assert resp.status_code == 200

    id = json.loads(resp.text)["bookingid"]

    url = url + "/" + str(id)
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Cookie"] = "token=" + cookie[0]

    data_str = str(json.dumps(data_updated))
    resp = rq.put(url, headers=headers, data=data_str)
    assert resp.status_code == 200
    resp = rq.get(url)
    assert json.loads(resp.text) == data_updated


@pytest.mark.parametrize("data,data_updated", data_update)
def test_update_partial(cookie_auth, data, data_updated):
    cookie = cookie_auth
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = home_url + "/booking"

    data_str = str(json.dumps(data))

    resp = rq.post(url, headers=headers, data=data_str)
    assert resp.status_code == 200

    id = json.loads(resp.text)["bookingid"]

    url = url + "/" + str(id)
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Cookie"] = "token=" + cookie[0]
    data = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111
    }
    data_str = str(json.dumps(data))
    resp = rq.patch(url, headers=headers, data=data_str)

    assert resp.status_code == 200
    resp = rq.get(url)
    assert json.loads(resp.text) == data_updated


@pytest.mark.parametrize("data", data)
def test_delete(cookie_auth, data):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    url = home_url + "/booking"
    data_str = str(json.dumps(data))
    resp = rq.post(url, headers=headers, data=data_str)
    assert resp.status_code == 200
    id = json.loads(resp.text)["bookingid"]

    cookie = cookie_auth
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Cookie"] = "token=" + cookie[0]
    url = home_url + "/booking/" + str(id)
    resp = rq.delete(url, headers=headers)
    assert resp.status_code == 201

    resp = rq.get(url)
    assert resp.status_code == 404
