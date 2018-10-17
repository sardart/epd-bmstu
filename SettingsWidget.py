from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMessageBox,  QPushButton, QWidget, QComboBox, QGridLayout, QLabel
from PyQt5.QtCore import Qt
import os
import serial.tools.list_ports
import measurment
import serial.tools.list_ports


rootPath = os.getcwd()

speeds = ["921600", "9600", "19200"]

# CONSTANTS !!!!!
byteSize = ["5", "6", "7", "8"]
parity = ["Нет", "Чет", "Нечет"]
stopBits = ["1", "1.5", "2"]


class SettingsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setupUI()
        self.updateConnectedDevices()

    def setupUI(self):
        os.chdir(rootPath + "/icons")

        # Label's font
        boldFont = QFont()
        boldFont.setBold(True)
        boldFont.setPixelSize(14)

        titleFont = QFont()
        titleFont.setBold(True)
        titleFont.setPixelSize(18)

        italFont = QFont()
        italFont.setPixelSize(14)
        italFont.setItalic(True)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        titleLabel = QLabel("Настройки подключения")
        titleLabel.setFont(titleFont)
        titleLabel.setMaximumHeight(18)
        titleLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(titleLabel, 0, 1)


        deviceLabel = QLabel("Устройство")
        deviceLabel.setFont(boldFont)
        self.layout.addWidget(deviceLabel, 1, 0)

        self.devicesBox = QComboBox()
        self.layout.addWidget(self.devicesBox, 1, 1)


        refreshButton = QPushButton("Обновить")
        refreshButton.clicked.connect(self.updateConnectedDevices)
        refreshButton.setMaximumWidth(130)
        refreshButton.setMinimumWidth(130)
        refreshButton.setIcon(QIcon("refresh.png"))
        self.layout.addWidget(refreshButton, 1, 2)


        speedLabel = QLabel("Скорость")
        speedLabel.setFont(boldFont)
        self.layout.addWidget(speedLabel, 2, 0)

        self.speedBox = QComboBox()
        self.speedBox.addItems(speeds)
        self.layout.addWidget(self.speedBox, 2, 1)


        byteSizeLabel = QLabel("Размер байта")
        byteSizeLabel.setFont(boldFont)
        self.layout.addWidget(byteSizeLabel, 3, 0)

        self.byteSizeBox = QComboBox()
        self.byteSizeBox.addItems(byteSize)
        self.layout.addWidget(self.byteSizeBox, 3, 1)


        parityLabel = QLabel("Паритет")
        parityLabel.setFont(boldFont)
        self.layout.addWidget(parityLabel, 4, 0)

        self.parityBox = QComboBox()
        self.parityBox.addItems(parity)
        self.layout.addWidget(self.parityBox, 4, 1)


        stopBitsLabel = QLabel("Стоп-битов")
        stopBitsLabel.setFont(boldFont)
        self.layout.addWidget(stopBitsLabel, 5, 0)

        self.stopBitsBox = QComboBox()
        self.stopBitsBox.setMinimumWidth(390)
        self.stopBitsBox.addItems(stopBits)
        self.layout.addWidget(self.stopBitsBox, 5, 1)


        stateStaticLabel = QLabel("Состояние")
        stateStaticLabel.setFont(boldFont)
        stateStaticLabel.setMaximumHeight(70)
        self.layout.addWidget(stateStaticLabel, 6, 0)

        self.stateLabel = QLabel()
        self.stateLabel.setText("Отключено")
        self.stateLabel.setFont(italFont)
        self.layout.addWidget(self.stateLabel, 6, 1)


        self.startButton = QPushButton("Начать")
        self.startButton.setMaximumWidth(140)
        self.startButton.setMinimumWidth(140)
        self.startButton.setIcon(QIcon("bluetooth-on.png"))
        self.startButton.clicked.connect(self.startMeasurment)
        self.layout.addWidget(self.startButton, 6, 2)


        self.stopButton = QPushButton("Прервать")
        self.stopButton.setMaximumWidth(140)
        self.stopButton.setMinimumWidth(140)
        self.stopButton.setIcon(QIcon("bluetooth-off.png"))
        # self.disconnectButton.clicked.connect(self.stopMeasurment)
        self.stopButton.setHidden(True)
        self.layout.addWidget(self.stopButton, 6, 2)

        os.chdir(rootPath)

    def startMeasurment(self):
        selectedDevice = self.devicesBox.currentText()
        selectedSpeed = int(self.speedBox.currentText())
        # selectedStopBits = int(self.stop.currentText())
        # selectedByteSize = int(self.byteSizeBox.currentText())

        try:
            measurment.run(
                port=selectedDevice,
                speed=selectedSpeed
            )

        except Exception as error:
            print(error)
            QMessageBox.question(self, 'Уведомление',
                                 "Не удалось подключиться к %s" % selectedDevice, QMessageBox.Ok |
                                 QMessageBox.Ok)

    def updateConnectedDevices(self):
        self.devicesBox.clear()

        list = serial.tools.list_ports.comports()
        connected = []
        for element in list:
            connected.append(element.device)

        self.devicesBox.addItems(connected)
