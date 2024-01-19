from PyQt5.QtCore import QThread, pyqtSignal
import json

class LoadMsgsThread(QThread):
    update_signal = pyqtSignal(list)

    def __init__(self, net, session_id):
        super(LoadMsgsThread, self).__init__()
        self.net = net
        self.session_id = session_id

    def run(self):
        while self.session_id:
            msgs = self.load_msgs()
            self.update_signal.emit(msgs)
            self.msleep(500)

    def load_msgs(self):
        self.net.send_to_server("0010", f"{self.session_id}")
        sv_status, sv_data = self.net.receive_from_server()
        if sv_status == "OK":
            try:
                msgs = json.loads(sv_data)
                return msgs
            except:
                pass
        elif str(sv_data) == "EMPTY":
            return []
        return []