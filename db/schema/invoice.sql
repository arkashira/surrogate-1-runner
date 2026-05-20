
CREATE TABLE invoices (
    id VARCHAR(255) PRIMARY KEY,
    date DATE,
    total DECIMAL(10, 2),
    vendor VARCHAR(255),
    format VARCHAR(255),
    file VARCHAR(255)
);