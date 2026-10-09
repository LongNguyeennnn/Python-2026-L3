from domains import student_name, cs, marks
import numpy as np
import math
import curses
import os
from output_functions import list_course, list_student_sorted, load_marks, load_courses, load_students

def save_line(filename, line):
    with open(filename, "a", encoding='utf-8') as f:
        f.write(line + '\n')

def init_file(filename, header):
    if not os.path.exists(filename):
        save_line(filename, header)

init_file("students.txt", f"{'Student ID':<11} | {'Name':<40} | {'DOB':<12}")
init_file("courses.txt", f"{'ID':<10} | {'Course Name':<25} | {'Credits':<5}")
init_file("marks.txt", f"{'Student ID':<11} | {'Name':<40} | {'GPA':<5}")

def floor(val):
    return math.floor(val * 10) / 10.0

def safe_addstr(x, row, col, text):
    max_y, max_x = x.getmaxyx()
    if row < max_y and col < max_x:
        try:
            x.addstr(row, col, text[:max_x - col - 1])
        except curses.error:
            pass

def get_input_str(x, row, col, prompt):
    safe_addstr(x, row, col, prompt)
    x.refresh()
    curses.echo()
    input_val = x.getstr(row, col + len(prompt)).decode('utf-8')
    curses.noecho()
    return input_val

def input_student(x):
    x.clear()
    load_students()
    
    try:
        num = int(get_input_str(x, 1, 2, "Enter number of student: "))
    except ValueError:
        safe_addstr(x, 3, 2, "Invalid number! Press any key to return.")
        x.getch()
        return

    for _ in range(num):
        x.clear()
        safe_addstr(x, 1, 2, f'Student {_ + 1}/{num}')
        sid = get_input_str(x, 3, 2, "Student ID: ")
        name = get_input_str(x, 4, 2, "Student Name: ")
        dob = get_input_str(x, 5, 2, "Date of Birth: ")
        student_name.append({'id': sid, 'name': name, 'dob': dob})
        save_line("students.txt", f"{sid:<11} | {name:<40} | {dob:<12}")

def input_course(x):
    x.clear()
    load_courses()
    
    try:
        raw_num = get_input_str(x, 1, 2, "Enter number of courses: ")
        num = int(raw_num)
    except ValueError:
        safe_addstr(x, 3, 2, f"Invalid input '{raw_num}'! Please enter an integer number.")
        safe_addstr(x, 4, 2, "Press any key to return")
        x.getch()
        return

    for i in range(num):
        x.clear()
        safe_addstr(x, 1, 2, f"--- Course {i + 1}/{num} ---")
        c_id = get_input_str(x, 3, 2, "Course ID: ")   
        name = get_input_str(x, 4, 2, "Course Name: ")   
        
        try:
            credits = float(get_input_str(x, 5, 2, "Credits: ")) 
        except ValueError:
            safe_addstr(x, 7, 2, "Invalid credits value! Defaulting to 0.0")
            credits = 0.0

        cs[c_id] = {'name': name, 'credits': credits}
        save_line("courses.txt", f"{c_id:<10} | {name:<25} | {credits:<5}")

def input_mark(x):
    x.clear()

    load_courses()
    load_students()
    load_marks()

    max_y, max_x = x.getmaxyx()
    safe_addstr(x, 1, 2, "Input marks for the course.")
    if not cs:
        safe_addstr(x, 3, 2, "Do you want to add some courses?")
        safe_addstr(x, 5, 2, "Press any key to return")
        x.getch()
        return

    safe_addstr(x, 3, 2, "Available Courses:")
    safe_addstr(x, 4, 2, f"{'ID':<10} | {'Course Name':<25} | {'Credits':<5}")
    safe_addstr(x, 5, 2, "-" * 45)

    row = 6
    if isinstance(cs, dict):
        for c_id, course in cs.items():
            if row >= max_y - 3:
                break
            c_name = course.get('name', 'N/A') if isinstance(course, dict) else 'N/A'
            c_credits = course.get('credits', 0) if isinstance(course, dict) else 0
            safe_addstr(x, row, 2, f"{c_id:<10} | {c_name:<25} | {c_credits:<5}")
            row += 1

    row += 1
    if row >= max_y - 1:
        safe_addstr(x, max_y - 1, 2, "Screen full. Press any key to return.")
        x.getch()
        return

    c_id = get_input_str(x, row, 2, "Enter Course ID to input marks: ") 
    
    if c_id not in cs:
        safe_addstr(x, row + 2, 2, "Course ID does not exist! Press any key")
        x.getch()
        return

    if c_id not in marks:
        marks[c_id] = {}

    x.clear()
    safe_addstr(x, 1, 2, f"Enter the mark for course: {c_id}")

    row = 3
    for s in student_name:
        if row >= max_y - 1:
            break
        try:
            raw_mark = float(get_input_str(x, row, 2, f"Mark for {s['name']} (ID: {s['id']}): "))
        except ValueError:
            raw_mark = 0.0
        floored_mark = floor(raw_mark) 
        
        marks[c_id][s['id']] = floored_mark 
        row += 1

    prompt_row = min(row + 1, max_y - 1)
    safe_addstr(x, prompt_row, 2, "Marks inputted in memory! Show GPA sorted to generate marks.txt.")
    x.getch()