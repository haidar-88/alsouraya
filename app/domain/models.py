from app.db import db
from sqlalchemy import Numeric

class admin(db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String(30), primary_key = True)
    password = db.Column(db.String(60), nullable = False)
    role = db.Column(db.String(10), nullable = False)
    
class app_user(db.Model):
    __tablename__ = 'app_user'
    username = db.Column(db.String(30), primary_key = True)
    password = db.Column(db.String(60), nullable = False)
    role = db.Column(db.String(10), nullable = False)

class orders(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('app_user.username'), nullable=False)

    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class ordered_product(db.Model):
    __tablename__ = 'ordered_product'
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    color = db.Column(db.String(10), nullable = False)
    size = db.Column(db.String(10), nullable = False)

class product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    unit_price = db.Column(Numeric(10, 2), nullable = False)
    category = db.Column(db.String(50), nullable = False)

class product_image(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    image_path = db.Column(db.Text)

class product_color(db.Model):
    __tablename__ = 'product_color'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    color = db.Column(db.String(10), nullable = False)

class product_size(db.Model):
    __tablename__ = 'product_size'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    size = db.Column(db.String(10), nullable = False)

class cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    username = db.Column(db.String(30), db.ForeignKey('app_user.username')) 
    size = db.Column(db.String(10), nullable = False)
    color = db.Column(db.String(10), nullable = False)