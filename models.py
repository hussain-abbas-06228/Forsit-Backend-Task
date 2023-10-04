from sqlalchemy import Column, DateTime, Integer, String, Float, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from database import Base

from datetime import datetime

class Category(Base):
    __tablename__ = 'Category'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False, unique=True)
    products = relationship('Products', backref='category')

class Vendor(Base):
    __tablename__ = 'Vendor'
    vendor_id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_name = Column(String(255), nullable=False, unique=True)
    products = relationship('Products', backref='vendor')

class Products(Base):
    __tablename__ = 'Products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('Category.category_id'))
    vendor_id = Column(Integer, ForeignKey('Vendor.vendor_id'))
    price = Column(Float(2), nullable=False)
    sales = relationship('Sales', backref='product')
    inventories = relationship('Inventory', backref='product')

class Users(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    sales = relationship('Sales', backref='user')

class Sales(Base):
    __tablename__ = 'Sales'
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Products.product_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    revenue = Column(Float(2), nullable=False)

class Inventory(Base):
    __tablename__ = 'Inventory'
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Products.product_id'), nullable=False)
    current_stock = Column(Integer, nullable=False)
    last_updated = Column(Date, nullable=False)



class InventoryChanges(Base):
    __tablename__ = 'inventory_changes'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('Products.product_id'), nullable=False)
    old_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)
    change_date = Column(DateTime, default=datetime.utcnow)

# Indexes
Index('idx_category', Products.category_id)
Index('idx_vendor', Products.vendor_id)
Index('idx_user', Sales.user_id)
Index('idx_product_sales', Sales.product_id)
Index('idx_product_inventory', Inventory.product_id)
Index('idx_product_inventory_changes', InventoryChanges.product_id)

