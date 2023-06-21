-- setup database for development use MySQL
-- create database for project development 'hbnb_test_db'
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- create user for development 'hbnb_test'
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- grant privileges to user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
-- grant SELECT privileges on perfomance_schema for hbnb_test_db
GRANT SELECT ON perfomance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
