from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import init_db

# 初始化数据库
init_db()

app = Flask(__name__)


# 数据库连接
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn


# 首页
@app.route('/')
def index():
    return render_template('index.html')


# 添加学生
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']

        conn = get_db_connection()
        conn.execute('INSERT INTO students (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_student.html')


# 添加成绩
@app.route('/add_grade/<int:student_id>', methods=['GET', 'POST'])
def add_grade(student_id):
    if request.method == 'POST':
        subject = request.form['subject']
        grade = request.form['grade']

        conn = get_db_connection()
        conn.execute('INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)', (student_id, subject, grade))
        conn.commit()
        conn.close()

        return redirect(url_for('view_grades', student_id=student_id))

    return render_template('add_grade.html', student_id=student_id)


# 查看学生成绩
@app.route('/view_grades/<int:student_id>')
def view_grades(student_id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    grades = conn.execute('SELECT * FROM grades WHERE student_id = ?', (student_id,)).fetchall()
    conn.close()

    # 计算平均成绩
    total_grades = sum(grade['grade'] for grade in grades)
    average_grade = total_grades / len(grades) if grades else 0

    return render_template('view_grades.html', student=student, grades=grades, average_grade=average_grade)


# 学生列表（按成绩排序）
@app.route('/student_list')
def student_list():
    conn = get_db_connection()
    students = conn.execute('''
        SELECT students.id, students.name, students.age, AVG(grades.grade) as avg_grade
        FROM students
        LEFT JOIN grades ON students.id = grades.student_id
        GROUP BY students.id
        ORDER BY avg_grade DESC
    ''').fetchall()
    conn.close()

    return render_template('student_list.html', students=students)


# 删除学生
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.execute('DELETE FROM grades WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('student_list'))


if __name__ == '__main__':
    app.run(debug=True)