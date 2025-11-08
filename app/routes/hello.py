from quart import request, Blueprint, jsonify

hello_bp = Blueprint('hello', __name__)

@hello_bp.route('/', methods=['GET'])
async def hello():
    return jsonify({'message': 'Hello, World!'})