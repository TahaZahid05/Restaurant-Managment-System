drop TABLE Order_Menu
drop TABLE Feedback
drop TABLE Orders
drop TABLE MenuItem
drop TABLE [Transaction]
drop TABLE Ingredients
drop TABLE Inventory
drop TABLE Staff
drop TABLE Reservations
drop TABLE Customer_Address
drop TABLE Customer
drop TABLE Restaurant
-- Table: Restaurant
CREATE TABLE Restaurant (
    id INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(255) NOT NULL,
    Address VARCHAR(255) NOT NULL
);

-- Table: Customer
CREATE TABLE Customer (
    id INT PRIMARY KEY IDENTITY(1,1),
    Restaurant_id INT FOREIGN KEY REFERENCES Restaurant(id),
    First_name VARCHAR(255) NOT NULL,
    Last_name VARCHAR(255),
    Email VARCHAR(255),
    username VARCHAR(255) ,
    [password] VARCHAR(255),
    Phone_number VARCHAR(15)
);

CREATE TABLE Customer_Address(
	Address VARCHAR(255),
	id INT,
	FOREIGN KEY (id) REFERENCES Customer(id),
	PRIMARY KEY(id, Address)
);

-- Table: Reservations
CREATE TABLE Reservations (

    id INT IDENTITY(1,1),
    CustomerID INT NOT NULL,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Party_size INT NOT NULL,
    Status VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customer(id),
	PRIMARY KEY (id, CustomerID)
);

-- Table: Staff
CREATE TABLE Staff (
    id INT PRIMARY KEY IDENTITY(1,1),
    RestaurantID INT FOREIGN KEY REFERENCES Restaurant(id),
    Full_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    Phone_Number VARCHAR(15),
    Position VARCHAR(50),
    Salary INT,
	Joining_Date DATE NOT NULL,
    Emergency_Contact VARCHAR(15) NOT NULL,
    Status VARCHAR(50) NOT NULL,
	ownerID INT,
	FOREIGN KEY (ownerID) REFERENCES Staff(id)
);

-- Updated Table: Inventory
CREATE TABLE Inventory (
    id INT PRIMARY KEY IDENTITY(1,1),
    RestaurantID INT FOREIGN KEY REFERENCES Restaurant(id)
);

-- New Table: Ingredients
CREATE TABLE Ingredients (
    id INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(255) NOT NULL,
    InventoryID INT FOREIGN KEY REFERENCES Inventory(id),
	Company varchar(255) not null,
    Cost INT NOT NULL,
    Last_Updated DATE NOT NULL,
	Stock int not null,
	CheckerStaffID int foreign key references staff(id)
);

-- Table: Transaction
CREATE TABLE [Transaction] (
    id INT PRIMARY KEY IDENTITY(1,1),
    InventoryID INT FOREIGN KEY REFERENCES Inventory(id),
    StaffID INT FOREIGN KEY REFERENCES Staff(id),
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Type VARCHAR(50) NOT NULL,
	PaymentType VARCHAR(50),
	Tax float NOT NULL,
    Amount INT NOT NULL
);

-- Table: MenuItem
CREATE TABLE MenuItem (
    ID INT PRIMARY KEY IDENTITY(1,1),
    StaffID INT FOREIGN KEY REFERENCES Staff(id),
    Name VARCHAR(255) NOT NULL,
    Category VARCHAR(50) NOT NULL,
	Description VARCHAR(255),
    Price INT NOT NULL,
	Discontinued bit NOT NULL
);

-- Table: Orders
CREATE TABLE Orders (
    id INT PRIMARY KEY IDENTITY(1,1),
    StaffID INT FOREIGN KEY REFERENCES Staff(id),
	TransactionID INT FOREIGN KEY REFERENCES [Transaction](id),
    CustomerID INT,
	CustomerAddress VARCHAR(255),
    Table_no INT,
    Special_Request VARCHAR(255),
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Status VARCHAR(50),
	FOREIGN KEY (CustomerID) REFERENCES Customer(id)
);

