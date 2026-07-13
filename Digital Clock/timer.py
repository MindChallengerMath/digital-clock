from PySide6.QtWidgets import (
                                QApplication,
                                QLabel,
                                QVBoxLayout,
                                QWidget
                                )
from PySide6.QtGui import (QIcon)
from PySide6.QtCore import Qt, QTimer, QTime
import sys




class Clock(QWidget):
    def __init__(self):
        super().__init__()
        self.clockLabel = QLabel(self)
        self.clockTimer = QTimer(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Digital Clock")
        self.setWindowIcon(QIcon("images/clockIcon.png"))
        #self.clockLabel.setText("00:00:00")
        self.clockLabel.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
                            QLabel{
                           font-size: 200px;
                           font-family: Times New Roman;
                           color: #781901;
                           background-color: #676e6d;
                           }""")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.clockLabel)
        self.setLayout(self.vbox)
        self.clockTimer.timeout.connect(self.updateTime)
        self.clockTimer.start(1000)
    def updateTime(self):
        currentTime = QTime.currentTime().toString("hh:mm:ss")
        self.clockLabel.setText(currentTime)
        


def main():
    app = QApplication(sys.argv)
    clock = Clock()
    clock.setGeometry(250, 100, 1000, 600)
    clock.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()