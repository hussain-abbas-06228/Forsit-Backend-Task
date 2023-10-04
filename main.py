from itertools import groupby
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import session
import models
from database import engine, SessionLocal
from datetime import date, timedelta

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models for request and response
class ProductCreate(BaseModel):
    name: str
    category_id: int
    vendor_id: int
    price: float
    opening_stock: int
    

class InventoryUpdate(BaseModel):
    product_id: int
    current_stock: int

# Endpoints
@app.post("/product/register/", status_code=status.HTTP_201_CREATED)
def register_product(product: ProductCreate, db: session.Session = Depends(get_db)):
    new_product = models.Products(
        name=product.name,
        category_id=product.category_id,
        vendor_id=product.vendor_id,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    new_inventory = models.Inventory(product_id=new_product.product_id, current_stock=product.opening_stock, last_updated=date.today())
    db.add(new_inventory)


    db.commit()
    db.refresh(new_product)
    return new_product

# Retrieve, Filter, and Analyze Sales Data:
@app.get("/sales/")
def get_sales_data(
    start_date: date = None, 
    end_date: date = date.today(),
    product_id: int = None,
    category_id: int = None,
    db: session.Session = Depends(get_db)):
    query = db.query(models.Sales).filter(models.Sales.sale_date.between(start_date, end_date))
    if product_id:
        query = query.filter(models.Sales.product_id == product_id)
    if category_id:
        query = query.join(models.Products).filter(models.Products.category_id == category_id)

    # Fetching data
    sales_data = query.all()

    # Calculating total revenue
    total_revenue = sum([sale.revenue for sale in sales_data])

    # Calculating total quantity sold

    total_quantity_sold = sum([sale.quantity_sold for sale in sales_data])

    # check if product_id
    if product_id:
        return {"product_id":product_id,"total_quantity_sold": total_quantity_sold,"total_revenue": total_revenue}
    else:
        return {"category_id":category_id,"total_quantity_sold": total_quantity_sold,"total_revenue": total_revenue}








@app.get("/revenue/analysis/")
def revenue_analysis(
    time_frame: str = Query(..., description="daily, weekly, monthly, annually"),
    category_id: int = None,
    db: session.Session = Depends(get_db)):
    # Define date range based on time_frame
    today = date.today()
    if time_frame == "daily":
        start_date = today
    elif time_frame == "weekly":
        start_date = today - timedelta(days=7)
    elif time_frame == "monthly":
        start_date = today.replace(day=1)
    elif time_frame == "annually":
        start_date = today.replace(day=1, month=1)
    else:
        raise HTTPException(status_code=400, detail="Invalid time_frame")

    # Filtering based on date range and category
    query = db.query(models.Sales).filter(models.Sales.sale_date.between(start_date, today))
    if category_id:
        query = query.join(models.Products).filter(models.Products.category_id == category_id)

    # Calculating revenue
    revenue = sum([sale.revenue for sale in query.all()])
    
    # add timeframe selected and category selected
    if category_id:
        return {"time_frame":time_frame,"category_id":category_id,"revenue": revenue}
    else:
        return {"time_frame":time_frame,"revenue": revenue}



# Analyze Revenue on Different Time Frames:
@app.get("/revenue/")
def get_revenue_data(time_frame: str = Query(..., description="daily, weekly, monthly, annually"), db: session.Session = Depends(get_db)):
    # We can use SQL's date functions for grouping by day, month, year
    if time_frame == "daily":
        group_by_clause = func.date(models.Sales.sale_date)
    elif time_frame == "monthly":
        group_by_clause = func.month(models.Sales.sale_date)
    elif time_frame == "annual":
        group_by_clause = func.year(models.Sales.sale_date)
    else:
        raise HTTPException(status_code=400, detail="Invalid time frame")
    
    revenues = db.query(group_by_clause, func.sum(models.Sales.revenue)).group_by(group_by_clause).all()

    # Convert the SQLAlchemy objects to dictionaries for JSON serialization
    revenues = [{"time_frame":time_frame, "revenue": revenue[1]} for revenue in revenues]
    return revenues





@app.get("/low_inventory/status/")
def low_inventory_check(low_stock_alert: int, db: session.Session = Depends(get_db)):
    query = db.query(models.Inventory).filter(models.Inventory.current_stock <= low_stock_alert)
    low_stock_items = query.all()
    items = []
    for item in low_stock_items:
        product = db.query(models.Products).filter(models.Products.product_id == item.product_id).first()
        items.append({"product_id": item.product_id, "product_name": product.name, "current_stock": item.current_stock})
    return {"low_stock_items": items}



@app.put("/inventory/{product_id}/")
def update_inventory(product_id: int, stock_change: int, db: session.Session = Depends(get_db)):
    inventory_item = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).one_or_none()
    
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    
    # Capture the old stock level before updating
    old_stock = inventory_item.current_stock

    # Update the inventory's current stock
    inventory_item.current_stock = stock_change
    inventory_item.last_updated = date.today()  # or use datetime.now() if you store time as well
    
    # Record the change in the InventoryChanges table
    inventory_change = models.InventoryChanges(
        product_id=product_id,
        old_stock=old_stock,
        new_stock=inventory_item.current_stock
    )
    db.add(inventory_change)
    
    db.commit()

    inventory_item_result = []
    inventory_item_result.append({"product_id": inventory_item.product_id, "current_stock": inventory_item.current_stock})

    inventory_change_result=[]
    inventory_change_result.append({"product_id": inventory_change.product_id, "old_stock": inventory_change.old_stock, "new_stock": inventory_change.new_stock})


    return {"inventory": inventory_item_result, "inventory_change": inventory_change_result}



