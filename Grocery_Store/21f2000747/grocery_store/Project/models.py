from flask_login import UserMixin
from . import db as database
from datetime import datetime as dt


class CustomerUser(UserMixin, database.Model):
    __tablename__ = 'CustomerUser'
    user_id = database.Column(
        database.Integer, primary_key=True, autoincrement=True)
    user_name = database.Column(database.String(1000))
    user_handle = database.Column(database.String(100), unique=True)
    user_password = database.Column(database.String(100))
    user_role = database.Column(database.Numeric())

    def get_id(self):
        return str(self.user_id)


class ProductCategories(database.Model):
    __tablename__ = 'ProductCategories'
    category_id = database.Column(
        database.Integer, primary_key=True, autoincrement=True)
    category_title = database.Column(database.String())

    def __repr__(self):
        return f"ProductCategories(category_id={self.category_id}, category_title='{self.category_title}')"


class ProductItem(database.Model):
    __tablename__ = 'ProductItem'
    product_id = database.Column(
        database.Integer, primary_key=True, autoincrement=True)
    product_name = database.Column(database.String(100))
    product_category_id = database.Column(
        database.Integer, database.ForeignKey('ProductCategories.category_id'))
    expiration_date = database.Column(database.Date)
    manufacturing_date = database.Column(database.Date)
    product_price = database.Column(database.Float)
    product_unit = database.Column(database.String())
    product_quantity = database.Column(database.Float)
    image_url = database.Column(database.String())
    image_file = database.Column(database.LargeBinary)
    creation_date = database.Column(
        database.DateTime, default=dt.utcnow, nullable=False)

    category = database.relationship(
        'ProductCategories', backref=database.backref('product_items', lazy=True))

    def __repr__(self):
        return f"ProductItem(product_id={self.product_id}, expiration_date={self.expiration_date}, manufacturing_date={self.manufacturing_date}, product_price={self.product_price}), product_unit={self.product_unit}, product_quantity={self.product_quantity}, creation_date={self.creation_date}"


class OrderData(database.Model):
    __tablename__ = 'OrderData'
    order_id = database.Column(
        database.Integer, primary_key=True, autoincrement=True)
    customer_id = database.Column(
        database.Integer, database.ForeignKey('CustomerUser.user_id'))
    item_id = database.Column(
        database.Integer, database.ForeignKey('ProductItem.product_id'))
    ordered_quantity = database.Column(database.Float)
    order_total = database.Column(database.Float)
    order_status = database.Column(database.String)
    item_title = database.Column(database.String(100))
    item_cost = database.Column(database.Float)
