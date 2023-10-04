# E-commerce Database Schema Documentation

## Overview
The e-commerce database consists of several tables designed to manage products, sales, inventory, vendors, users, and other related data. Each table is designed with specific attributes and has relationships with other tables to represent real-world scenarios of an e-commerce platform.

## Tables

### 1. Category
- **Purpose**: Represents different categories of products available on the platform.
- **Attributes**:
  - `category_id`: Unique identifier for each category.
  - `category_name`: Name of the category. This should be unique.
- **Relationships**:
  - One-to-many with the `Products` table. A category can be associated with multiple products.

### 2. Vendor
- **Purpose**: Represents vendors or manufacturers who supply products.
- **Attributes**:
  - `vendor_id`: Unique identifier for each vendor.
  - `vendor_name`: Name of the vendor. This should be unique.
- **Relationships**:
  - One-to-many with the `Products` table. A vendor can be associated with multiple products.

### 3. Products
- **Purpose**: Represents individual products available for sale.
- **Attributes**:
  - `product_id`: Unique identifier for each product.
  - `name`: Name of the product.
  - `category_id`: Reference to the category to which the product belongs.
  - `vendor_id`: Reference to the vendor of the product.
  - `price`: Price of the product.
- **Relationships**:
  - Many-to-one with `Category`.
  - Many-to-one with `Vendor`.
  - One-to-many with `Sales`, `Inventory`, and `InventoryChanges`.

### 4. Users
- **Purpose**: Represents users or customers of the platform.
- **Attributes**:
  - `user_id`: Unique identifier for each user.
  - `user_name`: Name of the user. This should be unique.
  - `email`: Email address of the user. This should be unique.
- **Relationships**:
  - One-to-many with `Sales`.

### 5. Sales
- **Purpose**: Records sales transactions.
- **Attributes**:
  - `sale_id`: Unique identifier for each sale.
  - `product_id`: Reference to the product that was sold.
  - `user_id`: Reference to the user who made the purchase.
  - `quantity_sold`: Quantity of the product sold in the transaction.
  - `sale_date`: Date of the sale.
  - `revenue`: Total revenue from the sale (typically `price x quantity_sold`).
- **Relationships**:
  - Many-to-one with `Products`.
  - Many-to-one with `Users`.

### 6. Inventory
- **Purpose**: Maintains current inventory levels for products.
- **Attributes**:
  - `inventory_id`: Unique identifier for each inventory entry.
  - `product_id`: Reference to the product.
  - `current_stock`: Current stock level of the product.
  - `last_updated`: Date the inventory was last updated.
- **Relationships**:
  - Many-to-one with `Products`.

### 7. InventoryChanges
- **Purpose**: Tracks changes in inventory levels over time.
- **Attributes**:
  - `id`: Unique identifier for each inventory change entry.
  - `product_id`: Reference to the product.
  - `old_stock`: Previous stock level before the change.
  - `new_stock`: Updated stock level after the change.
  - `change_date`: Date and time of the inventory change.
- **Relationships**:
  - Many-to-one with `Products`.

## Summary
The database is designed to effectively manage product listings, sales transactions, and inventory. The relationships between tables ensure that the data is organized in a structured manner, facilitating complex queries and operations necessary for e-commerce operations.
