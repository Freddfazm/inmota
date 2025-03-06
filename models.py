from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Realtor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    subscription = db.relationship('Subscription', backref='realtors')
    properties = db.relationship('Property', backref='realtor', lazy=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    max_properties = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    realtor_id = db.Column(db.Integer, db.ForeignKey('realtor.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    property_description = db.Column(db.Text(5000), nullable=True)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    area = db.Column(db.Numeric(10, 2), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    garage_spaces = db.Column(db.Integer, nullable=False, default=0)
    
    operation = db.Column(db.String(50), nullable=False, default="Venta")
    list_date = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    list_status = db.Column(db.String(50), nullable=False, default="Activo")
    off_market_date = db.Column(db.Date, nullable=True)
    close_date = db.Column(db.Date, nullable=True)
    close_price = db.Column(db.Numeric(12, 2), nullable=True)
    
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    photos = db.relationship('PropertyPhoto', backref='property', lazy=True)

class PropertyPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())