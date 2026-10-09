from domains import student_name, cs, marks
import numpy as np
import curses
import os

def load_students():
    if not os.path.exists("students.txt"):
        return

    student_name.clear()
    with open("students.txt", "r", encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Student ID"):
            continue

        parts = [part.strip() for part in line.split('|')]
        if len(parts) >= 3:
            sid, name, dob = parts[0], parts[1], parts[2]
            student_name.append({'id': sid, 'name': name, 'dob': dob})

def load_courses():
    if not os.path.exists("courses.txt"):
        return

    cs.clear()
    with open("courses.txt", "r", encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("ID"):
            continue

        parts = [part.strip() for part in line.split('|')]
        if len(parts) >= 3:
            try:
                c_id, name, credits = parts[0], parts[1], float(parts[2])
                cs[c_id] = {'name': name, 'credits': credits}
            except ValueError:
                continue

def load_marks():
    if not os.path.exists("marks.txt"):
        return
    pass

def calculate_student_gpa(student_id):
    student_marks = []
    course_credits = []

    for c_id, course_info in cs.items():
        if c_id in marks and student_id in marks[c_id]:
            student_marks.append(marks[c_id][student_id])
            if isinstance(course_info, dict):
                credits = course_info.get('credits', 0.0)  
            else:
                credits = 0.0
            course_credits.append(credits)

    if not course_credits or sum(course_credits) == 0:
        return 0.0

    np_marks = np.array(student_marks)
    np_credits = np.array(course_credits)

    weighted_gpa = np.sum(np_marks * np_credits) / np.sum(np_credits)
    return round(float(weighted_gpa), 2)

def save_gpa_to_file(sorted_indices, gpa_array):
    with open("marks.txt", "w", encoding='utf-8') as f:
        f.write(f"{'Student ID':<11} | {'Name':<40} | {'GPA':<5}\n")
        for idx in sorted_indices:
            s = student_name[idx]
            val = gpa_array[idx]
            f.write(f"{s['id']:<11} | {s['name']:<40} | {val:<5.2f}\n")

def list_course(x):
    x.clear()
    load_courses()

    max_y, max_x = x.getmaxyx()

    if not cs:
        x.addstr(1, 2, "No courses available!")
        x.addstr(min(3, max_y - 1), 2, "Press any key to return")
        x.getch()
        return

    x.addstr(1, 2, "Courses list")
    row = 3
    for cid, course in cs.items():
        if row >= max_y - 2:
            break
        x.addstr(row, 2, f"ID: {cid:<10} | Name: {course['name']:<25} | Credits: {course['credits']:<5}")
        row += 1

    prompt_row = min(row + 1, max_y - 1)
    x.addstr(prompt_row, 2, "Press any key to return")
    x.getch()

def list_student_sorted(x):
    x.clear()

    load_students()
    load_courses()
    
    max_y, max_x = x.getmaxyx()

    if not student_name:
        x.addstr(1, 2, "No students available!")
        x.addstr(min(3, max_y - 1), 2, "Press any key to return")
        x.getch()
        return

    gpa_list = []
    for s in student_name:
        s_gpa = calculate_student_gpa(s['id'])
        if s_gpa is None:
            s_gpa = 0.0
        gpa_list.append(s_gpa)

    gpa_array = np.array(gpa_list, dtype=float)
    sorted_indices = np.argsort(gpa_array)[::-1]

    save_gpa_to_file(sorted_indices, gpa_array)

    x.addstr(1, 2, "Students sorted by GPA")
    x.addstr(3, 2, f"{'Name':<20} | {'ID':<10} | {'GPA':<5}")
    x.addstr(4, 2, "-" * 42)

    row = 5
    for idx in sorted_indices:
        if row >= max_y - 2:
            break
        s = student_name[idx]
        val = gpa_array[idx]
        x.addstr(row, 2, f"{s['name']:<20} | {s['id']:<10} | {val:<5.2f}")
        row += 1

    prompt_row = min(row + 1, max_y - 1)
    x.addstr(prompt_row, 2, "GPAs updated in marks.txt! Press any key to return")
    x.getch()