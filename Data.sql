/*This is the database queries File that has to be always active like creating the table or merging it*/

CREATE TABLE IF NOT EXISTS Users_Data (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(30),
    Password TEXT,
    Passkey_Choice TEXT,
    Passkey TEXT
);

CREATE TABLE IF NOT EXISTS Articles_Data (
    ID_Article INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID INTEGER,
    Article_Name VARCHAR(30),
    Article_Body TEXT,
    Article_Date DATE,
    FOREIGN KEY (User_ID) REFERENCES (Users_Data.ID)
);