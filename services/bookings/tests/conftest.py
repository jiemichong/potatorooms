import pytest


@pytest.fixture
def client():
    from src import bookingapp

    bookingapp.app.config['TESTING'] = True

    bookingapp.db.engine.execute('''DROP TABLE IF EXISTS `booking`''')

    bookingapp.db.engine.execute('''CREATE TABLE `booking` (
  `booking_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `room_id` int NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `time_created` datetime NOT NULL,
  `time_updated` datetime NOT NULL,
  `total_price` float NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;''')

    bookingapp.db.engine.execute('''INSERT INTO `booking` VALUES
    (1, 1, 1, '2021-11-02 00:00:00', '2021-11-03 00:00:00', '2021-10-27 13:32:30',
'2021-11-03 00:00:00', 100.0, 'COMPLETED'),
(2, 3, 3, '2021-11-27 02:00:00', '2021-11-27 00:00:00', '2021-11-02 16:23:10',
'2021-11-02 16:23:10', 200.0, 'NEW');''')

    return bookingapp.app.test_client()
