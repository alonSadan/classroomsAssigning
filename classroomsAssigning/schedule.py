import os
import sqlite3
import atexit

dbcon = sqlite3.connect('schedule.db')
databaseexisted = os.path.isfile('schedule.db')
cursor = dbcon.cursor()


def main():

    cursor.execute("SELECT course_length FROM courses")
    numbersOfIterations = cursor.fetchall()
    x = max(numbersOfIterations)
    y = int(x[0])
    iternum = 0
    cursor.execute("SELECT id FROM classrooms")
    classrooms = cursor.fetchall()
    # stop when the db doesnt exist or all the iterations are done
    while databaseexisted & (y >= 0):  # class is occupied
        for classid in classrooms:
                cursor.execute("SELECT current_course_time_left FROM classrooms WHERE (id = ?) ", (int(classid[0]),))
                _course_time_left = cursor.fetchone()
                cursor.execute("SELECT location FROM classrooms WHERE (id = ?)", (int(classid[0]),))
                location = cursor.fetchone()
                cursor.execute("SELECT current_course_id FROM classrooms WHERE (id = ?)", (int(classid[0]),))
                current_course_id = cursor.fetchone()
                cursor.execute("SELECT course_name FROM courses WHERE (id = ?)", (int(current_course_id[0]),))
                current_course_name = cursor.fetchone()

                if int(_course_time_left[0]) > 0:  # class is occupied
                    cursor.execute(
                        "UPDATE classrooms SET current_course_time_left = ? WHERE (id = ?)",
                        (int(_course_time_left[0] - 1), int(classid[0]),))
                    cursor.execute("SELECT current_course_time_left FROM classrooms WHERE id = ? ", (int(classid[0]),))
                    _course_time_left = cursor.fetchone()
                    if _course_time_left[0] > 0:
                        print(
                            "(" + str(iternum) + ")" + " " + str(location[0]) + ": occupied by "
                            + str(current_course_name[0]))

                        # cursor.execute("SELECT current_course_time_left FROM classrooms WHERE (id = ?)",
                        # (int(classid[0]),))
                        # course_time_left = cursor.fetchone()
                    else:
                            print("(" + str(iternum) + ") " + str(location[0]) + ": " + str(current_course_name[0]) +
                                  " is done")
                            cursor.execute("DELETE FROM courses WHERE (id = ?)", (int(current_course_id[0]),))
                            cursor.execute("UPDATE classrooms SET current_course_time_left = ? WHERE (id = ?)",
                                           (0, int(classid[0])))
                            cursor.execute("UPDATE classrooms SET current_course_id = ? WHERE (id = ?) "
                                           , (0, int(classid[0])))
                            cursor.execute("SELECT course_length FROM courses WHERE (class_id = ?)",
                                           (int(classid[0]),))
                            add_to_iteration = cursor.fetchone()
                            if not(add_to_iteration is None):
                                if y < int(add_to_iteration[0]):
                                    t = int(add_to_iteration[0]) - y
                                    y = y + t
                                class_is_free(classid, iternum)

                else:
                    # class is free
                    # assign next course: find the next course with class_id=classid and update current_course_id
                    #                     find the student type with courseid, and do count = count - number_of_students
                    class_is_free(classid, iternum)

        print("courses")
        cursor.execute("SELECT * FROM courses")
        print_table(cursor.fetchall())
        print("classrooms")
        cursor.execute("SELECT * FROM classrooms")
        print_table(cursor.fetchall())
        print("students")
        cursor.execute("SELECT * FROM students")
        print_table(cursor.fetchall())
        y = y - 1
        iternum = iternum + 1


def class_is_free(classid, iternum):

    cursor.execute("SELECT id FROM courses WHERE (class_id = ?)", (int(classid[0]),))
    course_id = cursor.fetchone()
    if course_id is not None:
        cursor.execute("SELECT course_length FROM courses WHERE (id = ?)", (int(course_id[0]),))
        course_length = cursor.fetchone()
        cursor.execute("UPDATE classrooms SET current_course_id = ? WHERE id = ?",
                       (int(course_id[0]), int(classid[0])))
        cursor.execute("UPDATE classrooms SET current_course_time_left = ? WHERE id = ?",
                       (int(course_length[0]), int(classid[0])))
        cursor.execute("SELECT number_of_students FROM courses WHERE id = ?", (int(course_id[0]),))
        num_of_students = cursor.fetchone()
        cursor.execute("SELECT student FROM courses WHERE id = ?", (int(course_id[0]),))
        grade = cursor.fetchone()
        cursor.execute("SELECT count FROM students WHERE grade = ?", (str(grade[0]),))
        _count = cursor.fetchone()
        _count = int(_count[0] - num_of_students[0])
        cursor.execute("UPDATE students SET count = ? Where grade = ?", (_count, str(grade[0])))
        cursor.execute("SELECT location FROM classrooms WHERE (id = ?)", (int(classid[0]),))
        location = cursor.fetchone()
        cursor.execute("SELECT course_name FROM courses WHERE (id=? )", (int(course_id[0]),))
        course_name = cursor.fetchone()
        print("(" + str(iternum) + ") " + str(location[0]) + ": " + str(course_name[0])
              + " is schedule to start")


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def close_schedule():
    dbcon.commit()
    dbcon.close()


atexit.register(close_schedule)


if __name__ == '__main__':
    main()
