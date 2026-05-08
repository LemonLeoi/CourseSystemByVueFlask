from flask import jsonify
import json


class NumberFormatter:
    """数值格式化工具类"""
    
    @staticmethod
    def format_number(value, decimals=2):
        """
        格式化单个数值，保留指定小数位数
        
        Args:
            value: 待格式化的数值
            decimals: 保留的小数位数，默认为2
            
        Returns:
            格式化后的数值（四舍五入），如果输入无效则返回原值
        """
        try:
            # 尝试转换为浮点数
            num = float(value)
            
            # 使用round进行四舍五入
            formatted = round(num, decimals)
            
            # 如果结果是整数（如 5.0），返回整数形式
            if formatted == int(formatted):
                return int(formatted)
            
            return formatted
            
        except (ValueError, TypeError):
            # 如果转换失败，返回原值
            return value
    
    @staticmethod
    def format_data(data):
        """
        递归格式化数据结构中的所有数值
        
        Args:
            data: 任意类型的数据（dict, list, tuple, 或基本类型）
            
        Returns:
            格式化后的数据，所有数值保留两位小数
        """
        if isinstance(data, dict):
            # 处理字典
            return {key: NumberFormatter.format_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            # 处理列表
            return [NumberFormatter.format_data(item) for item in data]
        elif isinstance(data, tuple):
            # 处理元组
            return tuple(NumberFormatter.format_data(item) for item in data)
        elif isinstance(data, (int, float)):
            # 处理数值类型
            return NumberFormatter.format_number(data, 2)
        else:
            # 其他类型（字符串、None等）保持不变
            return data


class ResponseUtil:
    @staticmethod
    def success(data=None, message="操作成功"):
        """成功响应"""
        # 格式化数据中的所有数值
        formatted_data = NumberFormatter.format_data(data)
        
        return jsonify({
            "code": 200,
            "message": message,
            "data": formatted_data
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
