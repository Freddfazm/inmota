from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, Realtor

def register_realtor(data):
    if Realtor.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    realtor = Realtor(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(realtor)
    db.session.commit()
    
    return jsonify({'message': 'Realtor registered successfully'}), 201

def login_realtor(data):
    realtor = Realtor.query.filter_by(email=data['email']).first()
    
    if not realtor or not check_password_hash(realtor.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=realtor.id)
    return jsonify({'access_token': access_token}), 200
