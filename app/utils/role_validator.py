from functools import wraps
from quart import jsonify
from quart_jwt_extended import jwt_required, get_jwt

def role_required(allowed_roles):
    if not isinstance(allowed_roles, (list, tuple)):
        allowed_roles = [allowed_roles]

    def decorator(fn):
        @jwt_required()
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            
            claims = get_jwt()
            
            if "role" not in claims:
                return jsonify({"message": "Missing 'role' claim in token."}), 403
                
            user_role = claims["role"]
            
            if user_role not in allowed_roles:
                return jsonify({"message": "Not authorized. Insufficient permissions."}), 403

            return await fn(*args, **kwargs)
            
        return wrapper
    return decorator