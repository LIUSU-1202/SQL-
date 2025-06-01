from db_connect import get_connection

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, password))
        conn.commit()
        result = True
    except Exception as e:
        result = False
    conn.close()
    return result

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Username=? AND Password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None