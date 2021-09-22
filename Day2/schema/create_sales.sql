CREATE TABLE IF NOT EXISTS sales(
	id VARCHAR(500),
	transaction_id VARCHAR(500),
	bill_no VARCHAR(500),
	bill_date VARCHAR(500),
	bill_location VARCHAR(500),
	customer_id VARCHAR(500),
	product_id VARCHAR(500),
	qty VARCHAR(500),
	uom VARCHAR(500),
	price VARCHAR(500),
	gross_price VARCHAR(500),
	tax_pc VARCHAR(500),
	tax_amt VARCHAR(500),
	discount_pc VARCHAR(500),
	discount_amt VARCHAR(500),
	net_bill_amt VARCHAR(500),
	created_by VARCHAR(500),
	created_date VARCHAR(500),
	updated_by VARCHAR(500),
	updated_date VARCHAR(500)
);