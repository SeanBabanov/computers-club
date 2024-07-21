import socket
import threading
import sqlite3
 
thread_local_db = threading.local()   # מאחסן את החיבורים למס הנתונים לכל תרד
clients = []  # רשימת חיבורים של לקוחות

# פונקציה כדאי לעשות חיבור לכל טרד למסד הנתונים, כי למשהו אם לא לעשות את זה הכל קורס
def get_db():
    thread_local_db.connection = sqlite3.connect('messages.db')
    return thread_local_db.connection

# פונקציה לשמירת הודעות במסד הנתונים
def save_message_to_db(client_address, message):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO messages (client_address, message) VALUES (?, ?)", (client_address, message))
    db.commit()

# פונקציה לטיפול בלקוח
def handle_client(conn, addr):
    clients.append(conn)  # מוסיף את הלקוח לרשימת הלקוחות
    print(f"Connected by {addr}")

    while True:
        try:
            data = conn.recv(1024)  # מקבל נתונים מהלקוח
            if not data:
                break  # אם אין נתונים מנתק את החיבור
            message = data.decode()  # הופך נתונים לטקסט
            print(f"Received message from {addr}: {message}")
            save_message_to_db(addr[0], message)  # שומר הודעות במסד נתונים
            for client in clients:  # שליחת ההודעה לכל הלקוחות האחרים
                if client != conn:
                    try:
                        client.sendall(data)
                    except:
                        clients.remove(client)  # אם יש בעיה עם חיבור הלקוח מסיר אותו מהרשימה
        except Exception as e:  #מנתק חיבור אם יש תקלה
            print(f"Exception occurred: {e}")
            break
    conn.close()
    clients.remove(conn)  # מוחק לקוח מרשימה
    print(f"Connection with {addr} closed")

# פונקציה להפעלת השרת
def start_server(host='localhost', port=12345):
    db = get_db()  # פותח חיבור למסד נתונים
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))  # קישור השרת לכתובת ולפורט
        s.listen()  #בודק אם יש חיבורים חדשים
        print(f"Server has started, listening on {host}:{port}")
        while True:
            conn, addr = s.accept()  # מקבל חיבור חדש מלקוח
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()  # הפעלת תרד חדש ללקוח

if __name__ == "__main__":
    start_server()  # מפעיל את השרת