-- Table: Feedback
CREATE TABLE Feedback (
    id INT IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(id),
    Rating FLOAT NOT NULL,
	PRIMARY KEY (id, OrderID)
);

-- Table: Order_Menu
CREATE TABLE Order_Menu (
    Order_ID INT FOREIGN KEY REFERENCES Orders(id),
    Item_ID INT FOREIGN KEY REFERENCES MenuItem(ID),
	Quantity INT NOT NULL,
    PRIMARY KEY (Order_ID, Item_ID) -- Composite Primary Key
);

--------EXECUTE THE FOLLOWING AFTER EXECUTING THE CREATE QUERIES--------

-- Populate Restaurant table
INSERT INTO Restaurant (Name, Address)
VALUES 
('Highly Systematic Resturant', 'Habib University, Karachi');

-- Populate Customer table
INSERT INTO Customer (Restaurant_id, First_name, Last_name, Email, username, password, Phone_number)
VALUES
(1, 'John', 'Doe', 'johndoe@gmail.com', 'john_d', 'pass123', '1234567890'),
(1, 'Jane', 'Smith', 'janesmith@yahoo.com', 'jane_s', 'pass456', '0987654321'),
(1, 'Mike', 'Brown', 'mikebrown@hotmail.com', 'mike_b', 'pass789', '5678901234'),
(1, 'Alice', 'White', 'alicewhite@gmail.com', 'alice_w', 'pass101', '2345678901'),
(1, 'Bob', 'Green', 'bobgreen@outlook.com', 'bob_g', 'pass202', '3456789012'),
(1, 'Taha', 'Zahid', 'tahazahid1@gmail.com', 'tahazahid', 'tahazahid123', '123-456-7890'),
(1, 'Abdullah', 'Shaikh', 'abdullahshaikh1@gmail.com', 'abdullahshaikh', 'abdullahshaikh123', '123-456-7890');

INSERT INTO Customer_Address (id, Address)
VALUES
(1, '123 Main St'),
(2, '456 Elm St'),
(3, '789 Oak St'),
(4, '101 Maple St'),
(5, '202 Pine St'),
(6, 'Saddar, Karachi'),
(7, 'Continetal Bakery, Karachi');

-- Populate Reservations table
INSERT INTO Reservations (CustomerID, Date, Time, Party_size, Status)
VALUES
(1, '2024-11-10', '18:00:00', 4, 'Confirmed'),
(2, '2024-11-11', '19:00:00', 2, 'Pending'),
(3, '2024-11-12', '20:00:00', 5, 'Confirmed'),
(4, '2024-11-13', '18:30:00', 3, 'Cancelled'),
(5, '2024-11-14', '19:30:00', 6, 'Confirmed');

-- Populate Staff table
INSERT INTO Staff (RestaurantID, Full_Name, Last_Name, Email, username, Password, Phone_Number, Position, Salary, Joining_Date, Emergency_Contact, Status,ownerID)
VALUES
(1, 'Emma', 'Watson', 'emma.watson@gmail.com', 'emma_w', 'staff123', '1239874560', 'Chef', 50000, '2020-01-15', '9998887770', 'Working',5),
(1, 'Liam', 'Johnson', 'liam.johnson@yahoo.com', 'liam_j', 'staff456', '4567891230', 'Waiter', 30000, '2021-05-20', '8887776660', 'Working',5),
(1, 'Olivia', 'Davis', 'olivia.davis@hotmail.com', 'olivia_d', 'staff789', '7894561230', 'Waiter', 30000, '2022-03-01', '7776665550', 'On Leave',5),
(1, 'Noah', 'Miller', 'noah.miller@gmail.com', 'noah_m', 'staff101', '1236547890', 'Cleaner', 25000, '2019-08-12', '6665554440', 'Working',5),
(1, 'Ayaan', 'Merchant', 'ayaanmerchant1@gmail.com', 'ayaanmerchant', 'ayaanmerchant123', '123-456-7890', 'CEO', 300000, '2015-11-05', '4443332220', 'Working',NULL);

