CREATE DATABASE IF NOT EXISTS `rooms` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `rooms`;

DROP TABLE IF EXISTS `rooms`;

CREATE TABLE `rooms` (
  `room_id` int NOT NULL AUTO_INCREMENT,
  `capacity` int NOT NULL,
  `price` float NOT NULL,
  `floor` int NOT NULL,
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

INSERT INTO `rooms` VALUES (1,5,100.0,1),(2,20,200.0,1),(3,20,200.0,2),(4,50,300.0,1),(5,5,100.0,4);

CREATE DATABASE IF NOT EXISTS `customer` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `customer`;

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `cust_id` int NOT NULL AUTO_INCREMENT,
  `cust_name` varchar(225) NOT NULL,
  `cust_phone` int NOT NULL,
  `cust_email` varchar(225) NOT NULL,
  PRIMARY KEY (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

INSERT INTO `customer` VALUES (1,'Carmen Yip',98765432,'carmenyip@abc.com'),(2,'Nikki Poo',97654321,'nikkipoo@abc.com'),(3,'Jie Mi',96543218,'jiemi@abc.com');

CREATE DATABASE IF NOT EXISTS `booking` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `booking`;

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

INSERT INTO `booking` VALUES (1, 1, 1, '2021-11-02 00:00:00', '2021-11-03 00:00:00', '2021-10-27 13:32:30',
'2021-11-03 00:00:00', 100.0, 'COMPLETED'),
(2, 3, 3, '2021-11-27 02:00:00', '2021-11-27 00:00:00', '2021-11-02 16:23:10',
'2021-11-02 16:23:10', 200.0, 'NEW');

CREATE DATABASE IF NOT EXISTS `notification` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `notification`;

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `notification_id` int NOT NULL,
  `email` varchar(64) NOT NULL,
  `message` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `notification`
  ADD PRIMARY KEY (`notification_id`);

  ALTER TABLE `notification`
  MODIFY `notification_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
