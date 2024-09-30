CREATE DATABASE IF NOT EXISTS crypto_investment_db;
USE crypto_investment_db;
CREATE TABLE historical_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10),
    date DATE,
    open_price DECIMAL(10, 2),
    close_price DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    volume DECIMAL(20, 2)
);

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10),
    prediction_date DATE,
    predicted_close DECIMAL(10, 2)
);