-- Populate Inventory table
INSERT INTO Inventory (RestaurantID)
VALUES
(1);

-- Populate Ingredients table
INSERT INTO Ingredients (Name, InventoryID, Company, Cost, Last_Updated, Stock, checkerstaffid)
VALUES
('Tomatoes', 1,'Companyone', 50, '2024-10-30',6,2),
('Cheese', 1,'Companytwo', 200, '2024-10-31',7,3),
('Chicken', 1,'Companythree', 300, '2024-11-01',5,2),
('Beef', 1,'Companyfour',  500,'2024-11-02',4,3),
('Lettuce', 1,'Companyfive', 30, '2024-11-03',9,1);

-- Populate Transaction table
INSERT INTO [Transaction] (InventoryID, StaffID, Date, Time, Type, PaymentType, Tax, Amount)
VALUES
(1, 1, '2024-11-01', '10:00:00', 'Purchase', 'Card', 15, 1000),
(1, 2, '2024-11-02', '11:00:00', 'Refund', 'Cash', 15, 200),
(1, 3, '2024-11-03', '12:00:00', 'Purchase', 'Cash', 15, 300),
(1, 4, '2024-11-04', '13:00:00', 'Purchase', 'Cash', 15, 400),
(1, 5, '2024-11-05', '14:00:00', 'Refund', 'Cash', 15, 500);

-- Populate MenuItem table
INSERT INTO MenuItem (StaffID, Name, Category, Description, Price, Discontinued)
VALUES
(1, 'Burger', 'Main Course', 'A juicy, flavorful patty served in a soft, toasted bun, topped with fresh lettuce, ripe tomatoes, and your choice of sauces. A classic delight for any time of day!',  150, 0),
(2, 'Pasta', 'Main Course', 'Perfectly cooked pasta tossed in a rich, savory sauce, with a blend of herbs and spices. Served with a sprinkle of Parmesan for a comforting, indulgent meal.', 200, 0),
(3, 'Salad', 'Starter', 'A refreshing mix of crisp greens, vibrant veggies, and a tangy dressing. Light, healthy, and bursting with natural flavors.' ,100, 0),
(4, 'Soup', 'Starter', 'Warm, hearty, and comforting, our soup is crafted with fresh ingredients and simmered to perfection for a delightful, savory experience.' ,120, 0),
(5, 'Ice Cream', 'Dessert', 'Creamy, rich, and irresistibly smooth, our ice cream is available in a variety of flavors to satisfy your sweet cravings.' , 80, 0);

-- Populate Orders table
INSERT INTO Orders (StaffID, TransactionID, CustomerID, CustomerAddress, Table_no, Special_Request, Date, Time, Status)
VALUES
(1, 1, 1, '123 Main St', 10 , 'No onions', '2024-11-10', '18:45:00', 'Served'),
(2, 2, 2, '456 Elm St' , 12 ,'Extra spicy', '2024-11-11', '19:20:00', 'Preparing'),
(3, 3, 3, '789 Oak St' , 15 , 'Gluten-free', '2024-11-12', '20:10:00', 'Served'),
(4, 4, 4, '101 Maple St' , 8 , 'Less salt', '2024-11-13', '18:50:00', 'Cancelled'),
(5, 5, 5, '202 Pine St' , 20 , 'Extra cheese', '2024-11-14', '19:30:00', 'Served');

INSERT INTO Feedback (OrderID, Rating)
VALUES
(1, 4.5),
(2, 3.8),
(3, 4.9),
(4, 2.5),
(5, 5.0);

-- Populate Order_Menu table
INSERT INTO Order_Menu (Order_ID, Item_ID, Quantity)
VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 3),
(4, 4, 1),
(5, 5, 2);