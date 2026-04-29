# ETL状态管理模块
import json
import datetime
import os
import uuid
from typing import Dict, List, Optional, Any

class ETLStepStatus:
    """ETL步骤状态"""
    def __init__(self, step_name: str):
        self.step_name = step_name
        self.status: str = 'pending'  # pending, running, completed, failed
        self.progress: int = 0
        self.message: str = ''
        self.start_time: Optional[datetime.datetime] = None
        self.end_time: Optional[datetime.datetime] = None
        self.error: Optional[str] = None
    
    def start(self):
        self.status = 'running'
        self.start_time = datetime.datetime.now()
        self.progress = 0
    
    def update(self, progress: int, message: str = ''):
        self.progress = progress
        self.message = message
    
    def complete(self, message: str = ''):
        self.status = 'completed'
        self.progress = 100
        self.message = message
        self.end_time = datetime.datetime.now()
    
    def fail(self, error: str):
        self.status = 'failed'
        self.error = error
        self.end_time = datetime.datetime.now()
    
    def to_dict(self):
        return {
            'step_name': self.step_name,
            'status': self.status,
            'progress': self.progress,
            'message': self.message,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'error': self.error
        }

class ETLTask:
    """ETL任务"""
    def __init__(self, analysis_id: str, class_ids: List[str] = None, analysis_type: str = 'class'):
        self.analysis_id = analysis_id
        self.class_ids = class_ids or []
        self.analysis_type = analysis_type
        self.status: str = 'pending'  # pending, running, completed, failed
        self.current_step: str = ''
        self.progress: int = 0
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.error_message: Optional[str] = None
        
        # 定义ETL步骤
        self.steps: Dict[str, ETLStepStatus] = {
            'extract': ETLStepStatus('数据提取'),
            'transform': ETLStepStatus('数据转换'),
            'load': ETLStepStatus('数据加载'),
            'mining': ETLStepStatus('数据挖掘')
        }
    
    def start_step(self, step_name: str):
        if step_name in self.steps:
            self.current_step = step_name
            self.steps[step_name].start()
            self.status = 'running'
            self.updated_at = datetime.datetime.now()
    
    def update_step(self, step_name: str, progress: int, message: str = ''):
        if step_name in self.steps:
            self.steps[step_name].update(progress, message)
            self.progress = self.calculate_overall_progress()
            self.updated_at = datetime.datetime.now()
    
    def complete_step(self, step_name: str, message: str = ''):
        if step_name in self.steps:
            self.steps[step_name].complete(message)
            self.progress = self.calculate_overall_progress()
            self.updated_at = datetime.datetime.now()
            
            # 检查是否所有步骤都完成
            if all(step.status == 'completed' for step in self.steps.values()):
                self.status = 'completed'
    
    def fail_step(self, step_name: str, error: str):
        if step_name in self.steps:
            self.steps[step_name].fail(error)
            self.status = 'failed'
            self.error_message = error
            self.updated_at = datetime.datetime.now()
    
    def calculate_overall_progress(self) -> int:
        """计算总体进度"""
        step_weights = {
            'extract': 20,
            'transform': 25,
            'load': 20,
            'mining': 35
        }
        
        total = 0
        for step_name, step in self.steps.items():
            weight = step_weights.get(step_name, 25)
            if step.status == 'completed':
                total += weight
            elif step.status == 'running':
                total += weight * step.progress / 100
        
        return int(total)
    
    def to_dict(self):
        return {
            'analysis_id': self.analysis_id,
            'class_ids': self.class_ids,
            'analysis_type': self.analysis_type,
            'status': self.status,
            'current_step': self.current_step,
            'progress': self.progress,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'error_message': self.error_message,
            'steps': {name: step.to_dict() for name, step in self.steps.items()}
        }

