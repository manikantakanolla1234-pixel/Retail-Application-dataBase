create database online_Retil_Application;
use online_Retil_Application;

CREATE TABLE Customers(
CustomerID INT AUTO_INCREMENT PRIMARY KEY,
FullName VARCHAR(100),
Email VARCHAR(100) UNIQUE,
Password VARCHAR(100),
Phone VARCHAR(15),
Address VARCHAR(255)
);


CREATE TABLE Categories(
CategoryID INT AUTO_INCREMENT PRIMARY KEY,
CategoryName VARCHAR(50)
);

INSERT INTO Categories(CategoryName)

VALUES

('Electronics'),
('Mobiles'),
('Fashion'),
('Home'),
('Books');

CREATE TABLE Products(
ProductID INT AUTO_INCREMENT PRIMARY KEY,
CategoryID INT,
ProductName VARCHAR(100),
Description VARCHAR(255),
Price DECIMAL(10,2),
Stock INT,
Image VARCHAR(500),
FOREIGN KEY(CategoryID)
REFERENCES Categories(CategoryID)
);
DROP TABLE IF EXISTS Cart;
CREATE TABLE Cart(
CartID INT AUTO_INCREMENT PRIMARY KEY,
UserID INT,
ProductID INT,
Quantity INT DEFAULT 1,
FOREIGN KEY(UserID)REFERENCES Users(UserID)ON DELETE CASCADE,
FOREIGN KEY(ProductID)REFERENCES Products(ProductID)ON DELETE CASCADE
);


CREATE TABLE Orders(
OrderID INT AUTO_INCREMENT PRIMARY KEY,
CustomerID INT,
TotalAmount DECIMAL(10,2),
FOREIGN KEY(CustomerID)
REFERENCES Customers(CustomerID)
);
CREATE TABLE OrderDetails (
    OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    Price DECIMAL(10,2)
);
DESCRIBE OrderDetails;
CREATE TABLE Payments(
PaymentID INT AUTO_INCREMENT PRIMARY KEY,
OrderID INT,
Amount DECIMAL(10,2),
PaymentMethod VARCHAR(50),
FOREIGN KEY(OrderID)
REFERENCES Orders(OrderID)
);

select *from customers;


CREATE TABLE Users(
UserID INT AUTO_INCREMENT PRIMARY KEY,
Name VARCHAR(100),
Email VARCHAR(100) UNIQUE,
Password VARCHAR(100),
Phone VARCHAR(15),
Address VARCHAR(255)
);


INSERT INTO Products
(CategoryID,ProductName,Description,Price,Stock,Image)
VALUES

(1,'Laptop',
'HP Laptop',
55000,
20,
'https://images.unsplash.com/photo-1496181133206-80ce9b88a853'),


(2,'iPhone',
'Apple Smartphone',
70000,
15,
'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9'),


(3,'Shoes',
'Nike Shoes',
5000,
30,
'https://images.unsplash.com/photo-1542291026-7eec264c27ff'),


(4,'Sofa',
'Home Furniture',
25000,
10,
'https://images.unsplash.com/photo-1555041469-a586c61ea9bc');


INSERT INTO Products
(CategoryID,ProductName,Description,Price,Stock,Image)
VALUES

(1,
'HP Laptop',
'Intel i5 Laptop',
55000,
20,
'https://images.unsplash.com/photo-1496181133206-80ce9b88a853'),


(1,
'Dell Monitor',
'24 inch Display',
15000,
30,
'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf'),


(2,
'iPhone 15',
'Apple Smartphone',
70000,
15,
'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9'),


(2,
'Samsung Galaxy',
'Android Smartphone',
45000,
25,
'https://images.unsplash.com/photo-1598327105666-5b89351aff97'),


(3,
'Nike Shoes',
'Sports Shoes',
5000,
40,
'https://images.unsplash.com/photo-1542291026-7eec264c27ff'),


(3,
'Mens Jacket',
'Winter Jacket',
3500,
50,
'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3'),


(4,
'Sofa Set',
'Living Room Sofa',
30000,
10,
'https://images.unsplash.com/photo-1555041469-a586c61ea9bc'),


(5,
'Python Book',
'Programming Book',
800,
100,
'https://images.unsplash.com/photo-1532012197267-da84d127e765');
DESCRIBE OrderDetails;
show tables;
SELECT * FROM Orders;
SELECT * FROM OrderDetails;
SELECT * FROM Payments;