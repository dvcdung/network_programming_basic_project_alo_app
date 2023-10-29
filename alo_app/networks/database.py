import mysql.connector

# Thiết lập thông tin kết nối
host = "localhost"  # Địa chỉ IP hoặc tên máy chủ của máy chủ MySQL (localhost nếu chạy trên máy cá nhân)
user = "root"       # Tên người dùng MySQL
password = ""       # Mật khẩu MySQL (thường để trống mật khẩu trong cấu hình mặc định của XAMPP)
database = "ten_cua_coi_so_du_lieu"  # Tên của cơ sở dữ liệu bạn muốn kết nối

# Tạo kết nối đến cơ sở dữ liệu
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Kết nối thành công vào cơ sở dữ liệu!")
        # Thực hiện các thao tác với cơ sở dữ liệu ở đây

except mysql.connector.Error as error:
    print("Lỗi kết nối:", error)

finally:
    # Đảm bảo rằng kết nối được đóng, ngay cả khi có lỗi xảy ra
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Kết nối đã đóng.")