class ETLManager:
    """ETL管理器"""
    
    def __init__(self, storage_dir='e:/A_Course/backend/etl_tasks'):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.tasks: Dict[str, ETLTask] = {}
        self._load_tasks()
    
    def _load_tasks(self):
        """加载已保存的任务"""
        try:
            for file_name in os.listdir(self.storage_dir):
                if file_name.endswith('.json'):
                    file_path = os.path.join(self.storage_dir, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        task = ETLTask(
                            analysis_id=data['analysis_id'],
                            class_ids=data.get('class_ids', []),
                            analysis_type=data.get('analysis_type', 'class')
                        )
                        task.status = data['status']
                        task.current_step = data['current_step']
                        task.progress = data['progress']
                        task.created_at = datetime.datetime.fromisoformat(data['created_at'])
                        task.updated_at = datetime.datetime.fromisoformat(data['updated_at'])
                        task.error_message = data.get('error_message')
                        
                        # 加载步骤状态
                        for step_name, step_data in data.get('steps', {}).items():
                            if step_name in task.steps:
                                task.steps[step_name].status = step_data['status']
                                task.steps[step_name].progress = step_data['progress']
                                task.steps[step_name].message = step_data['message']
                                task.steps[step_name].error = step_data.get('error')
                                if step_data['start_time']:
                                    task.steps[step_name].start_time = datetime.datetime.fromisoformat(step_data['start_time'])
                                if step_data['end_time']:
                                    task.steps[step_name].end_time = datetime.datetime.fromisoformat(step_data['end_time'])
                        
                        self.tasks[data['analysis_id']] = task
        except Exception as e:
            print(f"加载ETL任务失败: {e}")
    
    def _save_task(self, task: ETLTask):
        """保存任务到文件"""
        try:
            file_path = os.path.join(self.storage_dir, f"{task.analysis_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(task.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存ETL任务失败: {e}")
            return False
    
    def create_task(self, class_ids: List[str], analysis_type: str = 'class') -> str:
        """创建ETL任务
        
        Args:
            class_ids: 班级ID列表
            analysis_type: 分析类型
            
        Returns:
            analysis_id: 分析任务ID
        """
        analysis_id = str(uuid.uuid4())[:8] + '_' + datetime.datetime.now().strftime("%Y%m%d")
        task = ETLTask(analysis_id, class_ids, analysis_type)
        self.tasks[analysis_id] = task
        self._save_task(task)
        return analysis_id
    
    def get_task(self, analysis_id: str) -> Optional[ETLTask]:
        """获取任务
        
        Args:
            analysis_id: 分析任务ID
            
        Returns:
            ETLTask对象或None
        """
        return self.tasks.get(analysis_id)
    
    def update_task(self, analysis_id: str, updates: Dict[str, Any]) -> bool:
        """更新任务
        
        Args:
            analysis_id: 分析任务ID
            updates: 更新内容
            
        Returns:
            是否更新成功
        """
        task = self.tasks.get(analysis_id)
        if not task:
            return False
        
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.datetime.now()
        self._save_task(task)
        return True
    
    def start_step(self, analysis_id: str, step_name: str) -> bool:
        """开始执行步骤
        
        Args:
            analysis_id: 分析任务ID
            step_name: 步骤名称
            
        Returns:
            是否成功
        """
        task = self.tasks.get(analysis_id)
        if not task:
            return False
        
        task.start_step(step_name)
        self._save_task(task)
        return True
    
    def update_step_progress(self, analysis_id: str, step_name: str, progress: int, message: str = '') -> bool:
        """更新步骤进度
        
        Args:
            analysis_id: 分析任务ID
            step_name: 步骤名称
            progress: 进度(0-100)
            message: 进度消息
            
        Returns:
            是否成功
        """
        task = self.tasks.get(analysis_id)
        if not task:
            return False
        
        task.update_step(step_name, progress, message)
        self._save_task(task)
        return True
    
    def complete_step(self, analysis_id: str, step_name: str, message: str = '') -> bool:
        """完成步骤
        
        Args:
            analysis_id: 分析任务ID
            step_name: 步骤名称
            message: 完成消息
            
        Returns:
            是否成功
        """
        task = self.tasks.get(analysis_id)
        if not task:
            return False
        
        task.complete_step(step_name, message)
        self._save_task(task)
        return True
    
    def fail_step(self, analysis_id: str, step_name: str, error: str) -> bool:
        """步骤失败
        
        Args:
            analysis_id: 分析任务ID
            step_name: 步骤名称
            error: 错误信息
            
        Returns:
            是否成功
        """
        task = self.tasks.get(analysis_id)
        if not task:
            return False
        
        task.fail_step(step_name, error)
        self._save_task(task)
        return True
    
    def delete_task(self, analysis_id: str) -> bool:
        """删除任务
        
        Args:
            analysis_id: 分析任务ID
            
        Returns:
            是否成功
        """
        if analysis_id not in self.tasks:
            return False
        
        # 删除内存中的任务
        del self.tasks[analysis_id]
        
        # 删除文件
        file_path = os.path.join(self.storage_dir, f"{analysis_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return True
    
    def list_tasks(self, status: str = None) -> List[ETLTask]:
        """列出任务
        
        Args:
            status: 任务状态过滤（可选）
            
        Returns:
            任务列表
        """
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        # 按更新时间排序
        tasks.sort(key=lambda t: t.updated_at, reverse=True)
        return tasks

# 全局ETL管理器实例
etl_manager = ETLManager()