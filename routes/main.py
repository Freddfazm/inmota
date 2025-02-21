from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Realtor, Property, Subscription
from services.auth_service import register_realtor, login_realtor
from services.property_service import create_property, get_properties

main_bp = Blueprint('main', __name__)

@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_realtor(data)

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_realtor(data)

@main_bp.route('/properties', methods=['POST'])
@jwt_required()
def add_property():
    data = request.get_json()
    realtor_id = get_jwt_identity()
    return create_property(realtor_id, data)

@main_bp.route('/properties', methods=['GET'])
@jwt_required()
def list_properties():
    realtor_id = get_jwt_identity()
    return get_properties(realtor_id)
