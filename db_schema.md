# Database Schema

## products
- id: Primary Key
- name: Product name
- category: Product category
- price: Product price
- stock: Available stock

## sales
- id: Primary Key
- product_id: Foreign Key to products
- quantity: Quantity sold
- total_price: Total price of the sale
- sale_date: Date of sale

## inventory_changes
- id: Primary Key
- product_id: Foreign Key to products
- change: Stock change (+/-)
- timestamp: Time of update
