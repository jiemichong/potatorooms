import pytest
from werkzeug.utils import append_slash_redirect

@pytest.fixture
def client():
    from src import app

    app.app.config['TESTING'] = True

    #############################
    # Reset Booking Table
    #############################

    app.db.engine.execute('''DROP TABLE IF EXISTS `booking`''')

    app.db.engine.execute('''CREATE TABLE `booking` (
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

    app.db.engine.execute('''INSERT INTO `booking` VALUES
    (1, 1, 1, '2021-11-02 00:00:00', '2021-11-03 00:00:00', '2021-10-27 13:32:30',
    '2021-11-03 00:00:00', 100.0, 'COMPLETED'),
    (2, 3, 3, '2021-11-27 02:00:00', '2021-11-27 00:00:00', '2021-11-02 16:23:10',
    '2021-11-02 16:23:10', 200.0, 'NEW');''')

    #############################
    # Reset Customer Table
    #############################
    app.db.engine.execute('DROP TABLE IF EXISTS `customer`;')

    app.db.engine.execute('''CREATE TABLE `customer` (
                          `cust_id` int NOT NULL AUTO_INCREMENT,
                          `cust_name` varchar(225) NOT NULL,
                          `cust_phone` int NOT NULL,
                          `cust_email` varchar(225) NOT NULL,
                          UNIQUE (cust_email),
                          PRIMARY KEY (`cust_id`)
                          ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;''')

    app.db.engine.execute(
        '''INSERT INTO `customer` VALUES
        (1,'Carmen Yip',98765432,'carmenyip@abc.com'),
        (2,'Nikki Poo',97654321,'nikkipoo@abc.com'),
        (3,'Jie Mi',96543218,'jiemi@abc.com');''')

    #############################
    # Reset Meeting Rooms Table
    #############################
    app.db.engine.execute('DROP TABLE IF EXISTS `rooms`;')

    app.db.engine.execute('''CREATE TABLE `rooms` (
                          `room_id` int NOT NULL AUTO_INCREMENT,
                          `capacity` int NOT NULL,
                          `price` float NOT NULL,
                          `floor` int NOT NULL,
                          PRIMARY KEY (`room_id`)
                          ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;''')

    app.db.engine.execute(
                          '''INSERT INTO `rooms` VALUES
                          (1,5,100.0,1),
                          (2,20,200.0,1),
                          (3,20,200.0,2),
                          (4,50,300.0,1),
                          (5,5,100.0,4);''')

    #############################
    # Reset Notifications Table
    #############################
    app.db.engine.execute('DROP TABLE IF EXISTS `notification`;')
    app.db.engine.execute('''CREATE TABLE `notification` (
                          `notification_id` int NOT NULL AUTO_INCREMENT,
                          `email` varchar(64) NOT NULL,
                          `message` mediumtext NOT NULL,
                          PRIMARY KEY (`notification_id`)
                          ) ENGINE=InnoDB AUTO_INCREMENT=1
                          DEFAULT CHARSET=utf8;''')

    return app.app.test_client()
