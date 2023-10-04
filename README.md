# E-commerce API

## Introduction
This API is designed for an e-commerce platform. It facilitates operations like product registration, sales data retrieval, inventory management, revenue analysis, and more.

## Setup Instructions

### Database Configuration
- Ensure you have MySQL installed and running.
- Create a database named `e_commerce_db`.
- Update the `URL_DATABASE` in `database.py` if your MySQL configurations are different.

### Python Environment
- Ensure you have Python 3.8 or later installed.
- It's recommended to create a virtual environment for the project:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
- Install the required Python packages:
    ```bash
    pip install fastapi[all] pymysql sqlalchemy uvicorn
    ```

### Running the Application
- Start the application using:
    ```bash
    uvicorn main:app --reload
    ```
- Access the application at `http://127.0.0.1:8000`.

## API Endpoints

1. **Product Registration**
    - `POST /product/register/`: Register a new product with its name, category, vendor, price, and opening stock.

2. **Sales Data Retrieval**
    - `GET /sales/`: Fetch sales data within a given date range and optionally filter by product or category.

3. **Revenue Analysis**
    - `GET /revenue/analysis/`: Analyze revenue within a given time frame and optionally filter by category.
    - `GET /revenue/`: Fetch revenue data grouped by day, month, or year.
    - `GET /revenue/compare/categories/`: Compare revenue between two categories.
    - `GET /revenue/compare/time-periods/`: Compare revenue between two different time periods.

4. **Inventory Management**
    - `GET /low_inventory/status/`: Check products that have inventory below a certain threshold.
    - `PUT /inventory/{product_id}/`: Update the inventory of a specific product.
    - `GET /inventory/{product_id}/changes/`: Fetch changes in inventory of a specific product over time.
    - `GET /inventory/{product_id}/status/`: Check the current inventory status of a product.

## Dependencies
- **FastAPI**: A modern, fast web framework for building APIs with Python 3.7+.
- **PyMySQL**: A pure-Python MySQL driver.
- **SQLAlchemy**: A popular SQL toolkit and Object-Relational Mapping (ORM) library for Python.

## Conclusion
This e-commerce API provides a robust set of tools to help you manage products, sales, and inventory. Ensure you have set up the environment correctly and initialized the database before running the API.
