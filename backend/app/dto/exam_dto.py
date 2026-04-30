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
            id=exam.exam_code,
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


class StudentExamInfoDTO:
    """学生考试信息的DTO，包含学生参与考试的具体信息"""
    def __init__(self, exam_code: str, exam_name: str, academic_year: str, semester: str,
                 grade: str, exam_type: str, start_date: str, end_date: str, status: str,
                 subjects: list = None, average_score: float = None, total_subjects: int = 0,
                 exam_location: str = None, special_notes: str = None):
        self.exam_code = exam_code
        self.exam_name = exam_name
        self.academic_year = academic_year
        self.semester = semester
        self.grade = grade
        self.exam_type = exam_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.subjects = subjects or []
        self.average_score = average_score
        self.total_subjects = total_subjects
        self.exam_location = exam_location
        self.special_notes = special_notes

    def to_dict(self):
        """转换为字典"""
        return {
            'examCode': self.exam_code,
            'examName': self.exam_name,
            'academicYear': self.academic_year,
            'semester': self.semester,
            'grade': self.grade,
            'examType': self.exam_type,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'status': self.status,
            'subjects': self.subjects,
            'averageScore': self.average_score,
            'totalSubjects': self.total_subjects,
            'examLocation': self.exam_location,
            'specialNotes': self.special_notes
        }

    @classmethod
    def from_model(cls, exam, subjects: list = None, average_score: float = None,
                   total_subjects: int = 0, exam_location: str = None, special_notes: str = None):
        """从模型创建DTO"""
        return cls(
            exam_code=exam.exam_code,
            exam_name=exam.exam_name,
            academic_year=exam.academic_year,
            semester=exam.semester,
            grade=exam.grade,
            exam_type=exam.exam_type,
            start_date=exam.start_date.isoformat() if exam.start_date else None,
            end_date=exam.end_date.isoformat() if exam.end_date else None,
            status=exam.status,
            subjects=subjects,
            average_score=average_score,
            total_subjects=total_subjects,
            exam_location=exam_location,
            special_notes=special_notes
        )
