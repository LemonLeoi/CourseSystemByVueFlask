from datetime import date
from typing import Optional

class ExamCreateDTO:
    """创建考试的DTO"""
    def __init__(self, code: str, name: str, academicYear: str, semester: str, grade: str, type: str, startDate: str, endDate: str, status: str):
        self.code = code
        self.name = name
        self.academicYear = academicYear
        self.semester = semester
        self.grade = grade
        self.type = type
        self.startDate = startDate
        self.endDate = endDate
        self.status = status
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建DTO"""
        return cls(
            code=data.get('code'),
            name=data.get('name'),
            academicYear=data.get('academicYear', '2024-2025学年'),
            semester=data.get('semester', '第一学期'),
            grade=data.get('grade'),
            type=data.get('type'),
            startDate=data.get('startDate'),
            endDate=data.get('endDate'),
            status=data.get('status')
        )

class ExamUpdateDTO:
    """更新考试的DTO"""
    def __init__(self, name: Optional[str] = None, academicYear: Optional[str] = None, semester: Optional[str] = None, 
                 grade: Optional[str] = None, type: Optional[str] = None, startDate: Optional[str] = None, 
                 endDate: Optional[str] = None, status: Optional[str] = None):
        self.name = name
        self.academicYear = academicYear
        self.semester = semester
        self.grade = grade
        self.type = type
        self.startDate = startDate
        self.endDate = endDate
        self.status = status
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建DTO"""
        return cls(
            name=data.get('name'),
            academicYear=data.get('academicYear'),
            semester=data.get('semester'),
            grade=data.get('grade'),
            type=data.get('type'),
            startDate=data.get('startDate'),
            endDate=data.get('endDate'),
            status=data.get('status')
        )

class ExamResponseDTO:
    """考试响应的DTO"""
    def __init__(self, id: int, code: str, name: str, academicYear: str, semester: str, grade: str, type: str, 
                 startDate: str, endDate: str, status: str):
        self.id = id
        self.code = code
        self.name = name
        self.academicYear = academicYear
        self.semester = semester
        self.grade = grade
        self.type = type
        self.startDate = startDate
        self.endDate = endDate
        self.status = status
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'academicYear': self.academicYear,
            'semester': self.semester,
            'grade': self.grade,
            'type': self.type,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'status': self.status
        }
    
    @classmethod
    def from_model(cls, exam):
        """从模型创建DTO"""
        return cls(
            id=exam.id,
            code=exam.exam_code,
            name=exam.exam_name,
            academicYear=exam.academic_year,
            semester=exam.semester,
            grade=exam.grade,
            type=exam.exam_type,
            startDate=exam.start_date.isoformat() if exam.start_date else None,
            endDate=exam.end_date.isoformat() if exam.end_date else None,
            status=exam.status
        )
