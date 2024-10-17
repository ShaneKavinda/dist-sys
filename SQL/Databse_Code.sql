CREATE DATABASE PITR;
GO

USE PITR;
GO

-- create the table to store user data
CREATE TABLE Users (
	userId INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
	personId VARCHAR(10) NOT NULL,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(50),
	has_pid BIT
);
GO

INSERT INTO Users (personId,first_name,last_name,email, has_pid) VALUES('2212231V','Test', 'User','testuser@email.com',1);