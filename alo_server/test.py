import base64
from datetime import datetime as dt

def encode_string(input_string):
    encoded_string = base64.b64encode(input_string.encode()).decode()
    return encoded_string

def decode_string(input_string):
    encoded_string = base64.b64decode(input_string.encode()).decode()
    return encoded_string

# Chuỗi cần mã hóa
input_string = f"test.py|{dt.now()}"

# Lần đầu tiên
encoded_value_1 = encode_string(input_string)
print(f"The encoded value at time 1: {encoded_value_1}")

# Lần thứ hai (thời điểm khác nhau)
encoded_value_2 = decode_string(encoded_value_1)
print(f"The encoded value at time 2: {encoded_value_2}")
