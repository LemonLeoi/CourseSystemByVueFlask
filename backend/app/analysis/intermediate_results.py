# Intermediate results storage module
import json
import datetime
import os
import pickle

class IntermediateResultsStorage:
    """中间结果存储类"""
    
    def __init__(self, storage_dir='e:/A_Course/backend/intermediate_results'):
        """初始化中间结果存储
        
        Args:
            storage_dir: 存储目录
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def save_result(self, analysis_id, step, data, description=None):
        """保存中间结果
        
        Args:
            analysis_id: 分析ID
            step: 分析步骤
            data: 中间数据
            description: 结果描述
            
        Returns:
            存储路径
        """
        try:
            # 创建分析目录
            analysis_dir = os.path.join(self.storage_dir, analysis_id)
            os.makedirs(analysis_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{step}_{timestamp}.json"
            file_path = os.path.join(analysis_dir, file_name)
            
            # 准备存储数据
            storage_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'step': step,
                'description': description,
                'data': data
            }
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, ensure_ascii=False, indent=2)
            
            return file_path
        except Exception as e:
            print(f"保存中间结果失败: {e}")
            return None
    
    def save_model_state(self, analysis_id, model_name, model_state, description=None):
        """保存模型状态
        
        Args:
            analysis_id: 分析ID
            model_name: 模型名称
            model_state: 模型状态
            description: 模型描述
            
        Returns:
            存储路径
        """
        try:
            # 创建分析目录
            analysis_dir = os.path.join(self.storage_dir, analysis_id)
            os.makedirs(analysis_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"model_{model_name}_{timestamp}.pkl"
            file_path = os.path.join(analysis_dir, file_name)
            
            # 准备存储数据
            storage_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'model_name': model_name,
                'description': description,
                'model_state': model_state
            }
            
            # 保存到文件
            with open(file_path, 'wb') as f:
                pickle.dump(storage_data, f)
            
            return file_path
        except Exception as e:
            print(f"保存模型状态失败: {e}")
            return None
    
    def get_results(self, analysis_id, step=None):
        """获取中间结果
        
        Args:
            analysis_id: 分析ID
            step: 分析步骤（可选）
            
        Returns:
            中间结果列表
        """
        try:
            analysis_dir = os.path.join(self.storage_dir, analysis_id)
            if not os.path.exists(analysis_dir):
                return []
            
            results = []
            for file_name in os.listdir(analysis_dir):
                if file_name.endswith('.json'):
                    file_path = os.path.join(analysis_dir, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if step and data.get('step') != step:
                        continue
                    results.append(data)
            
            # 按时间排序
            results.sort(key=lambda x: x.get('timestamp', ''))
            return results
        except Exception as e:
            print(f"获取中间结果失败: {e}")
            return []
    
    def get_model_state(self, analysis_id, model_name=None):
        """获取模型状态
        
        Args:
            analysis_id: 分析ID
            model_name: 模型名称（可选）
            
        Returns:
            模型状态列表
        """
        try:
            analysis_dir = os.path.join(self.storage_dir, analysis_id)
            if not os.path.exists(analysis_dir):
                return []
            
            models = []
            for file_name in os.listdir(analysis_dir):
                if file_name.endswith('.pkl'):
                    file_path = os.path.join(analysis_dir, file_name)
                    with open(file_path, 'rb') as f:
                        data = pickle.load(f)
                    if model_name and data.get('model_name') != model_name:
                        continue
                    models.append(data)
            
            # 按时间排序
            models.sort(key=lambda x: x.get('timestamp', ''))
            return models
        except Exception as e:
            print(f"获取模型状态失败: {e}")
            return []
    
    def save_conclusion(self, analysis_id, conclusion, level='intermediate'):
        """保存阶段性结论
        
        Args:
            analysis_id: 分析ID
            conclusion: 结论内容
            level: 结论级别（intermediate或final）
            
        Returns:
            存储路径
        """
        try:
            # 创建分析目录
            analysis_dir = os.path.join(self.storage_dir, analysis_id)
            os.makedirs(analysis_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"conclusion_{level}_{timestamp}.json"
            file_path = os.path.join(analysis_dir, file_name)
            
            # 准备存储数据
            storage_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'level': level,
                'conclusion': conclusion
            }
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, ensure_ascii=False, indent=2)
            
            return file_path
        except Exception as e:
            print(f"保存阶段性结论失败: {e}")
            return None
    
    def get_conclusions(self, analysis_id, level=None):
        """获取阶段性结论
        
        Args:
            analysis_id: 分析ID
            level: 结论级别（可选）
            
        Returns:
            结论列表
        """
        try:
            analysis_dir = os.path.join(self.storage_dir, analysis_id)
            if not os.path.exists(analysis_dir):
                return []
            
            conclusions = []
            for file_name in os.listdir(analysis_dir):
                if 'conclusion' in file_name and file_name.endswith('.json'):
                    file_path = os.path.join(analysis_dir, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if level and data.get('level') != level:
                        continue
                    conclusions.append(data)
            
            # 按时间排序
            conclusions.sort(key=lambda x: x.get('timestamp', ''))
            return conclusions
        except Exception as e:
            print(f"获取阶段性结论失败: {e}")
            return []
    
    def clear_results(self, analysis_id):
        """清除分析的所有中间结果
        
        Args:
            analysis_id: 分析ID
        """
        try:
            analysis_dir = os.path.join(self.storage_dir, analysis_id)
            if os.path.exists(analysis_dir):
                import shutil
                shutil.rmtree(analysis_dir)
            return True
        except Exception as e:
            print(f"清除中间结果失败: {e}")
            return False

# 全局存储实例
storage = IntermediateResultsStorage()