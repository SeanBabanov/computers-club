import socket
import threading

# פונקציה כדאי לקבל הודעות מהשרת
def receive_messages(s):
    while True:
            data = s.recv(1024)  # מקבל עד 1024 תווים מהשרת
            if not data:   # אם אין נתונים אז מסיים את הלולאה
                break
            print(f"Server: {data.decode()}")   # מדפיס את ההודעה שקיבל מהשרת

# פונקציה כדאי להתחבר לשרת ולשלוח הודעות
def connect_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # מתחבר לשרת בכתובת ופורט שצריך
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.start() # מתפעיל את התרד

        while True:
            message = input("Enter message, to exit enter 'exit': ")
            if message == 'exit':  # מנתק את המשתמש אם הוא כתב exit
                break
            s.sendall(message.encode()) # שולח את ההודעה לשרת

if __name__ == "__main__":
    connect_server()
