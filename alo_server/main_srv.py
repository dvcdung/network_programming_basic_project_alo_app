import os
import socket
import threading
import mysql
import json
from database import DB
from services.file_service import FileService

# Định nghĩa thư mục chứa dữ liệu của các tài khoản
DATA_DIR = "server_data"
IP_ADDR = "127.0.0.1"
PORT_NUM = 12345
db = DB()
jfs = FileService()
onlineUsers = {}

# Tạo thư mục chứa dữ liệu
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def handle_client(client_socket):
    try:
        while True:
            client_msg = client_socket.recv(2048).decode()
            if client_msg:
                (id, data) = client_msg.split(":", 1)
                if id == "0000": # Tạo tài khoản
                    username, password, displayname, phone = data.split("|", 3)
                    db.insertUser((username, password, displayname, phone))
                    client_socket.send("OK:Account successfully created".encode())
                elif id == "0001": # Đăng nhập
                    username, password = data.split("|", 1)
                    users = db.getUser(username, password)
                    if users and len(users) == 1:
                        userData = "|".join(list(map(str, users[0])))
                        client_socket.send(f"OK:{userData}".encode())
                        onlineUsers[username] = (client_socket, users[0])
                    else:
                        client_socket.send(f"ER:Failed".encode())
                    print(onlineUsers)
                elif id == "0003": # Đăng xuất
                    username = data
                    del onlineUsers[username]
                    print(f"Client named {username} is disconnected!\n")
                    client_socket.send(f"OK:Log out successfully!".encode())
                    print(onlineUsers)
                elif id == "0004": # Search users
                    key, user_id = data.split("|", 1)
                    usersFound = db.findUsers(key, user_id)
                    if (not usersFound):
                        client_socket.send("ER:EMPTY".encode())
                    else:
                        usersFound = [{"user_id": row[0],  "display_name": row[3], "is_a_friend": row[6]} for row in usersFound]
                        client_socket.send(f"OK:{json.dumps(usersFound)}".encode())
                elif id == "0005": # Add friend
                    user_id_1, user_id_2 = data.split("|", 1)
                    try:
                        db.addFriend(user_id_1, user_id_2)
                        client_socket.send("OK:Add friend successfully!")
                    except Exception:
                        client_socket.send("ER:Failed".encode())
                elif id == "0006": # Get chats
                    user_id = data
                    try:
                        chatsFound = db.getChats(user_id)
                        if (not chatsFound):
                            client_socket.send("ER:EMPTY".encode())
                        else:
                            chatsFound = [{"session_id": row[0],  "session_name": row[1], "is_a_friend": 1} for row in chatsFound]
                            client_socket.send(f"OK:{json.dumps(chatsFound)}".encode())
                    except Exception:
                        client_socket.send("ER:Failed".encode())
                elif id == "0010": # get Msgs
                    session_id = data
                    try:
                        msgs = db.getMsgs(session_id)
                        if (not msgs):
                            client_socket.send("ER:EMPTY".encode())
                        else:
                            msgs = [{"type": row[0],"id": row[1],  "content": row[2], "sender_id": row[3], "sender_name": row[4],  "session_id": row[5],  "sent_at": str(row[6])} for row in msgs]
                            client_socket.send(f"OK:{json.dumps(msgs)}".encode())
                    except Exception:
                        client_socket.send("ER:Failed".encode())
                elif id == "0011": # Send msg
                    message_text, sender_id, session_id = data.split("|")
                    try:
                        db.insertMsg(message_text, sender_id, session_id)
                        client_socket.send(f"OK:Insert successfully".encode())
                    except Exception:
                        client_socket.send("ER:Failed".encode())
                elif id == "0020": #Send file
                    file_name, file_size, sender_id, session_id = data.split("|")
                    try:
                        file_name = jfs.insert_file(file_name, sender_id, session_id)
                        received_data = 0
                        with open(f"./server_data/{file_name}", "wb") as file:
                            while received_data < int(file_size):
                                data = client_socket.recv(1024)
                                file.write(data)
                                received_data += len(data)
                        client_socket.send(f"OK:File sent successfully".encode())
                    except Exception as e:
                        print(e)
                        client_socket.send("ER:Failed".encode())
                elif id == "0021": #Download file
                    file_name = data
                    f_size = os.path.getsize(f"./server_data/{file_name}")
                    f_name = jfs.decode_string(file_name).split("|")[0]
                    client_socket.send(f"{f_name}|{f_size}".encode())
                    with open(f"./server_data/{file_name}", 'rb') as file:
                        for data in iter(lambda: file.read(1024), b''):
                            client_socket.send(data)
                
                    
    except ConnectionResetError:
        for username, (user_socket, _) in list(onlineUsers.items()):
            if (user_socket == client_socket):
                del onlineUsers[username]
                print(f"Client named {username} is disconnected!\n")
                break
    except mysql.connector.errors.IntegrityError:
        client_socket.send("ER:Failed".encode())

def server_main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_ADDR, PORT_NUM))
    server.listen(5)
    print(f"Server is listening at {IP_ADDR}:{PORT_NUM}")

    while True:
        client_socket, client_addr = server.accept()
        print(f"Chấp nhận kết nối từ {client_addr[0]}:{client_addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    server_main()