import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
if os.environ.get('db_conn'):
    uri = os.environ.get('db_conn') + '/booking'
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = None
# uri = 'mysql+mysqlconnector://cs302:cs302@host.docker.internal:3306/booking'
# app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)


class Booking(db.Model):
    __tablename__ = 'booking'

    booking_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    time_updated = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "customer_id": self.customer_id,
            "room_id": self.room_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "time_created": self.time_created,
            "time_updated": self.time_updated,
            "total_price": self.total_price,
            "status": self.status
        }


@app.route("/health")
def health_check():
    return jsonify(
            {
                "message": "Bookings service is healthy."
            }
    ), 200


@app.route("/bookings")
def get_all():
    booking_list = Booking.query.all()
    if len(booking_list) != 0:
        return jsonify(
            {
                "data": {
                    "bookings": [booking.to_dict() for booking in booking_list]
                }
            }
        ), 200
    return jsonify(
        {
            "message": "There are no bookings."
        }
    ), 404


@app.route("/bookings/<int:booking_id>")
def find_by_id(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if booking:
        return jsonify(
            {
                "data": booking.to_dict()
            }
        ), 200
    return jsonify(
        {
            "message": "Booking not found."
        }
    ), 404


@app.route("/bookings", methods=['POST'])
def new_booking():
    try:
        data = request.get_json()
        customer_id = request.json.get('customer_id')
        room_id = request.json.get('room_id')
        start_time = request.json.get('start_time')
        end_time = request.json.get('end_time')
        total_price = request.json.get('total_price')
        booking = Booking(customer_id=customer_id, room_id=room_id,
                          start_time=start_time, end_time=end_time,
                          time_created=datetime.now(),
                          time_updated=datetime.now(),
                          total_price=total_price, status='NEW')

        db.session.add(booking)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating the booking.",
                "test": data,
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "data": booking.to_dict()
        }
    ), 201


@app.route("/bookings/<int:booking_id>", methods=['PATCH'])
def update_booking(booking_id):
    booking = Booking.query.with_for_update(of=Booking)\
                 .filter_by(booking_id=booking_id).first()
    if booking is not None:
        data = request.get_json()
        if 'status' in data.keys():
            accept = ["CANCELLED", "NEW", "COMPLETED"]
            if (data['status'] in accept):
                booking.status = data['status']
                booking.time_modified = datetime.now()
            else:
                return jsonify(
                    {
                        "message": "Not an applicable status."
                    }
                ), 500
        try:
            db.session.commit()
        except Exception as e:
            return jsonify(
                {
                    "message": "An error occurred updating the booking.",
                    "error": str(e)
                }
            ), 500
        return jsonify(
            {
                "data": booking.to_dict()
            }
        )
    return jsonify(
        {
            "data": {
                "booking_id": booking_id
            },
            "message": "Booking not found."
        }
    ), 404


@app.route("/bookings/<int:booking_id>", methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    if booking is not None:
        try:
            db.session.delete(booking)
            db.session.commit()
        except Exception as e:
            return jsonify(
                {
                    "message": "An error occurred deleting the booking.",
                    "error": str(e)
                }
            ), 500
        return jsonify(
            {
                "data": {
                    "booking_id": booking_id
                }
            }
        ), 200
    return jsonify(
        {
            "data": {
                "booking_id": booking_id
            },
            "message": "Booking not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
