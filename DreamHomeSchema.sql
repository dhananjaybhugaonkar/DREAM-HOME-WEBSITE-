/*
Griffin Davies
Group with Dhananjay(G), Igri, Griffin
*/
CREATE DATABASE DreamHome;
USE DreamHome;
-- Branch  (*branchNo, street, city, postcode)
CREATE TABLE Branch (
  branchNo varchar(255),
  street varchar(255),
  city varchar(255),
  postcode varchar(255),
  PRIMARY KEY (branchNo));

-- Staff (*staffNo, fName, lName, position, sex, DOB, salary, &branchNo)
CREATE TABLE Staff (
  staffNo varchar(5),
  fName varchar(255),
  lName varchar(255),
  position varchar(255),
  sex char,
  DOB date,
  salary int,
  branchNo varchar(4),
  Telephone varchar(255),
  Mobile varchar(255),
  Email varchar(255),
  PRIMARY KEY (staffNo),
  FOREIGN KEY (branchNo) REFERENCES Branch(branchNo));
  
-- PropertyForRent (*propertyNo, street, city, postcode, type, rooms, rent, &ownerNo, &staffNo, &branchNo)
CREATE TABLE PropertyForRent (
  propertyNo varchar(4),
  street varchar(255),
  city varchar(255),
  postcode varchar(255),
  propertyType varchar(255),
  rooms int,
  rent int,
  ownerNo varchar(4),
  staffNo varchar(4),
  branchNo varchar(4),
  picture varchar(255),
  floorPlan varchar(255),
  PRIMARY KEY (propertyNo),
  FOREIGN KEY (staffNo) REFERENCES Staff(staffNo),
  FOREIGN KEY (branchNo) REFERENCES Branch(branchNo));
  
-- Client (*clientNo, fName, lName, telNo, prefType, maxRent, eMail)
CREATE TABLE Client (
  ID int AUTO_INCREMENT,
  clientNo varchar(4),
  fName varchar(255),
  lName varchar(255),
  telNo varchar(18),
  street varchar(255),
  city varchar(255),
  postCode varchar(10),
  email varchar(255),
  JoinedOn varchar(255),
  Region varchar(255),
  preType varchar(255),
  maxRent float,
  PRIMARY KEY (ID));

-- Viewing (&clientNo, &propertyNo, viewDate, comment)
CREATE TABLE Viewing (
ID int NOT NULL AUTO_INCREMENT,
clientNo int,
propertyNo varchar(4),
viewDate date,
viewHour time,
comment varchar(255),
WishToRent bool,
PRIMARY KEY(ID),
foreign key(clientNo) REFERENCES Client(ID),
foreign key (propertyNo) REFERENCES PropertyForRent(propertyNo));