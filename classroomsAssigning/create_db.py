
import sqlite3
import sys
import os
import atexit

DBExist = os.path.isfile('schedule.db')  # checks if file exists
dbcon = sqlite3.connect('schedule.db')
cursor = dbcon.cursor()


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def main(args):
    if not DBExist:
        create_tables()
        insert_data(args[1])
        print_tables()


def print_tables():
    print("courses")
    cursor.execute("SELECT * from courses")
    print_table(cursor.fetchall())
    print("classrooms")
    cursor.execute("SELECT * from classrooms")
    print_table(cursor.fetchall())
    print("students")
    cursor.execute("SELECT * from students")
    print_table(cursor.fetchall())


def insert_data(args):
    input_file_name = args
    os.path.isfile(input_file_name)  # checks if file exists
    with open(input_file_name) as inputFile:  # with == close the resources automatically,
        for line in inputFile:
            words = line.split(', ')
            for word in words:
                word.lstrip()
            if words[0] == 'S':
                insert_to_student(words)
            elif words[0] == 'R':
                insert_to_classrooms(words)
            elif words[0] == 'C':
                insert_to_courses(words)


def insert_to_student(words):
    grade = words[1]
    count = words[2][:len(words[2]) - 1]
    cursor.execute("INSERT INTO students VALUES(?,?)", [grade, count])


def insert_to_classrooms(words):
    id_ = words[1]
    location = words[2][:len(words[2]) - 1]
    cursor.execute("INSERT INTO classrooms VALUES (?,?,?,?)", [id_, location, 0, 0])


def insert_to_courses(words):
    _id = words[1]
    course_name = words[2]
    student = words[3]
    number_of_students = words[4]
    classroom_id = words[5]
    t = str(words[6]).find('\n')
    if t != -1:
        course_length = words[6][:len(words[6]) - 1]
    else:
        course_length = words[6]
    cursor.execute("INSERT INTO courses VALUES (?,?,?,?,?,?)",
                   [_id, course_name, student, number_of_students, classroom_id, course_length])


def create_tables():

    cursor.execute("CREATE TABLE courses(id INTEGER PRIMARY KEY, course_name TEXT NOT NULL, "
                   "student TEXT NOT NULL, number_of_students INTEGER NOT NULL, "
                   " class_id INTEGER REFERENCES  classrooms(id), course_length INTEGER NOT NULL )")

    cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY, count INTEGER NOT NULL)")

    cursor.execute("""CREATE TABLE classrooms(id INTEGER PRIMARY KEY, location TEXT NOT NULL, 
                   current_course_id INTEGER NOT NULL, current_course_time_left INTEGER NOT NULL )""")


def close_db():
    dbcon.commit()
    dbcon.close()


atexit.register(close_db)


if __name__ == '__main__':
    main(sys.argv)




