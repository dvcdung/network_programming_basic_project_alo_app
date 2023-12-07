import base64
from datetime import datetime as dt
from database import DB


class FileService:
    def __init__(self):
        self.db = DB()

    def encode_string(self, input_string):
        encoded_string = base64.b64encode(input_string.encode()).decode()
        return encoded_string

    def decode_string(self, input_string):
        decoded_string = base64.b64decode(input_string.encode()).decode()
        return decoded_string
    
    def insert_file(self, file_name, sender_id, session_id):
        file_name = self.encode_string(f"{file_name}|{dt.now()}")
        query = f"INSERT INTO `resources` (`file_name`, `sender_id`, `session_id`) VALUES (%s, %s, %s);"
        self.db.insert(query, (file_name, sender_id, session_id))
        return file_name
    

