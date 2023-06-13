DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Sensor;

CREATE TABLE IF NOT EXISTS Admin (
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE IF NOT EXISTS Company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    api_key TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Location (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    meta TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Company(id)
);

CREATE TABLE IF NOT EXISTS Sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    meta TEXT NOT NULL,
    api_key TEXT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES Location(id)
);

CREATE TABLE IF NOT EXISTS SensorData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    humedad FLOAT,
    temperatura FLOAT,
    fecha UNSIGNED BIG INT,
    luminosidad FLOAT,
    potencia_senal FLOAT,
    FOREIGN KEY (sensor_id) REFERENCES Sensor(id)
)