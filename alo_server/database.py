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
    
    def insert(self, query, params):
        connection = self.connect_db()
        if (connection):   
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            cursor.close()
            connection.close()
    
    def select(self, query, params):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            if params: cursor.execute(query, params)
            else: cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        else: return None

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
        query = "insert into users (username, password, display_name, phone) values (%s, %s, %s, %s)"
        self.insert(query, (user[0], user[1], user[2], user[3]))

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

    def getFriends(self, user_id):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = f"SELECT P.SESSION_ID FROM PARTICIPATIONS P INNER JOIN CHAT_SESSIONS C ON P.session_id = C.session_id WHERE USER_ID = {user_id} AND C.SESSION_NAME = 'individual'"
            cursor.execute(query)
            session_ids = [row[0] for row in cursor.fetchall()]
            if (session_ids):          
                query = "SELECT P.USER_ID, U.DISPLAY_NAME FROM PARTICIPATIONS P INNER JOIN USERS U ON P.USER_ID = U.USER_ID WHERE SESSION_ID = %s AND P.USER_ID <> %s"
                frientsFound = []
                for session_id in session_ids:
                    cursor.execute(query, (session_id, user_id))
                    result = cursor.fetchall()
                    frientsFound.append(result[0])
            cursor.close()
            connection.close()
            return frientsFound
        else: return None

    def createGroup(self, group_name, selected_friends):
        connection = self.connect_db()
        if (connection):
            cursor = connection.cursor()
            query = "INSERT INTO chat_sessions (session_name, folder_name) VALUES (%s, MD5(%s));"
            val = [(group_name, str(datetime.now()))]
            cursor.executemany(query, val)
            connection.commit()
            
            session_id = cursor.lastrowid

            query1 = "INSERT INTO `participations` (`user_id`, `session_id`) VALUES (%s, %s);"
            selected_friends = [(item, session_id) for item in selected_friends]
            cursor.executemany(query1, selected_friends)
            connection.commit()
            cursor.close()
            connection.close()

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
            query = """SELECT 'msg' as type, m.message_id as id, m.message_text as content,m.sender_id, u.display_name as sender_name, m.session_id, m.sent_at
                    FROM messages as m 
                        inner join users u on m.sender_id = u.user_id
                    WHERE m.session_id = %s
                    UNION
                    SELECT 'file' as type, r.file_id as id, r.file_name as content, r.sender_id, u.display_name as sender_name, r.session_id, r.sent_at
                    FROM resources r
                        inner join users u on r.sender_id = u.user_id
                    WHERE r.session_id = %s
                    ORDER BY sent_at ASC;"""
            cursor.execute(query, (session_id, session_id))
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return records
        else: return None

    def insertMsg(self, message_text, sender_id, session_id):
        query = f"INSERT INTO `messages` (`message_text`, `sender_id`, `session_id`) VALUES (%s, %s, %s);"
        self.insert(query, (message_text, sender_id, session_id))
    