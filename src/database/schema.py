-- Heart rate readings table
CREATE TABLE heart_rate_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    heart_rate INTEGER NOT NULL,
    raw_flags INTEGER,
    session_id INTEGER,
    FOREIGN KEY (session_id) REFERENCES gaming_sessions(id)
);

-- Gaming sessions table
CREATE TABLE gaming_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT NOT NULL,
    end_time TEXT,
    game_name TEXT,
    notes TEXT
);

-- Create index for faster queries
CREATE INDEX idx_hr_timestamp ON heart_rate_readings(timestamp);
CREATE INDEX idx_hr_session ON heart_rate_readings(session_id);