-- Prepares MySQL server for the project

CREATE DATABASE IF NOT EXIST hbnb_dev_db;
CREATE USER IF NOT EXIST hbnb_dev@localhost IDENTIFIED by 'hbnb_dev_pwd';
USE hbnb_dev_db;
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
USE performance_schema;
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
