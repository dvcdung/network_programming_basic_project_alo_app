import mysql.connector
from datetime import datetime

class DB:
    # Thiết lập thông tin kết nối
    host = "localhost"  # Địa chỉ IP hoặc tên máy chủ của máy chủ MySQL (localhost nếu chạy trên máy cá nhân)
    user = "root"       # Tên người dùng MySQL
    password = ""       # Mật khẩu MySQL (thường để trống mật khẩu trong cấu hình mặc định của XAMPP)
    database = "alo_app_data"  # Tên của cơ sở dữ liệu bạn muốn kết nối

    def connect_db(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if connection.is_connected():
                return connection
        except mysql.connector.Error as error:
            print("Connection error:", error)
        return None
        
    def getUser(self, username, password):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = f"Select * from users where username = '{username}' and password = '{password}'"
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        else: return None

    def getUsers(self):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = "SELECT * FROM USERS"
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        else: return None


    def insertUser(self, user):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = "insert into users (username, password, display_name, phone) values (%s, %s, %s, %s)"
            val = [ (user[0], user[1], user[2], user[3]) ]
            cursor.executemany(query, val)
            connection.commit()

    def findUsers(self, key, user_id):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = f"SELECT SESSION_ID FROM PARTICIPATIONS WHERE USER_ID = {user_id}"
            cursor.execute(query)
            session_ids = [row[0] for row in cursor.fetchall()]
            if (session_ids):          
                query = "SELECT USER_ID FROM PARTICIPATIONS WHERE SESSION_ID = %s AND USER_ID <> %s"
                user_ids = []
                for session_id in session_ids:
                    cursor.execute(query, (session_id, user_id))
                    result = cursor.fetchall()
                    user_ids.extend([row[0] for row in result])
                
                # Lấy tất cả các người dùng khác user_id và thêm cột is_a_friend = 1 nếu user_id nằm trong user_ids
                query = f"SELECT *, CASE WHEN USER_ID IN ({', '.join(map(str, user_ids))}) THEN 1 ELSE 0 END AS is_a_friend FROM USERS WHERE USER_ID <> {user_id} AND (display_name like '%{key}%' OR phone like '%{key}%');"
            else:
                query = f"SELECT *, 0 AS is_a_friend FROM USERS WHERE USER_ID <> {user_id} AND (display_name like '%{key}%' OR phone like '%{key}%')"

            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        else: return None

    def addFriend(self, user_id_1, user_id_2):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = "INSERT INTO chat_sessions (session_name, folder_name) VALUES (%s, MD5(%s));"
            val = [("individual", str(datetime.now()))]
            cursor.executemany(query, val)
            connection.commit()
            
            session_id = cursor.lastrowid
            
            query1 = f"INSERT INTO `participations` (`user_id`, `session_id`) VALUES ({user_id_1}, {session_id}), ({user_id_2}, {session_id});"
            cursor.execute(query1)
            connection.commit()
            cursor.close()
            connection.close()

    def getChats(self, user_id):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = """SELECT 
                            c.session_id,
                            CASE 
                                WHEN c.session_name = 'individual' THEN u.display_name 
                                ELSE c.session_name
                            END AS session_name
                        FROM 
                            chat_sessions c
                            INNER JOIN participations p ON c.session_id = p.session_id
                            INNER JOIN users u ON u.user_id = p.user_id
                        WHERE 
                            p.user_id <> %s AND C.session_id IN (
                            SELECT participations.session_id FROM participations
                                INNER JOIN users ON participations.user_id = users.user_id
                                WHERE users.user_id = %s
                            );"""
            cursor.execute(query, (user_id, user_id))
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        else: return None

    def getMsgs(self, session_id):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = """SELECT M.*, U.display_name as sender_name 
                    FROM MESSAGES M 
                        inner join users U on M.sender_id = U.user_id 
                    WHERE SESSION_ID = %s
                    ORDER BY M.sent_at ASC"""
            cursor.execute(query, (session_id, ))
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        else: return None

    def insertMsg(self, message_text, sender_id, session_id):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = f"INSERT INTO `messages` (`message_text`, `sender_id`, `session_id`) VALUES (%s, %s, %s);"
            cursor.execute(query, (message_text, sender_id, session_id))
            connection.commit()
            cursor.close()
            connection.close()

db = DB()
db.insertMsg("Ê bạn ơi", 2, 43)