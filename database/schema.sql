CREATE DATABASE IF NOT EXISTS flight_db;
USE flight_db;

CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255)
);

CREATE TABLE airlines (
  airline_id INT PRIMARY KEY AUTO_INCREMENT,
  airline_name VARCHAR(100),
  rating FLOAT,
  logo_path VARCHAR(100)
);

CREATE TABLE flights (
  flight_id INT PRIMARY KEY AUTO_INCREMENT,
  airline_id INT,
  route VARCHAR(100),
  stops INT,
  base_price FLOAT,
  booking_url VARCHAR(255),
  FOREIGN KEY (airline_id) REFERENCES airlines(airline_id)
);

CREATE TABLE booking_clicks (
  click_id INT PRIMARY KEY AUTO_INCREMENT,
  flight_id INT,
  click_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);