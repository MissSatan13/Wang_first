import sqlite3


def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    # 创建学生表
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    class_name TEXT NOT NULL
                )''')

    # 创建成绩表
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    subject TEXT NOT NULL,
                    grade REAL NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students (id)
                )''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()