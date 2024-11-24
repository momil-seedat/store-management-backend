# utils.py

import random
from datetime import datetime

def generate_project_serial_number():
    current_year = datetime.now().year
    random_number = random.randint(1000, 9999)
    return f"PR{current_year}-{random_number}"

def generate_task_serial_number(project_serial):
    random_number = random.randint(1000, 9999)
    return f"TK{random.randint(10, 99)}-{project_serial}"
