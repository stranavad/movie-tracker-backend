# Codes for communication between frontend and backend

### 0x - Init

#### 01 - MySQL
Cant estabilish connection to MySQL server


### 10x Movies Get

#### 101 - ERROR - Show tables
Problem getting tables for seeing if user is in database

#### 102 - ERROR - SELECT data from user table
Cant select data from user table

#### 103 - no movies
There are no movies inside user table

#### 104 - OK
Return is fine

#### 105 - ERROR - cannot create table
Can't create new table for user who doesn't have any movies yet

#### 106 - Table created
Table for user without movies has been created successfully


### 11x Movies Post

#### 111 - ERROR - Cant INSERT
Cannot insert movie into user table

#### 112 - OK
Data was pushed to the table
