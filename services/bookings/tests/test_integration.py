import json
import pytest


def call(client, path, method='GET', body=None):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    if method == 'POST':
        response = client.post(path, data=json.dumps(body), headers=headers)
    elif method == 'PUT':
        response = client.put(path, data=json.dumps(body), headers=headers)
    elif method == 'PATCH':
        response = client.patch(path, data=json.dumps(body), headers=headers)
    elif method == 'DELETE':
        response = client.delete(path)
    else:
        response = client.get(path)

    return {
        "json": json.loads(response.data.decode('utf-8')),
        "code": response.status_code
    }


@pytest.mark.dependency()
def test_health(client):
    result = call(client, 'health')
    assert result['code'] == 200


@pytest.mark.dependency()
def test_get_all(client):
    result = call(client, 'bookings')
    assert result['code'] == 200
    assert result['json']['data']['bookings'] == [
        {
            "booking_id": 1,
            "customer_id": 1,
            "end_time": "Wed, 03 Nov 2021 00:00:00 GMT",
            "room_id": 1,
            "start_time": "Tue, 02 Nov 2021 00:00:00 GMT",
            "status": "COMPLETED",
            "time_created": "Wed, 27 Oct 2021 13:32:30 GMT",
            "time_updated": "Wed, 03 Nov 2021 00:00:00 GMT",
            "total_price": 100.0
        },
        {
            "booking_id": 2,
            "customer_id": 3,
            "end_time": "Sat, 27 Nov 2021 00:00:00 GMT",
            "room_id": 3,
            "start_time": "Sat, 27 Nov 2021 02:00:00 GMT",
            "status": "NEW",
            "time_created": "Tue, 02 Nov 2021 16:23:10 GMT",
            "time_updated": "Tue, 02 Nov 2021 16:23:10 GMT",
            "total_price": 200.0
        }
    ]


@pytest.mark.dependency(depends=['test_get_all'])
def test_one_valid(client):
    result = call(client, 'bookings/2')
    assert result['code'] == 200
    assert result['json']['data'] == {
        "booking_id": 2,
        "customer_id": 3,
        "end_time": "Sat, 27 Nov 2021 00:00:00 GMT",
        "room_id": 3,
        "start_time": "Sat, 27 Nov 2021 02:00:00 GMT",
        "status": "NEW",
        "time_created": "Tue, 02 Nov 2021 16:23:10 GMT",
        "time_updated": "Tue, 02 Nov 2021 16:23:10 GMT",
        "total_price": 200.0
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_one_invalid(client):
    result = call(client, 'bookings/55')
    assert result['code'] == 404
    assert result['json'] == {
        "message": "Booking not found."
    }


@pytest.mark.dependency(depends=['test_get_all'])
def test_update_existing_booking(client):
    result = call(client, 'bookings/2', 'PATCH', {
        "status": "CANCELLED"
    })
    assert result['code'] == 200
    assert result['json']['data']['status'] == "CANCELLED"


@pytest.mark.dependency(depends=['test_get_all'])
def test_create_no_body(client):
    result = call(client, 'bookings', 'POST', {})
    assert result['code'] == 500


@pytest.mark.dependency(depends=['test_get_all', 'test_create_no_body'])
def test_create_one_booking(client):
    result = call(client, 'bookings', 'POST', {
        "customer_id": 2,
        "end_time": "2021-11-28 00:00:00",
        "room_id": 2,
        "start_time": "2021-11-27 00:00:00",
        "total_price": 200.0
    })
    print(result['json'])
    assert result['code'] == 201
    assert result['json']['data']['customer_id'] == 2
    assert result['json']['data']['booking_id'] == 3
    assert result['json']['data']['status'] == "NEW"
    assert result['json']['data']['room_id'] == 2
    assert result['json']['data']['total_price'] == 200.0
    assert result['json']['data']['start_time'] == "Sat, 27 Nov 2021 00:00:00 GMT"
    assert result['json']['data']['end_time'] == "Sun, 28 Nov 2021 00:00:00 GMT"


@pytest.mark.dependency(depends=['test_get_all'])
def test_create_new_booking_fail(client):
    result = call(client, 'bookings', 'POST', {
        "customer_id": 6
    })
    assert result['code'] == 500


@pytest.mark.dependency(depends=['test_get_all'])
def test_update_existing_booking_fail(client):
    result = call(client, 'bookings/2', 'PATCH', {
        "status": None
    })
    assert result['code'] == 500


@pytest.mark.dependency(depends=['test_get_all'])
def test_update_nonexisting_booking(client):
    result = call(client, 'bookings/555', 'PATCH', {
        "status": "CANCELLED"
    })
    assert result['code'] == 404
