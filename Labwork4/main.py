import curses  
import numpy as np
import zipfile
import os
from input_functions import input_student, input_course, input_mark, get_input_str  
from output_functions import list_course, list_student_sorted, load_students, load_courses, load_marks

DATA_FILES = ["students.txt", "courses.txt", "marks.txt"]
NAME = "students.dat"

def compress(filename = NAME):
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in DATA_FILES:
            if os.path.exists(file):
                zipf.write(file)

def decompress(filename = NAME):
    if os.path.exists(filename):
        with zipfile.ZipFile(filename, "r") as zipf:
            zipf.extractall()
        return True
    return False

def main_menu(stdscr):
    curses.curs_set(1) 

    while True:        
        stdscr.clear()  
        stdscr.addstr(1, 2, "=== STUDENT MANAGEMENT SYSTEM ===")  
        stdscr.addstr(3, 2, "1. Input Students")               
        stdscr.addstr(4, 2, "2. Input Courses")                 
        stdscr.addstr(5, 2, "3. Input Marks for Course")         
        stdscr.addstr(6, 2, "4. Show Course List")              
        stdscr.addstr(7, 2, "5. Show Students Sorted by GPA")    
        stdscr.addstr(8, 2, "6. Exit")                           
        
        choice = get_input_str(stdscr, 10, 2, "Your choice: ")  

        match choice:
            case '1':
                input_student(stdscr)
            case '2':
                input_course(stdscr)
            case '3':
                input_mark(stdscr)
            case '4':
                list_course(stdscr)
            case '5':
                list_student_sorted(stdscr)
            case '6':
                break            

if __name__ == "__main__":
    if decompress():
        load_courses()
        load_students()
        load_marks()

    try:
        curses.wrapper(main_menu)
    finally:
        compress()