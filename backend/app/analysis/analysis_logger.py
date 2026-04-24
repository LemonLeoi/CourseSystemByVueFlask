# Analysis logger module
import json
import datetime
import os

class AnalysisLogger:
    """分析日志记录器"""
    
    def __init__(self, log_dir='e:/A_Course/backend/logs'):
        """初始化日志记录器
        
        Args:
            log_dir: 日志存储目录
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f'analysis_{datetime.datetime.now().strftime("%Y%m%d")}.json')
        self.logs = []
    
    def log(self, analysis_type, step, details, params=None, operator='system'):
        """记录分析日志
        
        Args:
            analysis_type: 分析类型（如'personal', 'class', 'grade'）
            step: 分析步骤（如'data_preprocessing', 'feature_engineering', 'model_training', 'result_generation'）
            details: 详细信息
            params: 使用的参数
            operator: 操作人员
        """
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'analysis_type': analysis_type,
            'step': step,
            'details': details,
            'params': params or {},
            'operator': operator
        }
        self.logs.append(log_entry)
        self._save_logs()
    
    def log_error(self, analysis_type, step, error_message, params=None, operator='system'):
        """记录错误日志
        
        Args:
            analysis_type: 分析类型
            step: 分析步骤
            error_message: 错误信息
            params: 使用的参数
            operator: 操作人员
        """
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'analysis_type': analysis_type,
            'step': step,
            'details': f'ERROR: {error_message}',
            'params': params or {},
            'operator': operator,
            'is_error': True
        }
        self.logs.append(log_entry)
        self._save_logs()
    
    def _save_logs(self):
        """保存日志到文件"""
        try:
            # 读取现有日志
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    existing_logs = json.load(f)
            else:
                existing_logs = []
            
            # 添加新日志
            existing_logs.extend(self.logs)
            
            # 保存到文件
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(existing_logs, f, ensure_ascii=False, indent=2)
            
            # 清空内存中的日志
            self.logs = []
        except Exception as e:
            print(f"保存日志失败: {e}")
    
    def get_logs(self, analysis_type=None, start_time=None, end_time=None):
        """获取日志
        
        Args:
            analysis_type: 分析类型
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            日志列表
        """
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # 过滤日志
            filtered_logs = logs
            if analysis_type:
                filtered_logs = [log for log in filtered_logs if log.get('analysis_type') == analysis_type]
            if start_time:
                filtered_logs = [log for log in filtered_logs if log.get('timestamp') >= start_time]
            if end_time:
                filtered_logs = [log for log in filtered_logs if log.get('timestamp') <= end_time]
            
            return filtered_logs
        except Exception as e:
            print(f"获取日志失败: {e}")
            return []
    
    def export_logs(self, output_file):
        """导出日志
        
        Args:
            output_file: 输出文件路径
        """
        try:
            logs = self.get_logs()
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出日志失败: {e}")
            return False

# 全局日志实例
logger = AnalysisLogger()