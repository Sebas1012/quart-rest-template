from quart import Blueprint
from quart_jwt_extended import create_access_token
from app.models.auth import UserLogin, TokenResponse, User, UserResponse, ErrorResponse
from passlib.hash import pbkdf2_sha256
from quart_schema import validate_request, validate_response

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/token', methods=['POST'])
@validate_request(User)
@validate_response(TokenResponse, 200)
@validate_response(ErrorResponse, 401)
async def token(data: User):
    username = data.username
    password = data.password

    user = await UserLogin.filter(username=username).first()

    if user and user.verify_password(password):
        additional_claims = {'role': user.user_rol}
        access_token = create_access_token(identity=user.id, user_claims=additional_claims)

        return {
            'user_id': user.id,
            'user_role': user.user_rol,
            'token': access_token
        }, 200
    
    return {'message': 'Invalid username or password'}, 401
    
@auth_bp.route('/create-user', methods=['POST'])
@validate_request(User)
@validate_response(UserResponse, 201)
@validate_response(ErrorResponse, 409)
async def create_user(data: User):
    username = data.username
    password = data.password

    user = await UserLogin.filter(username=username).first()

    if user is None:
        user = UserLogin(username=username, password=pbkdf2_sha256.hash(password))
        await user.save() 

        return {'message': 'User created successfully'}, 201

    return {'message': 'User already exists'}, 409