from flask import Flask, request, jsonify, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)
CORS(api) # Allow CORS requests

@api.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "Hello from backend!"}), 200

# ////////////////////////////////////////////////////////// REGISTRO
@api.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"msg": "Email and password are required"}), 400

    # Validar si el email ya existe
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409
    
    # Encriptar clave y crear usuario
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        email=data["email"],
        password=hashed_password,
        is_active=True # Requerido por el modelo estándar de 4Geeks
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500

# ////////////////////////////////////////////////////////// LOGIN
@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    user = User.query.filter_by(email=data.get("email")).first()
    
    # Verificar usuario y clave encriptada
    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"msg": "Invalid email or password"}), 401

    # Generar Token (identidad como string)
    access_token = create_access_token(identity=str(user.id))
    
    # Retornamos exactamente lo que el Reducer necesita
    return jsonify({
        "token": access_token,
        "user": user.serialize()
    }), 200

# ////////////////////////////////////////////////////////////// RUTA PRIVADA (VALIDACIÓN)
@api.route("/private", methods=["GET"])
@jwt_required()
def handle_private():
    # Obtener el ID del usuario desde el token
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    return jsonify({
        "msg": "Access granted to private area",
        "user": user.serialize()
    }), 200
