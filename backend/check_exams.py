from app import create_app, db
from app.models import Exam

app = create_app()
with app.app_context():
    print('Exam count:', Exam.query.count())
    print('Exams:')
    for exam in Exam.query.all():
        print(f'  - {exam.exam_name} (code: {exam.exam_code})')
