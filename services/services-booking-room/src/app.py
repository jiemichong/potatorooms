import os
import json
import requests
import amqp_setup
import pika
from dateutil import parser

from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

if os.environ.get('stage') == 'production':
    rooms_service_url = os.environ.get('rooms_service_url')
    customer_service_url = os.environ.get('customer_service_url')
    bookings_service_url = os.environ.get('bookings_service_url')
    stripe_service_url = os.environ.get('stripe_service_url')
    ui_service_url = os.environ.get('ui_service_url')
else:
    rooms_service_url = os.environ.get('rooms_service_url_internal')
    customer_service_url = os.environ.get('customer_service_url_internal')
    bookings_service_url = os.environ.get('bookings_service_url_internal')
    stripe_service_url = os.environ.get('stripe_service_url_internal')
    ui_service_url = os.environ.get('ui_service_url')

app = Flask(__name__)

CORS(app)
cors_config = {"origins": "*"}
cors = CORS(app, resources={r"/*]": cors_config})


@app.route("/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route("/booking_room", methods=['POST'])
def booking_room():

    data = request.get_json()
    print("##########################################")
    print(data)

    room_id = data['room_id']
    email = data['cust_email']

    # check if not existing customer & create if not
    response = requests.get(customer_service_url + '/customer/' + email)
    if response.status_code == 404:
        requests.post(customer_service_url + '/customer',
                      data=json.dumps({
                          "cust_email": email,
                          "cust_name": data["name"],
                          "cust_phone": data["phone"]
                      }),
                      headers={
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        })

    # look for room price
    response = requests.get(rooms_service_url +
                            '/rooms/' + str(room_id) + '/price').json()
    price = response['data']['price']

    # add the booking to the database
    # (1) Check if the room is available
    # check status for "NEW",
    # check if the specific room is occupied for the START date
    date = parser.parse(data['start_time']).date()
    edate = parser.parse(data['end_time']).date()
    print(room_id)
    print(type(room_id))
    response = requests.get(bookings_service_url + '/bookings').json()
    print("##########################################")
    print(response)
    for booking in response['data']['bookings']:
        status = booking['status']
        print("##########################################")
        print(booking['start_time'])
        print(type(booking['start_time']))
        booking_date = parser.parse(booking['start_time']).date()
        if (status == 'NEW' and date == booking_date
                and room_id == booking['room_id']):
            return jsonify(
                {
                    "message": "Room is unavailable on that day."
                }
            ), 409

    customer = requests.get(customer_service_url + '/customer/' + email).json()
    cust_id = customer['data']['cust_id']

    # (2) Create the booking
    booking_response = requests.post(
        bookings_service_url + '/bookings',
        data=json.dumps({
            "customer_id": cust_id,
            "end_time": edate.strftime("%Y-%m-%d %H:%M:%S"),
            "room_id": room_id,
            "start_time": date.strftime("%Y-%m-%d %H:%M:%S"),
            "total_price": price
        }),
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )

    if booking_response.status_code != 201:
        return jsonify(
            {
                "message": "Unable to create room booking.",
                "error": booking_response.json()
            }
        ), 500

    return jsonify(
        {
            "message": "Booking placed.",
            "data": booking_response.json()['data']
        }
    ), 200


@app.route("/delete_booking/<int:id>", methods=['GET'])
def delete_booking(id):
    print("test")
    print(id)
    # undo creation of booking
    requests.delete(bookings_service_url + "/bookings" + str(id))

    # undo notificationsbasicall
    return redirect(ui_service_url + "/paymentCancelled.html")


@app.route("/send_notification/<int:id>", methods=['GET'])
def send_notifications(id):
    booking_response = requests.get(
        bookings_service_url + '/bookings/' + str(id)).json()
    data = booking_response['data']

    customer = requests.get(customer_service_url +
                            '/customer/' + str(data['customer_id'])).json()
    email = customer['data']['cust_email']
    # (3) Send notification to the AMQP broker
    notification_data = {
            "email": email,
            "message": {
                "subject": "Booking Confirmation",
                "message": ("Your booking has been confirmed.\n"
                            "Booking Details: \n" +
                            "From: " + data['start_time'] + "\n"
                            "To: " + data['end_time'] + "\n"
                            "Room Id: " + str(data['room_id']) + "\n\n"
                            "Thank you.")}

    }

    connection = pika.BlockingConnection(amqp_setup.parameters)

    channel = connection.channel()

    channel.basic_publish(
        exchange=amqp_setup.exchange_name, routing_key="booking.new",
        body=json.dumps(notification_data),
        properties=pika.BasicProperties(delivery_mode=2))

    connection.close()

    return redirect(ui_service_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
