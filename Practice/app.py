import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MessageGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("📡 Simple CDP Messaging")
        self.setGeometry(300, 100, 500, 400)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Layouts
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        # Received messages display
        self.messages_box = QtWidgets.QTextEdit()
        self.messages_box.setReadOnly(True)
        self.messages_box.setStyleSheet(
            "background-color: #ffffff; font-size: 14px; padding: 10px; border-radius: 10px;"
        )
        self.messages_box.setPlaceholderText("Received messages will appear here...")
        main_layout.addWidget(self.messages_box)

        # Input layout
        input_layout = QtWidgets.QHBoxLayout()
        self.input_box = QtWidgets.QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet(
            "padding: 5px; font-size: 14px; border-radius: 10px; border: 1px solid #ccc;"
        )
        input_layout.addWidget(self.input_box)

        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 14px; padding: 5px 15px; border-radius: 10px;"
        )
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

    def send_message(self):
        message = self.input_box.text().strip()
        if message:
            # Append sent message to the display box
            self.messages_box.append(f"➡️ You: {message}")
            self.input_box.clear()

            # TODO: Here, you can call your GNU Radio send function
            # send_to_flowgraph(message)

    def receive_message(self, message):
        # Call this function to display received messages
        self.messages_box.append(f"📩 Received: {message}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = MessageGUI()
    gui.show()

    # Example of simulating received message after 3 seconds
    QtCore.QTimer.singleShot(3000, lambda: gui.receive_message("Hello from CDP flowgraph!"))

    sys.exit(app.exec_())
