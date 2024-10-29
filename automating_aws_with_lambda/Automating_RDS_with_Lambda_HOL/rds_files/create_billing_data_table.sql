CREATE TABLE IF NOT EXISTS billing_data (
    id INT,
    company_name VARCHAR(255),
    country VARCHAR(255),
    city VARCHAR(255),
    product_line VARCHAR(255),
    item VARCHAR(255),
    bill_date DATE,
    currency VARCHAR(255),
    bill_amount DECIMAL(14, 2),
    bill_amount_usd DECIMAL(14, 2),
	PRIMARY KEY (id, bill_date)
);
