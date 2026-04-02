from flask import jsonify

class ResponseUtil:
    @staticmethod
    def success(data=None, message="操作成功"):
        """成功响应"""
        return jsonify({
            "code": 200,
            "message": message,
            "data": data
        })
    
    @staticmethod
    def error(code=400, message="操作失败"):
        """错误响应"""
        return jsonify({
            "code": code,
            "message": message,
            "data": None
        }), code
    
    @staticmethod
    def not_found(message="资源不存在"):
        """资源不存在响应"""
        return jsonify({
            "code": 404,
            "message": message,
            "data": None
        }), 404
    
    @staticmethod
    def bad_request(message="请求参数错误"):
        """请求参数错误响应"""
        return jsonify({
            "code": 400,
            "message": message,
            "data": None
        }), 400
    
    @staticmethod
    def internal_error(message="服务器内部错误"):
        """服务器内部错误响应"""
        return jsonify({
            "code": 500,
            "message": message,
            "data": None
        }), 500
