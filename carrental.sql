CREATE DATABASE IF NOT EXISTS projectDB;
USE projectDB;
drop table Reservations;

CREATE TABLE Reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    car_type ENUM('sedan', 'SUV', 'pickup', 'van') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    charge DECIMAL(10, 2) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
