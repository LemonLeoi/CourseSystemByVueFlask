import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db
from app.models import CourseSchedule

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py'), 'r', encoding='utf-8') as f:
    exec(f.read())

with app.app_context():
    db.create_all()
    print("Created course_schedules table successfully")