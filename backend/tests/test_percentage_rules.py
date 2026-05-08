"""
单元测试：百分比规则动态获取功能

测试场景：
1. 正常情况：数据库中有grade_settings记录
2. 缺失字段：某些百分比规则字段缺失
3. 表不存在：grade_settings表不存在
4. 连接错误：数据库连接失败
5. 缓存机制：验证缓存功能正常工作
6. 数据验证：验证数值范围和类型检查
"""

import unittest
import unittest.mock as mock
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_access.grade_data_access import GradeDataAccess


class TestPercentageRules(unittest.TestCase):
    
    def setUp(self):
        """测试前准备：清除缓存"""
        GradeDataAccess._clear_percentage_rules_cache()
    
    def tearDown(self):
        """测试后清理：清除缓存"""
        GradeDataAccess._clear_percentage_rules_cache()
    
    def test_get_percentage_rules_normal_case(self):
        """测试正常情况：数据库中有grade_settings记录"""
        # Mock GradeSettings查询
        mock_settings = mock.Mock()
        mock_settings.percentage_rule_a = 90
        mock_settings.percentage_rule_b = 85
        mock_settings.percentage_rule_c = 75
        mock_settings.percentage_rule_d = 60
        mock_settings.percentage_rule_e = 50
        
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = mock_settings
            
            rules = GradeDataAccess.get_percentage_rules()
            
            self.assertEqual(rules['percentage_rule_a'], 90)
            self.assertEqual(rules['percentage_rule_b'], 85)
            self.assertEqual(rules['percentage_rule_c'], 75)
            self.assertEqual(rules['percentage_rule_d'], 60)
            self.assertEqual(rules['percentage_rule_e'], 50)
    
    def test_get_percentage_rules_missing_fields(self):
        """测试缺失字段：某些百分比规则字段缺失"""
        # Mock GradeSettings查询，只设置部分字段
        mock_settings = mock.Mock()
        mock_settings.percentage_rule_a = 95
        mock_settings.percentage_rule_b = None  # 缺失
        mock_settings.percentage_rule_c = 70
        mock_settings.percentage_rule_d = None  # 缺失
        mock_settings.percentage_rule_e = 45
        
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = mock_settings
            
            rules = GradeDataAccess.get_percentage_rules()
            
            # 验证存在的字段使用实际值
            self.assertEqual(rules['percentage_rule_a'], 95)
            self.assertEqual(rules['percentage_rule_c'], 70)
            self.assertEqual(rules['percentage_rule_e'], 45)
            
            # 验证缺失的字段使用默认值
            self.assertEqual(rules['percentage_rule_b'], 85)  # 默认值
            self.assertEqual(rules['percentage_rule_d'], 60)  # 默认值
    
    def test_get_percentage_rules_no_settings_record(self):
        """测试表中无记录：grade_settings表中没有记录"""
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = None
            
            rules = GradeDataAccess.get_percentage_rules()
            
            # 验证使用默认值
            self.assertEqual(rules['percentage_rule_a'], 90)
            self.assertEqual(rules['percentage_rule_b'], 85)
            self.assertEqual(rules['percentage_rule_c'], 75)
            self.assertEqual(rules['percentage_rule_d'], 60)
            self.assertEqual(rules['percentage_rule_e'], 50)
    
    def test_get_percentage_rules_database_error(self):
        """测试数据库连接错误：模拟数据库查询失败"""
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.side_effect = Exception("Database connection failed")
            
            rules = GradeDataAccess.get_percentage_rules()
            
            # 验证在异常情况下使用默认值
            self.assertEqual(rules['percentage_rule_a'], 90)
            self.assertEqual(rules['percentage_rule_b'], 85)
            self.assertEqual(rules['percentage_rule_c'], 75)
            self.assertEqual(rules['percentage_rule_d'], 60)
            self.assertEqual(rules['percentage_rule_e'], 50)
    
    def test_get_percentage_rules_cache(self):
        """测试缓存机制：验证缓存功能正常工作"""
        mock_settings = mock.Mock()
        mock_settings.percentage_rule_a = 90
        mock_settings.percentage_rule_b = 85
        mock_settings.percentage_rule_c = 75
        mock_settings.percentage_rule_d = 60
        mock_settings.percentage_rule_e = 50
        
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = mock_settings
            
            # 第一次调用，应该查询数据库
            rules1 = GradeDataAccess.get_percentage_rules()
            self.assertEqual(MockGradeSettings.query.first.call_count, 1)
            
            # 第二次调用，应该使用缓存
            rules2 = GradeDataAccess.get_percentage_rules()
            self.assertEqual(MockGradeSettings.query.first.call_count, 1)  # 仍然是1次调用
            
            # 验证两次结果相同
            self.assertEqual(rules1, rules2)
    
    def test_get_percentage_rules_cache_expire(self):
        """测试缓存过期：验证缓存过期后重新查询"""
        mock_settings = mock.Mock()
        mock_settings.percentage_rule_a = 90
        mock_settings.percentage_rule_b = 85
        mock_settings.percentage_rule_c = 75
        mock_settings.percentage_rule_d = 60
        mock_settings.percentage_rule_e = 50
        
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = mock_settings
            
            # 第一次调用
            GradeDataAccess.get_percentage_rules()
            self.assertEqual(MockGradeSettings.query.first.call_count, 1)
            
            # 模拟缓存过期（设置过期时间为过去）
            import time
            GradeDataAccess._cache_timestamp = time.time() - 400  # 过期
            
            # 第二次调用，应该重新查询
            GradeDataAccess.get_percentage_rules()
            self.assertEqual(MockGradeSettings.query.first.call_count, 2)
    
    def test_validate_percentage_value_normal(self):
        """测试数值验证：正常数值"""
        result = GradeDataAccess._validate_percentage_value(80, 75, 'test')
        self.assertEqual(result, 80)
    
    def test_validate_percentage_value_none(self):
        """测试数值验证：None值使用默认值"""
        result = GradeDataAccess._validate_percentage_value(None, 75, 'test')
        self.assertEqual(result, 75)
    
    def test_validate_percentage_value_invalid_type(self):
        """测试数值验证：无效类型使用默认值"""
        result = GradeDataAccess._validate_percentage_value('invalid', 75, 'test')
        self.assertEqual(result, 75)
    
    def test_validate_percentage_value_out_of_range(self):
        """测试数值验证：超出范围的值使用默认值"""
        # 大于100
        result1 = GradeDataAccess._validate_percentage_value(150, 75, 'test')
        self.assertEqual(result1, 75)
        
        # 小于0
        result2 = GradeDataAccess._validate_percentage_value(-10, 75, 'test')
        self.assertEqual(result2, 75)
    
    def test_refresh_percentage_rules(self):
        """测试刷新缓存：验证强制刷新功能"""
        mock_settings = mock.Mock()
        mock_settings.percentage_rule_a = 90
        mock_settings.percentage_rule_b = 85
        mock_settings.percentage_rule_c = 75
        mock_settings.percentage_rule_d = 60
        mock_settings.percentage_rule_e = 50
        
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = mock_settings
            
            # 第一次调用
            GradeDataAccess.get_percentage_rules()
            self.assertEqual(MockGradeSettings.query.first.call_count, 1)
            
            # 刷新缓存并重新获取
            GradeDataAccess.refresh_percentage_rules()
            self.assertEqual(MockGradeSettings.query.first.call_count, 2)
    
    def test_percentage_rule_c_default(self):
        """测试percentage_rule_c默认值：验证默认值为75"""
        # 场景1：表中无记录
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = None
            
            rules = GradeDataAccess.get_percentage_rules()
            self.assertEqual(rules['percentage_rule_c'], 75)
        
        # 场景2：字段为None
        mock_settings = mock.Mock()
        mock_settings.percentage_rule_a = 90
        mock_settings.percentage_rule_b = 85
        mock_settings.percentage_rule_c = None  # 缺失
        mock_settings.percentage_rule_d = 60
        mock_settings.percentage_rule_e = 50
        
        with mock.patch('app.data_access.grade_data_access.GradeSettings') as MockGradeSettings:
            MockGradeSettings.query.first.return_value = mock_settings
            
            rules = GradeDataAccess.get_percentage_rules()
            self.assertEqual(rules['percentage_rule_c'], 75)


if __name__ == '__main__':
    unittest.main()
