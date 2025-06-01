from db_connect import get_connection

def add_student(student_number, name, gender, major, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Students (StudentNumber, Name, Gender, Major, Phone, Email, Address) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (student_number, name, gender, major, phone, email, address)
    )
    conn.commit()
    conn.close()

def update_student(student_id, student_number, name, gender, major, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Students SET StudentNumber=?, Name=?, Gender=?, Major=?, Phone=?, Email=?, Address=? WHERE StudentID=?",
        (student_number, name, gender, major, phone, email, address, student_id)
    )
    conn.commit()
    conn.close()

def query_students(student_number=None, name=None, gender=None, major=None, phone=None, email=None, address=None):
    conn = get_connection()
    cursor = conn.cursor()
    conditions = []
    params = []
    if student_number:
        conditions.append("StudentNumber LIKE ?")
        params.append(f"%{student_number}%")
    if name:
        conditions.append("Name LIKE ?")
        params.append(f"%{name}%")
    if gender:
        conditions.append("Gender LIKE ?")
        params.append(f"%{gender}%")
    if major:
        conditions.append("Major LIKE ?")
        params.append(f"%{major}%")
    if phone:
        conditions.append("Phone LIKE ?")
        params.append(f"%{phone}%")
    if email:
        conditions.append("Email LIKE ?")
        params.append(f"%{email}%")
    if address:
        conditions.append("Address LIKE ?")
        params.append(f"%{address}%")
    sql = "SELECT * FROM Students"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Students WHERE StudentID=?", (student_id,))
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    rows = cursor.fetchall()
    conn.close()
    return rows