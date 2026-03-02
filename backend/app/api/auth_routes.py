from flask import Blueprint, request, jsonify
from ..models import User
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 401
        
        # 检查密码（注意：这里直接比较密码，因为我们在导入数据时存储的是明文密码）
        # 在实际生产环境中，应该使用哈希密码
        if user.password != data['password']:
            return jsonify({'error': '密码错误'}), 401
        
        # 返回用户信息
        return jsonify({
            'message': '登录成功',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/check', methods=['GET'])
def check_auth():
    # 这里可以添加token验证逻辑
    # 由于我们没有实现token认证，暂时返回一个简单的响应
    return jsonify({'message': '认证检查通过'}), 200

@bp.route('/logout', methods=['POST'])
def logout():
    # 这里可以添加token失效逻辑
    # 由于我们没有实现token认证，暂时返回一个简单的响应
    return jsonify({'message': '登出成功'}), 200
