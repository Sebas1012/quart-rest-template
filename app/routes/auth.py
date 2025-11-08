from quart import request, Blueprint, jsonify
from quart_jwt_extended import create_access_token
from app.models.auth import UserLogin
from passlib.hash import pbkdf2_sha256
from app.utils.role_validator import role_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/token', methods=['POST'])
async def token():
    data = await request.get_json()
    username = data['username']
    password = data['password']

    user = await UserLogin.filter(username=username).first()

    if user and user.verify_password(password):
        additional_claims = {'role': user.user_rol}
        access_token = create_access_token(identity=user.id, user_claims=additional_claims)

        return jsonify({
            'user_id': user.id,
            'user_role': user.user_rol,
            'token': access_token
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@auth_bp.route('/create-user', methods=['POST'])
async def create_user():
    data = await request.get_json()
    username = data['username']
    password = data['password']

    user = await UserLogin.filter(username=username).first()

    if user is None:
        user = UserLogin(username=username, password=pbkdf2_sha256.hash(password))
        await user.save() 

        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'message': 'User already exists'}), 409