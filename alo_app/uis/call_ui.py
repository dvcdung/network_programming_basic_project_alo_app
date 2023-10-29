import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2

class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.video_label = QLabel(self)  # Tạo QLabel để hiển thị video
        self.video_label.setAlignment(Qt.AlignCenter)  # Căn giữa nội dung QLabel

        vbox = QVBoxLayout(self)  # Sử dụng QVBoxLayout để tự động điều chỉnh kích thước QLabel
        vbox.addWidget(self.video_label)  # Thêm QLabel vào layout

        self.setLayout(vbox)  # Đặt layout cho cửa sổ chính

        self.video_capture = cv2.VideoCapture(0)  # Sử dụng camera mặc định (index 0)
        self.updateVideo()  # Gọi hàm cập nhật video

        self.setWindowTitle('Video Window')
        self.setGeometry(100, 100, 640, 480)
        self.show()

    def updateVideo(self):
        ret, frame = self.video_capture.read()  # Đọc khung hình từ camera
        if ret:
            # Chuyển đổi frame thành QImage để hiển thị trên QLabel
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

            # Tạo QPixmap từ QImage và hiển thị trên QLabel
            pixmap = QPixmap.fromImage(qImg)
            self.video_label.setPixmap(pixmap)

        # Lặp lại hàm cập nhật video sau 10ms
        self.video_label.repaint()  # Cần gọi repaint() để QLabel được vẽ lại khi cần
        self.video_label.update()
        self.repaint()  # Cũng cần gọi repaint() cho cửa sổ chính để đảm bảo việc vẽ lại

        # Gọi hàm cập nhật video sau 10ms
        self.video_label.repaint()
        self.video_label.update()
        self.repaint()
        self.timer = self.startTimer(10)  # Hàm startTimer sẽ gọi lại hàm timerEvent mỗi 10ms

    def timerEvent(self, event):
        self.updateVideo()  # Hàm này sẽ được gọi mỗi khi timer đến

    def closeEvent(self, event):
        self.video_capture.release()  # Giải phóng camera khi ứng dụng đóng

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoWindow()
    sys.exit(app.exec_())
