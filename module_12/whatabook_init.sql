/*
    Title: whatabook_init.sql
    Author: Ryan Kite
    Date: 13 December 2021
    Description: whatabook database initialization script.
    For: CSD310 Module 12 capstone project
*/

-- drop whatabook database if it exists
DROP DATABASE IF EXISTS whatabook;

-- create whatabook database if it does not exist
CREATE DATABASE IF NOT EXISTS whatabook;

-- drop test user if exists 
DROP USER IF EXISTS 'whatabook_user'@'localhost';

-- create whatabook_user and grant them all privileges to the whatabook database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the whatabook database to user whatabook_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';

-- use whatabook database
use whatabook;

-- drop tables if they are present
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS wishlist;

-- create the book table 
CREATE TABLE `book` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `book_name` varchar(200) NOT NULL,
  `details` varchar(500) NOT NULL,
  `author` varchar(200) NOT NULL,
  `store_id` int DEFAULT '1',
  PRIMARY KEY (`book_id`)
);

-- create table store
CREATE TABLE `store` (
  `store_id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(500) NOT NULL,
  `location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`store_id`)
);

-- create the user table
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(75) NOT NULL,
  `last_name` varchar(75) NOT NULL,
  PRIMARY KEY (`user_id`)
);

-- create the wishlist table
CREATE TABLE `wishlist` (
  `wishlist_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  PRIMARY KEY (`wishlist_id`),
  KEY `user_id` (`user_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`book_id`)
);

-- insert book records
INSERT INTO `book` 
    VALUES (1,'The Hobbit: or There and Back Again','Part of the The Lord of the Rings Series','J.R.R. Tolkien',1),(2,'The Lord Of The Rings - The Fellowship Of The Ring','Book #1 in the The Lord of the Rings Series','J.R.R. Tolkien',1),(3,'Lord Of The Rings: The Two Towers','Book #2 in the The Lord of the Rings Series','J.R.R. Tolkien',1),(4,'The Silmarillion','The three Silmarils were jewels created by Fanor','J.R.R. Tolkien',1),(5,'The Return of the King','Book #3 in the The Lord of the Rings Series','J.R.R. Tolkien',1),(6,'The Lord of the Rings','Part of the The Lord of the Rings Series','J.R.R. Tolkien',1),(7,'The Fall of Gondolin','Part of the Tales of Middle Earth Series','J.R.R. Tolkien',1),(8,'The Legend of Sigurd and Gudrun','the great legend of Northern antiquity','J.R.R. Tolkien',1),(9,'The Book of Lost Tales Part I & Part II','The glorious history of how Middle-earth','J.R.R. Tolkien',1);

-- insert store records 
INSERT INTO `store` 
    VALUES (1,'1024 Pike Street, Seattle, WA 98024','Seattle'),(2,'1005 W Burnside St, Portland, OR 97209','Portland');

-- insert user records 
INSERT INTO `user` 
    VALUES (1,'Ryan','Kite'),(2,'Gabriel','Kite'),(3,'Aila','Kite');

-- insert wishlist records 
INSERT INTO `wishlist` 
    VALUES (7,3,7),(8,2,1),(24,1,1);

