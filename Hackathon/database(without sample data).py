import sqlite3

def setup_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('medication_program.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        FullName TEXT NOT NULL,
        Gender TEXT,
        EmergencyContact TEXT
    );
    ''')

    # Create AddictionHistory table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AddictionHistory (
        AddictionID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Substance TEXT,
        Duration TEXT,
        Status TEXT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
    ''')

    # Create HealthMetrics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS HealthMetrics (
        MetricID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        Age INTEGER,
        Weight REAL,
        Height REAL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
    ''')

    # Create MedicationRecords table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MedicationRecords (
        RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        MedicationName TEXT,
        Dosage TEXT,
        Frequency TEXT,
        StartDate DATE,
        EndDate DATE,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
