-- setup database for development use MySQL
-- create database for project development 'hbnb_dev_db'
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- create user for development 'hbnb_dev'
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- grant privileges to user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
-- grant SELECT privileges on perfomance_schema for hbnb_dev_db
GRANT SELECT ON perfomance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