# Get changes over time in stock
@app.get("/inventory/{product_id}/changes/")
def get_inventory_changes(product_id: int, db: session.Session = Depends(get_db)):
    inventory_changes = db.query(models.InventoryChanges).filter(models.InventoryChanges.product_id == product_id).all()
    
    if not inventory_changes:
        raise HTTPException(status_code=404, detail="No changes found for this product")

    # Convert the SQLAlchemy objects to dictionaries for JSON serialization
    result = []

    for change in inventory_changes:
        result.append({"product_id": change.product_id, "old_stock": change.old_stock, "new_stock": change.new_stock, "change_date": change.change_date})

    return {"inventory_changes": result}

from sqlalchemy import func, and_


# Check the current inventory status of a product
@app.get("/inventory/{product_id}/status/")
def get_inventory_status(product_id: int, db: session.Session = Depends(get_db)):
    inventory_item = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).one_or_none()
    
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Product not found in inventory")
    
    return {"product_id": product_id, "current_stock": inventory_item.current_stock}

# Compare revenue between categories
@app.get("/revenue/compare/categories/")
def compare_revenue_by_category(
    category_id_1: int = None, category_id_2: int = None, db: session.Session = Depends(get_db)):
    
    # Base query
    base_query = db.query(
        models.Category.category_name,
        func.sum(models.Sales.revenue).label("total_revenue")
    ).join(
        models.Products, models.Products.category_id == models.Category.category_id
    ).join(
        models.Sales, models.Sales.product_id == models.Products.product_id
    ).group_by(models.Category.category_name)
    
    # If category IDs are provided, modify the query to filter by these categories
    if category_id_1 and category_id_2:
        base_query = base_query.filter(models.Category.category_id.in_([category_id_1, category_id_2]))
    
    category_revenues = base_query.all()
    
    return {"revenues": {item[0]: item[1] for item in category_revenues}}

# Compare revenue between different time periods
# for testing use the following dates: start_date=2023-08-01 end_date=2023-08-31 previous_start_date=2023-10-01 previous_end_date=2023-10-31
@app.get("/revenue/compare/time-periods/")
def compare_revenue_by_time_period(start_date: date, end_date: date, previous_start_date: date = None, previous_end_date: date = None, db: session.Session = Depends(get_db)):
    period_revenue = db.query(func.sum(models.Sales.revenue)).filter(and_(models.Sales.sale_date >= start_date, models.Sales.sale_date <= end_date)).scalar()
    
    if previous_start_date and previous_end_date:
        previous_period_revenue = db.query(func.sum(models.Sales.revenue)).filter(and_(models.Sales.sale_date >= previous_start_date, models.Sales.sale_date <= previous_end_date)).scalar()
        return {
            "current_period_revenue": period_revenue,
            "previous_period_revenue": previous_period_revenue
        }
    
    return {"current_period_revenue": period_revenue}
