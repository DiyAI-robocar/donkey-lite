import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QTabWidget, QLabel, 
    QComboBox, QTextEdit, QInputDialog, QLineEdit, QSlider, QCheckBox, QLCDNumber)  

# layouts
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


def create_slider():
    slider = QSlider()
    slider.setOrientation(Qt.Horizontal)
    slider.setFocusPolicy(Qt.StrongFocus)
    slider.setTickPosition(QSlider.TicksBothSides)
    slider.setMinimum(-100)
    slider.setMaximum(100)
    slider.setValue(0)
    slider.setSingleStep(20)
    return slider

 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'DonkeyLite'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
 
        self.show()
 

class TabCar(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.tab = QWidget()   
        self.tab.layout = QGridLayout(self)
        self.tab.layout.setSpacing(10)

        self.STEERING_CHANNEL_Edit = QLineEdit()
        self.STEERING_LEFT_PWM_Edit = QLineEdit()
        self.STEERING_RIGHT_PWM_Edit = QLineEdit()
        self.THROTTLE_CHANNEL_Edit = QLineEdit()
        self.THROTTLE_FORWARD_PWM_Edit = QLineEdit()
        self.THROTTLE_STOPPED_PWM_Edit = QLineEdit()
        self.THROTTLE_REVERSE_PWM_Edit = QLineEdit()

        self.button_ok = QPushButton("Ok")
        self.button_cancel = QPushButton("Cancel")

        self.tab.layout.addWidget(QLabel("STEERING_CHANNEL"), 2, 0)
        self.tab.layout.addWidget(self.STEERING_CHANNEL_Edit, 2, 1)
        self.tab.layout.addWidget(QLabel("STEERING_LEFT_PWM"), 3, 0)
        self.tab.layout.addWidget(self.STEERING_LEFT_PWM_Edit, 3, 1)
        self.tab.layout.addWidget(QLabel("STEERING_RIGHT_PWM"), 4, 0)
        self.tab.layout.addWidget(self.STEERING_RIGHT_PWM_Edit, 4, 1)
        self.tab.layout.addWidget(QLabel("THROTTLE_CHANNEL"), 5, 0)
        self.tab.layout.addWidget(self.THROTTLE_CHANNEL_Edit, 5, 1)
        self.tab.layout.addWidget(QLabel("THROTTLE_FORWARD_PWM"), 6, 0)
        self.tab.layout.addWidget(self.THROTTLE_FORWARD_PWM_Edit, 6, 1)
        self.tab.layout.addWidget(QLabel("THROTTLE_STOPPED_PWM"), 7, 0)
        self.tab.layout.addWidget(self.THROTTLE_STOPPED_PWM_Edit, 7, 1)
        self.tab.layout.addWidget(QLabel("THROTTLE_REVERSE_PWM"), 8, 0)
        self.tab.layout.addWidget(self.THROTTLE_REVERSE_PWM_Edit, 8, 1)

        self.tab.layout.addWidget(self.button_ok, 10, 2)
        self.tab.layout.addWidget(self.button_cancel, 10, 3)

        self.tab.setLayout(self.tab.layout)

    def run(self):
        return self.tab


class TabCamera(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.tab = QWidget()
        self.tab.layout = QHBoxLayout()

        self.image_layout = QVBoxLayout()
        self.image = QPixmap("./data/default.png")
        self.image_lable = QLabel()
        self.image_lable.setPixmap(self.image)

        self.button_make_image = QPushButton("Make image")
        self.image_layout.addWidget(self.image_lable)
        self.image_layout.addWidget(self.button_make_image)

        self.config_layout = QGridLayout()

        self.CAMERA_RESOLUTION_HIGH_Edit = QLineEdit()
        self.CAMERA_RESOLUTION_WIDTH_Edit = QLineEdit()
        self.CAMERA_FRAMERATE_Edit = QLineEdit()
        self.CAMERA_ZOOM_Edit = QLineEdit()
        self.CAMERA_COLORBALANCE_LENS_Edit = QLineEdit()
        self.CAMERA_COLORBALANCE_RGB_Edit = QLineEdit()
        self.CAMERA_COLORBALANCE_UV_Edit = QLineEdit()

        self.button_ok = QPushButton("Ok")
        self.button_cancel = QPushButton("Cancel")

        self.config_layout.addWidget(QLabel("CAMERA_RESOLUTION_HIGH"), 1, 0)
        self.config_layout.addWidget(self.CAMERA_RESOLUTION_HIGH_Edit, 1, 1)
        self.config_layout.addWidget(QLabel("CAMERA_RESOLUTION_WIDTH"), 2, 0)
        self.config_layout.addWidget(self.CAMERA_RESOLUTION_WIDTH_Edit, 2, 1)
        self.config_layout.addWidget(QLabel("CAMERA_FRAMERATE"), 3, 0)
        self.config_layout.addWidget(self.CAMERA_FRAMERATE_Edit, 3, 1)
        self.config_layout.addWidget(QLabel("CAMERA_ZOOM"), 4, 0)
        self.config_layout.addWidget(self.CAMERA_ZOOM_Edit, 4, 1)
        self.config_layout.addWidget(QLabel("CAMERA_COLORBALANCE_LENS"), 5, 0)
        self.config_layout.addWidget(self.CAMERA_COLORBALANCE_LENS_Edit, 5, 1)
        self.config_layout.addWidget(QLabel("CAMERA_COLORBALANCE_RGB"), 6, 0)
        self.config_layout.addWidget(self.CAMERA_COLORBALANCE_RGB_Edit, 6, 1)
        self.config_layout.addWidget(QLabel("CAMERA_COLORBALANCE_UV"), 7, 0)
        self.config_layout.addWidget(self.CAMERA_COLORBALANCE_UV_Edit, 7, 1)

        self.config_layout.addWidget(self.button_ok, 10, 2)
        self.config_layout.addWidget(self.button_cancel, 10, 3)

        self.tab.layout.addLayout(self.image_layout)
        self.tab.layout.addLayout(self.config_layout)
        self.tab.setLayout(self.tab.layout)

    def run(self):
        return self.tab


class TabDrive(QWidget):
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
        self.tab = QWidget()
        self.tab.layout = QGridLayout()

        self.driving_modes = QComboBox()
        self.driving_modes.addItem("user controlled")
        self.driving_modes.addItem("user controlls only angle")
        self.driving_modes.addItem("user controlls only speed")
        self.driving_modes.addItem("autopilot")

        self.driving_models = QComboBox()
        self.driving_models.addItem("None")
        self.driving_models.addItem("path to model 1")
        self.driving_models.addItem("path to model 2")
        self.driving_models.addItem("path to model 3")

        self.cb_keyboard = QCheckBox('KEYBOARD', self)
        self.cb_joystick = QCheckBox('JOYSTICK', self)

        self.slider_speed = create_slider()
        self.slider_speed_lcd_display = QLCDNumber(self)

        self.slider_angle = create_slider()
        self.slider_angle_lcd_display = QLCDNumber(self)

        self.tab.layout.addWidget(QLabel("DRIVING MODE"), 1, 0)
        self.tab.layout.addWidget(self.driving_modes, 2, 0)
        self.tab.layout.addWidget(QLabel("MODEL"), 3, 0)
        self.tab.layout.addWidget(self.driving_models, 4, 0)

        self.tab.layout.addWidget(QLabel("CONTROLLER"), 5, 0)
        self.tab.layout.addWidget(self.cb_keyboard, 6, 0)
        self.tab.layout.addWidget(self.cb_joystick, 7, 0)
        self.tab.layout.addWidget(QLabel("ANGLE VALUE"), 8, 0)
        self.tab.layout.addWidget(self.slider_angle_lcd_display, 8, 1)
        self.tab.layout.addWidget(self.slider_speed, 9, 0)
        self.tab.layout.addWidget(QLabel("SPEED VALUE"), 10, 0)
        self.tab.layout.addWidget(self.slider_speed_lcd_display, 10, 1)
        self.tab.layout.addWidget(self.slider_angle, 11, 0)

        self.tab.setLayout(self.tab.layout)

    def run(self):
        return self.tab


class MyTableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(QWidget, self).__init__(parent)
                
        self.le = QLineEdit(self)
        self.button1 = QPushButton("Connect")
        self.button2 = QPushButton("Stop")
        self.layout_address = QHBoxLayout()
        self.layout_address.addWidget(self.le)
        self.layout_address.addWidget(self.button1)
        self.layout_address.addWidget(self.button2)

        self.tabs = QTabWidget()
        self.tabs.resize(300,200)
        self.tabs.addTab(TabDrive(self).run(), "Drive")
        self.tabs.addTab(TabCar(self).run(),"Vehicle config")
        self.tabs.addTab(TabCamera(self).run(),"Camera config")

        self.layout_tab = QVBoxLayout()
        self.layout_tab.addWidget(self.tabs)

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.layout_address)
        self.layout.addLayout(self.layout_tab)
        self.setLayout(self.layout)

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
