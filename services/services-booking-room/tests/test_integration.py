from unittest.mock import Mock
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

# def mock_stripe():
#     stripe_response_mock = Mock()
#     stripe_response_mock.status_code = 200
#     stripe_response_mock.json.return_value = {

#     }

def mock_get_customer_exist():
    customer_response = Mock()
    customer_response.status_code = 200
    customer_response.json.return_value = {
        "data": {
            "cust_id": 1,
            "cust_name": "potatoes",
            "cust_phone": 97443233,
            "cust_email": "potatoesops@gmail.com"
        }
    }


def mock_get_customer_new():
    customer_response = Mock()
    customer_response.status_code = 404
    customer_response.json.return_value = {
        "message": "Customer not found."
    }


def mock_create_customer_new():
    customer_response = Mock()
    customer_response.status_code = 200
    customer_response.json.return_value = {
        "data": {
            "cust_id": 1,
            "cust_name": "potatoes",
            "cust_phone": 97443233,
            "cust_email": "potatoesops@gmail.com"
        }
    }


def mock_get_room_price():
    room_service_response = Mock()
    room_service_response.status_code = 200
    room_service_response.json.return_value = {
        "data": 100.00
    }

def mock_get_room_price_invalid():
    room_service_response = Mock()
    room_service_response.status_code = 404
    room_service_response.json.return_value = {
        "message": "Meeting room not found."
    }


# booking with same date/timing with the one we posting
def mock_get_bookings_found_existing():
    booking_service_response = Mock()
    booking_service_response.status_code = 200
    booking_service_response.return_value = {
        "data" : {
            "bookings": {
                "booking_id": 1,
                "customer_id": 1,
                "end_time": "Wed, 03 Nov 2021 00:00:00 GMT",
                "room_id": 1,
                "start_time": "Tue, 02 Nov 2021 00:00:00 GMT", # change the time 
                "status": "NEW",
                "time_created": "Wed, 27 Oct 2021 13:32:30 GMT", 
                "time_updated": "Wed, 03 Nov 2021 00:00:00 GMT",
                "total_price": 100.0
            }
        }
    }


# no existing booking that match the one we trying to send
def mock_get_bookings_found_not_existing():
    booking_service_response = Mock()
    booking_service_response.status_code = 200
    booking_service_response.return_value = {
        "data" : {
            "bookings": {
                "booking_id": 1,
                "customer_id": 1,
                "end_time": "Wed, 03 Nov 2021 00:00:00 GMT",
                "room_id": 1,
                "start_time": "Tue, 02 Nov 2021 00:00:00 GMT",
                "status": "COMPLETED",
                "time_created": "Wed, 27 Oct 2021 13:32:30 GMT",
                "time_updated": "Wed, 03 Nov 2021 00:00:00 GMT",
                "total_price": 100.0
            }
        }
    }

def mock_get_bookings_notfound():
    booking_service_response = Mock()
    booking_service_response.status_code = 404
    booking_service_response.return_value = {
        "message": "There are no bookings."
    }


def mock_post_booking_ok():
    booking_service_response = Mock()
    booking_service_response.status_code = 201
    booking_service_response.return_value = {
            "data":  {
                "customer_id": 2,
                "booking_id": 3,
                "room_id": 2,
                "total_price": 200,
                "start_time": "Sat, 27 Nov 2021 00:00:00 GMT",
                "end_time": "Sun, 28 Nov 2021 00:00:00 GMT"
            }
        }


def mock_post_booking_not_ok():
    booking_service_response = Mock()
    booking_service_response.status_code = 500
    booking_service_response.return_value = {
            "message": "An error occurred creating the booking.",
            "error": "error in booking service"
        }


@pytest.mark.dependency()
def get_booking_rooms(client):
    result = call(client, 'booking_room', 'GET', {
        "customer_id": 2,
        "end_time": "2021-11-28 00:00:00",
        "room_id": 2,
        "start_time": "2021-11-27 00:00:00",
        "total_price": 200.0
    })
