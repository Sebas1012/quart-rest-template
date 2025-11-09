from quart import Blueprint, jsonify

hello_bp = Blueprint('hello', __name__, url_prefix='/api/v1/hello')

@hello_bp.route('/', methods=['GET'])
async def hello():
    return jsonify({'message': 'Hello, World!'})