from app import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    expiry_year = db.Column(db.Integer, nullable=False)
    max_discount = db.Column(db.Numeric(10, 2), nullable=False)