CREATE TABLE map (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  map_name VARCHAR(50),
  r1slat VARCHAR(50),
  r1slon VARCHAR(50),
  r1elat VARCHAR(50),
  r1elon VARCHAR(50),
  r2slat VARCHAR(50),
  r2slon VARCHAR(50),
  r2elat VARCHAR(50),
  r2elon VARCHAR(50),
  r3slat VARCHAR(50),
  r3slon VARCHAR(50),
  r3elat VARCHAR(50),
  r3elon VARCHAR(50),
  record_state enum('Active', 'Inactive', 'Deleted', 'Other', 'Reserved') NOT NULL DEFAULT 'Active',
  last_updated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_map (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  map_id INT,
  user_id INT,
  user_lat VARCHAR(50),
  user_lon VARCHAR(50),
  record_state enum('Active', 'Inactive', 'Deleted', 'Other', 'Reserved') NOT NULL DEFAULT 'Active',
  last_updated TIMESTAMP DEFAULT NOW() 
);

CREATE TABLE detonation_q (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  map_id INT,
  sender_id INT,
  recipient_id INT,
  bomb_lat VARCHAR(50),
  bomb_lon VARCHAR(50),
  record_state enum('Active', 'Inactive', 'Deleted', 'Other', 'Reserved') NOT NULL DEFAULT 'Active',
  last_updated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE kills (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  map_id INT,
  sender_id INT,
  recipient_id INT,
  bomb_lat VARCHAR(50),
  bomb_lon VARCHAR(50),
  record_state enum('Active', 'Inactive', 'Deleted', 'Other', 'Reserved') NOT NULL DEFAULT 'Active',
  last_updated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE kills_history (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  map_id INT,
  sender_id INT,
  recipient_id INT,
  bomb_lat VARCHAR(50),
  bomb_lon VARCHAR(50),
  record_state enum('Active', 'Inactive', 'Deleted', 'Other', 'Reserved') NOT NULL DEFAULT 'Active',
  last_updated TIMESTAMP DEFAULT NOW()
);



