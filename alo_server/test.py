# import base64
# from datetime import datetime as dt

# def encode_string(input_string):
#     encoded_string = base64.b64encode(input_string.encode()).decode()
#     return encoded_string

# def decode_string(input_string):
#     encoded_string = base64.b64decode(input_string.encode()).decode()
#     return encoded_string

# # Chuỗi cần mã hóa
# input_string = f"test.py|{dt.now()}"

# # Lần đầu tiên
# encoded_value_1 = encode_string(input_string)
# print(f"The encoded value at time 1: {encoded_value_1}")

# # Lần thứ hai (thời điểm khác nhau)
# encoded_value_2 = decode_string(encoded_value_1)
# print(f"The encoded value at time 2: {encoded_value_2}")

# Mảng chứa các số nguyên
integer_array = [1, 2, 3, 4, 5]

# Sử dụng str() để chuyển mảng thành chuỗi
array_as_string = str(integer_array)

print(f"Mảng số nguyên dưới dạng chuỗi: {array_as_string}")

import json
# Sử dụng json.loads()
array_from_string = json.loads(array_as_string)

print(f"Chuỗi dưới dạng mảng số nguyên: {array_from_string[0]}")