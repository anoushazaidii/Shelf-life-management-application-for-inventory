import os
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
from sqlalchemy import event



class MaterialDescription(db.Model):
    __tablename__ = 'MaterialDescriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_description = db.Column(db.String, nullable=False, unique=True)
    code = db.Column(db.String, nullable=False, unique=True)
    shelf_life = db.Column(db.Integer, nullable=False)
    u_o_m = db.Column(db.String,nullable = False, unique=False)

    @classmethod
    def from_dict(cls, data):
        return cls(
            material_description=data['Material Discription'],
            code=data['CODE '].strip(),
            shelf_life=data['shelf_life'],
            u_o_m = data['u_o_m'],
        )
        


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, db.ForeignKey('MaterialDescriptions.code'), nullable=False)
    material_description = db.Column(db.String, nullable=False)
    receiving_date = db.Column(db.DateTime, nullable=False)
    current_date = db.Column(db.DateTime, default=datetime.utcnow)
    aging_days = db.Column(db.Integer)
    shelf_life_remaining = db.Column(db.Integer)
    expiry_date = db.Column(db.DateTime)
    receiving_stock = db.Column(db.Integer)
    remaining_stock = db.Column(db.Integer, default=None)
    shelf_life = db.Column(db.Integer)
    po_number = db.Column(db.String)
    u_o_m = db.Column(db.String)
    issuance = db.Column(db.Boolean, default=False)
    vendor_name = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    total_issuances = db.Column(db.Float, default=0)
    md_number = db.Column(db.Integer)
    lot_number = db.Column(db.Integer)
    issuances = db.relationship('Issuance', backref='product', lazy=True)
    last_issuance_date = db.Column(db.DateTime, default=None)
    barcode_path = db.Column(db.String(255), nullable=True)
    
def set_remaining_stock(mapper, connection, target):
    if target.receiving_stock is not None:
        target.remaining_stock = target.receiving_stock

event.listen(Product, 'before_insert', set_remaining_stock)



class Issuance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    issue_quantity = db.Column(db.Float, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

