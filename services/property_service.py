from flask import jsonify
from models import db, Property, Realtor

def create_property(realtor_id, data):
    realtor = Realtor.query.get(realtor_id)
    if not realtor:
        return jsonify({'error': 'Realtor not found'}), 404

    property = Property(
        realtor_id=realtor_id,
        title=data['title'],
        description=data['description'],
        location=data['location'],
        price=data['price'],
        property_type=data['property_type'],
        area=data['area'],
        bedrooms=data['bedrooms'],
        bathrooms=data['bathrooms'],
        status=data['status']
    )
    
    db.session.add(property)
    db.session.commit()
    
    return jsonify({'message': 'Property created successfully', 'id': property.id}), 201

def get_properties(realtor_id):
    properties = Property.query.filter_by(realtor_id=realtor_id).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'location': p.location,
        'price': str(p.price),
        'status': p.status
    } for p in properties]), 200
