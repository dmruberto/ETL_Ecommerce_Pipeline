USE ecommerce_data;

CREATE TABLE cleaned_sales (
    Invoice VARCHAR(50),
    StockCode VARCHAR(50),
    Description TEXT,
    Quantity INT,
    InvoiceDate DATETIME,
    Price DECIMAL(10, 2),
    CustomerID INT,
    Country VARCHAR(50),
    TotalPrice DECIMAL(10, 2),
    YearMonth VARCHAR(7),
    ProductCategory VARCHAR(50)
);
