from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import re
import json
import os

class PyPyWorker(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.process = None
        self._stop_requested = False

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8"
            )

            for line in self.process.stdout:
                if self._stop_requested:
                    self.process.terminate()
                    break
                self.output_signal.emit(line.strip())
            self.process.stdout.close()
            self.process.wait()
            if self._stop_requested:
                self.output_signal.emit("Остановка процесса по запросу пользователя.")

        except Exception as e:
            self.output_signal.emit(f"Ошибка: {e}")

    def stop(self):
        self._stop_requested = True
        if self.process and self.process.poll() is None:
            self.process.terminate()

class Ui_Main(object):
    def __init__(self):
        super().__init__()
        self.config_file_path = ""

    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(1900, 1020)
        font = QtGui.QFont()
        font.setPointSize(10)
        Main.setFont(font)
        Main.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(Main)
        self.centralwidget.setStyleSheet("background-color: rgb(23, 23, 35);")
        self.centralwidget.setObjectName("centralwidget")
        self.label_dekod = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.label_dekod.setGeometry(QtCore.QRect(15, 830, 570, 180))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_dekod.setFont(font)
        self.label_dekod.setStyleSheet("QPlainTextEdit {\n"
                                       "color: rgb(255, 255, 255);\n"
                                       "background-color: rgb(33, 33, 45);\n"
                                       "border: 5px solid;\n"
                                       "border-color: rgb(124, 124, 124);\n"
                                       "border-radius: 20px;\n"
                                       "padding:10px 10px 10px 10px\n"
                                       "}\n"
                                       "")
        self.label_dekod.setReadOnly(True)
        self.label_dekod.setObjectName("label_dekod")
        self.label_kod = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.label_kod.setGeometry(QtCore.QRect(15, 220, 570, 570))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_kod.setFont(font)
        self.label_kod.setStyleSheet("QPlainTextEdit {\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "background-color: rgb(33, 33, 45);\n"
                                     "border: 5px solid;\n"
                                     "border-color: rgb(124, 124, 124);\n"
                                     "border-radius: 20px ;\n"
                                     "padding:10px 10px 10px 10px\n"
                                     "}\n"
                                     "\n"
                                     "")
        self.label_kod.setReadOnly(True)
        self.label_kod.setObjectName("label_kod")
        self.Button_dekod = QtWidgets.QPushButton(self.centralwidget)
        self.Button_dekod.setGeometry(QtCore.QRect(180, 775, 250, 70))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Button_dekod.setFont(font)
        self.Button_dekod.setStyleSheet("QPushButton {\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(33, 33, 85);\n"
                                        "border: 6px solid;\n"
                                        "border-color:  rgb(154, 160, 231);\n"
                                        "border-radius: 30px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "border: 3px solid;\n"
                                        "background-color: rgb(12, 12, 52);\n"
                                        "border-color:  rgb(154, 160, 231);\n"
                                        "border-radius: 30px;\n"
                                        "transition: background-color 0.5s ease;\n"
                                        "}\n"
                                        "\n"
                                        "\n"
                                        "")
        self.Button_dekod.setIconSize(QtCore.QSize(50, 50))
        self.Button_dekod.setAutoRepeatInterval(100)
        self.Button_dekod.setObjectName("Button_dekod")
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setGeometry(QtCore.QRect(600, 10, 3, 1000))
        self.line_1.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.line_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.comboBox_kod = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_kod.setGeometry(QtCore.QRect(100, 70, 400, 45))
        self.comboBox_kod.setStyleSheet("QComboBox {\n"
                                        "font-size: 14px;\n"
                                        "background-color: rgb(220, 220, 220);\n"
                                        "border: 3px solid;\n"
                                        "border-color: rgb(124, 124, 124);\n"
                                        "border-radius: 5px;\n"
                                        "padding:5px 5px 5px 5px;\n"
                                        "color: black;\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox:hover {\n"
                                        "font-size: 14px;\n"
                                        "background-color: rgb(220, 220, 220);\n"
                                        "border: 3px solid;\n"
                                        "border-color: rgb(1, 130, 100);\n"
                                        "border-radius: 5px;\n"
                                        "padding:5px 5px 5px 5px\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox  QAbstractItemView {\n"
                                        "background-color: rgb(220, 220, 220);\n"
                                        "}\n"
                                        "                                  \n"
                                        "\n"
                                        "                                   ")
        self.comboBox_kod.setObjectName("comboBox_kod")
        self.comboBox_kod.addItem("")
        self.comboBox_kod.addItem("")
        self.lineEdit_bits = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_bits.setGeometry(QtCore.QRect(50, 130, 500, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_bits.setFont(font)
        self.lineEdit_bits.setWhatsThis("")
        self.lineEdit_bits.setStyleSheet("QLineEdit {\n"
                                         "background-color: rgb(33, 33, 45);\n"
                                         "border: 3px solid;\n"
                                         "border-color:  rgb(1, 130, 100);\n"
                                         "border-radius: 10px;\n"
                                         "padding:2px 2px 2px 2px;\n"
                                         "color: grey;\n"
                                         "}\n"
                                         "\n"
                                         "QLineEdit:hover {\n"
                                         "background-color: rgb(33, 33, 45);\n"
                                         "border: 3px solid;\n"
                                         "border-color: rgb(154, 160, 231);\n"
                                         "border-radius: 10px;\n"
                                         "padding:2px 2px 2px 2px\n"
                                         "}")
        self.lineEdit_bits.setText("")
        self.lineEdit_bits.setFrame(True)
        self.lineEdit_bits.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_bits.setObjectName("lineEdit_bits")
        self.label_name_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_name_1.setGeometry(QtCore.QRect(175, 20, 330, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name_1.setFont(font)
        self.label_name_1.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_name_1.setObjectName("label_name_1")
        self.Button_kod = QtWidgets.QPushButton(self.centralwidget)
        self.Button_kod.setGeometry(QtCore.QRect(180, 175, 250, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Button_kod.setFont(font)
        self.Button_kod.setStyleSheet("QPushButton {\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(33, 33, 85);\n"
                                      "border: 6px solid;\n"
                                      "border-color:  rgb(154, 160, 231);\n"
                                      "border-radius: 30px;\n"
                                      "padding:3px 3px 3px 3px;\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "border: 3px solid;\n"
                                      "background-color: rgb(12, 12, 52);\n"
                                      "border-color:  rgb(154, 160, 231);\n"
                                      "border-radius: 30px;\n"
                                      "transition: background-color 0.5s ease;\n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "")
        self.Button_kod.setIconSize(QtCore.QSize(18, 18))
        self.Button_kod.setAutoRepeatInterval(100)
        self.Button_kod.setObjectName("Button_kod")
        self.label_name_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_name_2.setGeometry(QtCore.QRect(680, 20, 660, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name_2.setFont(font)
        self.label_name_2.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_name_2.setObjectName("label_name_2")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(1400, 10, 3, 1000))
        self.line_2.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.checkBox_save_test_res = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_save_test_res.setGeometry(QtCore.QRect(1420, 405, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_save_test_res.setFont(font)
        self.checkBox_save_test_res.setAcceptDrops(False)
        self.checkBox_save_test_res.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_save_test_res.setAutoFillBackground(False)
        self.checkBox_save_test_res.setStyleSheet("QCheckBox {\n"
                                                  "padding:2px 2px 2px 2px;\n"
                                                  "color: grey;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QCheckBox:hover {\n"
                                                  "padding:2px 2px 2px 2px;\n"
                                                  "color: rgb(1, 130, 100);\n"
                                                  "}")
        self.checkBox_save_test_res.setIconSize(QtCore.QSize(16, 16))
        self.checkBox_save_test_res.setObjectName("checkBox_save_test_res")
        self.checkBox_multi = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_multi.setGeometry(QtCore.QRect(625, 250, 330, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_multi.setFont(font)
        self.checkBox_multi.setAcceptDrops(False)
        self.checkBox_multi.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_multi.setAutoFillBackground(False)
        self.checkBox_multi.setStyleSheet("QCheckBox {\n"
                                                  "padding:2px 2px 2px 2px;\n"
                                                  "color: grey;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QCheckBox:hover {\n"
                                                  "padding:2px 2px 2px 2px;\n"
                                                  "color: rgb(1, 130, 100);\n"
                                                  "}")
        self.checkBox_multi.setIconSize(QtCore.QSize(16, 16))
        self.checkBox_multi.setObjectName("checkBox_multi")
        self.checkBox_multi_test = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_multi_test.setGeometry(QtCore.QRect(1420, 330, 330, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_multi_test.setFont(font)
        self.checkBox_multi_test.setAcceptDrops(False)
        self.checkBox_multi_test.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_multi_test.setAutoFillBackground(False)
        self.checkBox_multi_test.setStyleSheet("QCheckBox {\n"
                                                  "padding:2px 2px 2px 2px;\n"
                                                  "color: grey;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QCheckBox:hover {\n"
                                                  "padding:2px 2px 2px 2px;\n"
                                                  "color: rgb(1, 130, 100);\n"
                                                  "}")
        self.checkBox_multi_test.setIconSize(QtCore.QSize(16, 16))
        self.checkBox_multi_test.setObjectName("checkBox_multi_test")
        self.comboBox_dekod_al = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_dekod_al.setGeometry(QtCore.QRect(630, 100, 280, 45))
        self.comboBox_dekod_al.setStyleSheet("QComboBox {\n"
                                             "font-size: 14px;\n"
                                             "background-color: rgb(220, 220, 220);\n"
                                             "border: 3px solid;\n"
                                             "border-color: rgb(124, 124, 124);\n"
                                             "border-radius: 5px;\n"
                                             "padding:5px 5px 5px 5px;\n"
                                             "color: black;\n"
                                             "}\n"
                                             "\n"
                                             "QComboBox:hover {\n"
                                             "font-size: 14px;\n"
                                             "background-color: rgb(220, 220, 220);\n"
                                             "border: 3px solid;\n"
                                             "border-color: rgb(1, 130, 100);\n"
                                             "border-radius: 5px;\n"
                                             "padding:5px 5px 5px 5px\n"
                                             "}\n"
                                             "\n"
                                             "QComboBox  QAbstractItemView {\n"
                                             "background-color: rgb(220, 220, 220);\n"
                                             "}\n"
                                             "                                  \n"
                                             "\n"
                                             "                                   ")
        self.comboBox_dekod_al.setObjectName("comboBox_dekod_al")
        self.comboBox_dekod_al.addItem("")
        self.comboBox_dekod_al.addItem("")
        self.comboBox_dekod_al.addItem("")
        self.label_evrist = QtWidgets.QLabel(self.centralwidget)
        self.label_evrist.setGeometry(QtCore.QRect(640, 70, 130, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_evrist.setFont(font)
        self.label_evrist.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_evrist.setObjectName("label_evrist")
        self.comboBox_dekod_al_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_dekod_al_2.setGeometry(QtCore.QRect(940, 100, 180, 45))
        self.comboBox_dekod_al_2.setStyleSheet("QComboBox {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(124, 124, 124);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px;\n"
                                               "color: black;\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox:hover {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(1, 130, 100);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox  QAbstractItemView {\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "}\n"
                                               "                                  \n"
                                               "\n"
                                               "                                   ")
        self.comboBox_dekod_al_2.setObjectName("comboBox_dekod_al_2")
        self.comboBox_dekod_al_2.addItem("")
        self.comboBox_dekod_al_2.addItem("")
        self.label_crossover = QtWidgets.QLabel(self.centralwidget)
        self.label_crossover.setGeometry(QtCore.QRect(940, 70, 100, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_crossover.setFont(font)
        self.label_crossover.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_crossover.setObjectName("label_crossover")
        self.label_populations = QtWidgets.QLabel(self.centralwidget)
        self.label_populations.setGeometry(QtCore.QRect(1150, 70, 220, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_populations.setFont(font)
        self.label_populations.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_populations.setObjectName("label_populations")
        self.comboBox_dekod_al_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_dekod_al_3.setGeometry(QtCore.QRect(1150, 100, 220, 45))
        self.comboBox_dekod_al_3.setStyleSheet("QComboBox {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(124, 124, 124);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px;\n"
                                               "color: black;\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox:hover {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(1, 130, 100);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox  QAbstractItemView {\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "}\n"
                                               "                                  \n"
                                               "\n"
                                               "                                   ")
        self.comboBox_dekod_al_3.setObjectName("comboBox_dekod_al_3")
        self.comboBox_dekod_al_3.addItem("")
        self.comboBox_dekod_al_3.addItem("")
        self.lineEdit_count_populations = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_count_populations.setGeometry(QtCore.QRect(820, 155, 80, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_count_populations.setFont(font)
        self.lineEdit_count_populations.setWhatsThis("")
        self.lineEdit_count_populations.setStyleSheet("QLineEdit {\n"
                                                      "background-color: rgb(33, 33, 45);\n"
                                                      "border: 3px solid;\n"
                                                      "border-color:  rgb(1, 130, 100);\n"
                                                      "border-radius: 10px;\n"
                                                      "padding:2px 2px 2px 2px;\n"
                                                      "color: grey;\n"
                                                      "}\n"
                                                      "\n"
                                                      "QLineEdit:hover {\n"
                                                      "background-color: rgb(33, 33, 45);\n"
                                                      "border: 3px solid;\n"
                                                      "border-color: rgb(154, 160, 231);\n"
                                                      "border-radius: 10px;\n"
                                                      "padding:2px 2px 2px 2px\n"
                                                      "}")
        self.lineEdit_count_populations.setText("")
        self.lineEdit_count_populations.setFrame(True)
        self.lineEdit_count_populations.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_count_populations.setPlaceholderText("")
        self.lineEdit_count_populations.setObjectName("lineEdit_count_populations")
        self.lineEdit_count_generat = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_count_generat.setGeometry(QtCore.QRect(1050, 155, 80, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_count_generat.setFont(font)
        self.lineEdit_count_generat.setWhatsThis("")
        self.lineEdit_count_generat.setStyleSheet("QLineEdit {\n"
                                                  "background-color: rgb(33, 33, 45);\n"
                                                  "border: 3px solid;\n"
                                                  "border-color: rgb(1, 130, 100);\n"
                                                  "border-radius: 10px;\n"
                                                  "padding:2px 2px 2px 2px;\n"
                                                  "color: grey;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QLineEdit:hover {\n"
                                                  "background-color: rgb(33, 33, 45);\n"
                                                  "border: 3px solid;\n"
                                                  "border-color: rgb(154, 160, 231);\n"
                                                  "border-radius: 10px;\n"
                                                  "padding:2px 2px 2px 2px\n"
                                                  "}")
        self.lineEdit_count_generat.setText("")
        self.lineEdit_count_generat.setFrame(True)
        self.lineEdit_count_generat.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_count_generat.setPlaceholderText("")
        self.lineEdit_count_generat.setObjectName("lineEdit_count_generat")
        self.lineEdit_rate_mut = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_rate_mut.setGeometry(QtCore.QRect(1320, 155, 60, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_rate_mut.setFont(font)
        self.lineEdit_rate_mut.setWhatsThis("")
        self.lineEdit_rate_mut.setStyleSheet("QLineEdit {\n"
                                             "background-color: rgb(33, 33, 45);\n"
                                             "border: 3px solid;\n"
                                             "border-color:  rgb(1, 130, 100);\n"
                                             "border-radius: 10px;\n"
                                             "padding:2px 2px 2px 2px;\n"
                                             "color: grey;\n"
                                             "}\n"
                                             "\n"
                                             "QLineEdit:hover {\n"
                                             "background-color: rgb(33, 33, 45);\n"
                                             "border: 3px solid;\n"
                                             "border-color: rgb(154, 160, 231);\n"
                                             "border-radius: 10px;\n"
                                             "padding:2px 2px 2px 2px\n"
                                             "}")
        self.lineEdit_rate_mut.setText("")
        self.lineEdit_rate_mut.setFrame(True)
        self.lineEdit_rate_mut.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_rate_mut.setPlaceholderText("")
        self.lineEdit_rate_mut.setObjectName("lineEdit_rate_mut")
        self.lineEdit_rate_mut_evr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_rate_mut_evr.setGeometry(QtCore.QRect(905, 205, 60, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_rate_mut_evr.setFont(font)
        self.lineEdit_rate_mut_evr.setWhatsThis("")
        self.lineEdit_rate_mut_evr.setStyleSheet("QLineEdit {\n"
                                                 "background-color: rgb(33, 33, 45);\n"
                                                 "border: 3px solid;\n"
                                                 "border-color:  rgb(1, 130, 100);\n"
                                                 "border-radius: 10px;\n"
                                                 "padding:2px 2px 2px 2px;\n"
                                                 "color: grey;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QLineEdit:hover {\n"
                                                 "background-color: rgb(33, 33, 45);\n"
                                                 "border: 3px solid;\n"
                                                 "border-color:rgb(154, 160, 231);\n"
                                                 "border-radius: 10px;\n"
                                                 "padding:2px 2px 2px 2px\n"
                                                 "}")
        self.lineEdit_rate_mut_evr.setText("")
        self.lineEdit_rate_mut_evr.setFrame(True)
        self.lineEdit_rate_mut_evr.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_rate_mut_evr.setPlaceholderText("")
        self.lineEdit_rate_mut_evr.setObjectName("lineEdit_rate_mut_evr")
        self.lineEdit_evrist_n = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_evrist_n.setGeometry(QtCore.QRect(1120, 205, 80, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_evrist_n.setFont(font)
        self.lineEdit_evrist_n.setWhatsThis("")
        self.lineEdit_evrist_n.setStyleSheet("QLineEdit {\n"
                                             "background-color: rgb(33, 33, 45);\n"
                                             "border: 3px solid;\n"
                                             "border-color:  rgb(1, 130, 100);\n"
                                             "border-radius: 10px;\n"
                                             "padding:2px 2px 2px 2px;\n"
                                             "color: grey;\n"
                                             "}\n"
                                             "\n"
                                             "QLineEdit:hover {\n"
                                             "background-color: rgb(33, 33, 45);\n"
                                             "border: 3px solid;\n"
                                             "border-color:rgb(154, 160, 231);\n"
                                             "border-radius: 10px;\n"
                                             "padding:2px 2px 2px 2px\n"
                                             "}")
        self.lineEdit_evrist_n.setText("")
        self.lineEdit_evrist_n.setFrame(True)
        self.lineEdit_evrist_n.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_evrist_n.setPlaceholderText("")
        self.lineEdit_evrist_n.setObjectName("lineEdit_evrist_n")
        self.label_count_populations = QtWidgets.QLabel(self.centralwidget)
        self.label_count_populations.setGeometry(QtCore.QRect(630, 160, 190, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_count_populations.setFont(font)
        self.label_count_populations.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_count_populations.setObjectName("label_count_populations")
        self.label_count_generat = QtWidgets.QLabel(self.centralwidget)
        self.label_count_generat.setGeometry(QtCore.QRect(910, 160, 135, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_count_generat.setFont(font)
        self.label_count_generat.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_count_generat.setObjectName("label_count_generat")
        self.label_rate_mut = QtWidgets.QLabel(self.centralwidget)
        self.label_rate_mut.setGeometry(QtCore.QRect(1150, 160, 165, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_rate_mut.setFont(font)
        self.label_rate_mut.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_rate_mut.setObjectName("label_rate_mut")
        self.label_count_populations_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_count_populations_2.setGeometry(QtCore.QRect(630, 210, 275, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_count_populations_2.setFont(font)
        self.label_count_populations_2.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_count_populations_2.setObjectName("label_count_populations_2")
        self.label_evrist_n = QtWidgets.QLabel(self.centralwidget)
        self.label_evrist_n.setGeometry(QtCore.QRect(980, 210, 130, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_evrist_n.setFont(font)
        self.label_evrist_n.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_evrist_n.setObjectName("label_evrist_n")
        self.label_decrypt_al = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.label_decrypt_al.setGeometry(QtCore.QRect(620, 330, 760, 680))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_decrypt_al.setFont(font)
        self.label_decrypt_al.setStyleSheet("QPlainTextEdit {\n"
                                            "color: rgb(255, 255, 255);\n"
                                            "background-color: rgb(33, 33, 45);\n"
                                            "border: 5px solid;\n"
                                            "border-color: rgb(124, 124, 124);\n"
                                            "border-radius: 20px ;\n"
                                            "padding:10px 10px 10px 10px\n"
                                            "}\n"
                                            "\n"
                                            "")
        self.label_decrypt_al.setReadOnly(True)
        self.label_decrypt_al.setObjectName("label_decrypt_al")
        self.Button_decrypt_al = QtWidgets.QPushButton(self.centralwidget)
        self.Button_decrypt_al.setGeometry(QtCore.QRect(875, 285, 250, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Button_decrypt_al.setFont(font)
        self.Button_decrypt_al.setStyleSheet("QPushButton {\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "border: 6px solid;\n"
                                             "background-color: rgb(33, 33, 85);\n"
                                             "border-color:  rgb(154, 160, 231);\n"
                                             "border-radius: 30px;\n"
                                             "padding:3px 3px 3px 3px;\n"
                                             "}\n"
                                             "\n"
                                             "\n"
                                             "QPushButton:hover {\n"
                                             "border: 3px solid;\n"
                                             "background-color: rgb(12, 12, 52);\n"
                                             "border-color:  rgb(154, 160, 231);\n"
                                             "border-radius: 30px;\n"
                                             "transition: background-color 0.5s ease;\n"
                                             "}\n"
                                             "\n"
                                             "\n"
                                             "")
        self.Button_decrypt_al.setIconSize(QtCore.QSize(18, 18))
        self.Button_decrypt_al.setAutoRepeatInterval(100)
        self.Button_decrypt_al.setObjectName("Button_decrypt_al")
        self.label_name_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_name_3.setGeometry(QtCore.QRect(1550, 20, 200, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_name_3.setFont(font)
        self.label_name_3.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_name_3.setObjectName("label_name_3")
        self.comboBox_dekod_al_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_dekod_al_4.setGeometry(QtCore.QRect(1620, 270, 270, 45))
        self.comboBox_dekod_al_4.setStyleSheet("QComboBox {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(124, 124, 124);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px;\n"
                                               "color: black;\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox:hover {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(1, 130, 100);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox  QAbstractItemView {\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "}\n"
                                               "                                  \n"
                                               "\n"
                                               "                                   ")
        self.comboBox_dekod_al_4.setObjectName("comboBox_dekod_al_4")
        self.comboBox_dekod_al_4.addItem("")
        self.comboBox_dekod_al_4.addItem("")
        self.comboBox_dekod_al_4.addItem("")
        self.label_evrist_test = QtWidgets.QLabel(self.centralwidget)
        self.label_evrist_test.setGeometry(QtCore.QRect(1760, 240, 130, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_evrist_test.setFont(font)
        self.label_evrist_test.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_evrist_test.setObjectName("label_evrist_test")
        self.label_populations_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_populations_2.setGeometry(QtCore.QRect(1420, 240, 220, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_populations_2.setFont(font)
        self.label_populations_2.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_populations_2.setObjectName("label_populations_2")
        self.comboBox_dekod_al_5 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_dekod_al_5.setGeometry(QtCore.QRect(1420, 270, 160, 45))
        self.comboBox_dekod_al_5.setStyleSheet("QComboBox {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(124, 124, 124);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px;\n"
                                               "color: black;\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox:hover {\n"
                                               "font-size: 14px;\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "border: 3px solid;\n"
                                               "border-color: rgb(1, 130, 100);\n"
                                               "border-radius: 5px;\n"
                                               "padding:5px 5px 5px 5px\n"
                                               "}\n"
                                               "\n"
                                               "QComboBox  QAbstractItemView {\n"
                                               "background-color: rgb(220, 220, 220);\n"
                                               "}\n"
                                               "                                  \n"
                                               "\n"
                                               "                                   ")
        self.comboBox_dekod_al_5.setObjectName("comboBox_dekod_al_5")
        self.comboBox_dekod_al_5.addItem("")
        self.comboBox_dekod_al_5.addItem("")
        self.lineEdit_count_test = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_count_test.setGeometry(QtCore.QRect(1580, 155, 80, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_count_test.setFont(font)
        self.lineEdit_count_test.setWhatsThis("")
        self.lineEdit_count_test.setStyleSheet("QLineEdit {\n"
                                               "background-color: rgb(33, 33, 45);\n"
                                               "border: 3px solid;\n"
                                               "border-color:  rgb(1, 130, 100);\n"
                                               "border-radius: 10px;\n"
                                               "padding:2px 2px 2px 2px;\n"
                                               "color: grey;\n"
                                               "}\n"
                                               "\n"
                                               "QLineEdit:hover {\n"
                                               "background-color: rgb(33, 33, 45);\n"
                                               "border: 3px solid;\n"
                                               "border-color:rgb(154, 160, 231);\n"
                                               "border-radius: 10px;\n"
                                               "padding:2px 2px 2px 2px\n"
                                               "}")
        self.lineEdit_count_test.setText("")
        self.lineEdit_count_test.setFrame(True)
        self.lineEdit_count_test.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_count_test.setPlaceholderText("")
        self.lineEdit_count_test.setObjectName("lineEdit_count_test")
        self.lineEdit_len = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_len.setGeometry(QtCore.QRect(1580, 195, 80, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_len.setFont(font)
        self.lineEdit_len.setWhatsThis("")
        self.lineEdit_len.setStyleSheet("QLineEdit {\n"
                                               "background-color: rgb(33, 33, 45);\n"
                                               "border: 3px solid;\n"
                                               "border-color:  rgb(1, 130, 100);\n"
                                               "border-radius: 10px;\n"
                                               "padding:2px 2px 2px 2px;\n"
                                               "color: grey;\n"
                                               "}\n"
                                               "\n"
                                               "QLineEdit:hover {\n"
                                               "background-color: rgb(33, 33, 45);\n"
                                               "border: 3px solid;\n"
                                               "border-color:rgb(154, 160, 231);\n"
                                               "border-radius: 10px;\n"
                                               "padding:2px 2px 2px 2px\n"
                                               "}")
        self.lineEdit_len.setText("")
        self.lineEdit_len.setFrame(True)
        self.lineEdit_len.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_len.setPlaceholderText("")
        self.lineEdit_len.setObjectName("lineEdit_len")
        self.label_count_test = QtWidgets.QLabel(self.centralwidget)
        self.label_count_test.setGeometry(QtCore.QRect(1420, 160, 155, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_count_test.setFont(font)
        self.label_count_test.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_count_test.setObjectName("label_count_test")
        self.label_len = QtWidgets.QLabel(self.centralwidget)
        self.label_len.setGeometry(QtCore.QRect(1420, 200, 155, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_len.setFont(font)
        self.label_len.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_len.setObjectName("label_len")
        self.Button_load_test_params = QtWidgets.QPushButton(self.centralwidget)
        self.Button_load_test_params.setGeometry(QtCore.QRect(1710, 80, 170, 100))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Button_load_test_params.setFont(font)
        self.Button_load_test_params.setStyleSheet("QPushButton {\n"
                                                   "color: rgb(255, 255, 255);\n"
                                                   "border: 6px solid;\n"
                                                   "border-color:  rgb(154, 160, 231);\n"
                                                   "border-radius: 30px;\n"
                                                   "background-color: rgb(33, 33, 85);\n"
                                                   "padding:3px 3px 3px 3px;\n"
                                                   "}\n"
                                                   "\n"
                                                   "\n"
                                                   "QPushButton:hover {\n"
                                                   "border: 3px solid;\n"
                                                   "background-color: rgb(12, 12, 52);\n"
                                                   "border-color:  rgb(154, 160, 231);\n"
                                                   "border-radius: 30px;\n"
                                                   "transition: background-color 0.5s ease;\n"
                                                   "}\n"
                                                   "\n"
                                                   "\n"
                                                   "")
        self.Button_load_test_params.setIconSize(QtCore.QSize(18, 18))
        self.Button_load_test_params.setAutoRepeatInterval(100)
        self.Button_load_test_params.setObjectName("Button_load_test_params")
        self.label_test = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.label_test.setGeometry(QtCore.QRect(1420, 490, 460, 350))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_test.setFont(font)
        self.label_test.setStyleSheet("QPlainTextEdit {\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(33, 33, 45);\n"
                                      "border: 5px solid;\n"
                                      "border-color: rgb(124, 124, 124);\n"
                                      "border-radius: 20px;\n"
                                      "padding:10px 10px 10px 10px\n"
                                      "}\n"
                                      "")
        self.label_test.setReadOnly(True)
        self.label_test.setObjectName("label_test")
        self.Button_test_run = QtWidgets.QPushButton(self.centralwidget)
        self.Button_test_run.setGeometry(QtCore.QRect(1470, 445, 210, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Button_test_run.setFont(font)
        self.Button_test_run.setStyleSheet("QPushButton {\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border: 6px solid;\n"
                                           "background-color: rgb(33, 33, 85);\n"
                                           "border-color:  rgb(154, 160, 231);\n"
                                           "border-radius: 30px;\n"
                                           "padding:3px 3px 3px 3px;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "border: 3px solid;\n"
                                           "background-color: rgb(12, 12, 52);\n"
                                           "border-color:  rgb(154, 160, 231);\n"
                                           "border-radius: 30px;\n"
                                           "transition: background-color 0.5s ease;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "")
        self.Button_test_run.setIconSize(QtCore.QSize(18, 18))
        self.Button_test_run.setAutoRepeatInterval(100)
        self.Button_test_run.setObjectName("Button_test_run")

        self.Button_test_stop = QtWidgets.QPushButton(self.centralwidget)
        self.Button_test_stop.setGeometry(QtCore.QRect(1700, 445, 150, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Button_test_stop.setFont(font)
        self.Button_test_stop.setStyleSheet("QPushButton {\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border: 5px solid;\n"
                                           "background-color: rgb(240, 0, 0);\n"
                                           "border-color:  rgb(154, 160, 231);\n"
                                           "border-radius: 30px;\n"
                                           "padding:3px 3px 3px 3px;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "QPushButton:hover {\n"
                                           "border: 3px solid;\n"
                                           "background-color: rgb(180, 0, 0);\n"
                                           "border-color:  rgb(154, 160, 231);\n"
                                           "border-radius: 30px;\n"
                                           "transition: background-color 0.5s ease;\n"
                                           "}\n"
                                           "\n"
                                           "\n"
                                           "")
        self.Button_test_stop.setIconSize(QtCore.QSize(18, 18))
        self.Button_test_stop.setAutoRepeatInterval(100)
        self.Button_test_stop.setObjectName("Button_test_stop")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(1415, 850, 470, 3))
        self.line.setStyleSheet("background-color: rgb(83, 83, 83);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.Button_view_test_res = QtWidgets.QPushButton(self.centralwidget)
        self.Button_view_test_res.setGeometry(QtCore.QRect(1475, 910, 350, 80))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.Button_view_test_res.setFont(font)
        self.Button_view_test_res.setStyleSheet("QPushButton {\n"
                                                "color: rgb(255, 255, 255);\n"
                                                "border: 5px solid;\n"
                                                "border-color:  rgb(154, 160, 231);\n"
                                                "background-color: rgb(33, 33, 85);\n"
                                                "border-radius: 30px;\n"
                                                "padding:3px 3px 3px 3px;\n"
                                                "}\n"
                                                "\n"
                                                "\n"
                                                "QPushButton:hover {\n"
                                                "border: 3px solid;\n"
                                                "background-color: rgb(1, 130, 100);\n"
                                                "border-color:  rgb(154, 160, 231);\n"
                                                "border-radius: 30px;\n"
                                                "transition: background-color 0.5s ease;\n"
                                                "}\n"
                                                "\n"
                                                "\n"
                                                "")
        self.Button_view_test_res.setIconSize(QtCore.QSize(18, 18))
        self.Button_view_test_res.setAutoRepeatInterval(100)
        self.Button_view_test_res.setObjectName("Button_view_test_res")
        self.label_view_test_res = QtWidgets.QLabel(self.centralwidget)
        self.label_view_test_res.setGeometry(QtCore.QRect(1470, 860, 360, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_view_test_res.setFont(font)
        self.label_view_test_res.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_view_test_res.setObjectName("label_view_test_res")
        self.label_evrist_n_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_evrist_n_2.setGeometry(QtCore.QRect(1420, 370, 130, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_evrist_n_2.setFont(font)
        self.label_evrist_n_2.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_evrist_n_2.setObjectName("label_evrist_n_2")
        self.lineEdit_save_file = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_save_file.setGeometry(QtCore.QRect(1550, 365, 320, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_save_file.setFont(font)
        self.lineEdit_save_file.setWhatsThis("")
        self.lineEdit_save_file.setStyleSheet("QLineEdit {\n"
                                              "background-color: rgb(33, 33, 45);\n"
                                              "border: 3px solid;\n"
                                              "border-color:  rgb(1, 130, 100);\n"
                                              "border-radius: 10px;\n"
                                              "padding:2px 2px 2px 2px;\n"
                                              "color: grey;\n"
                                              "}\n"
                                              "\n"
                                              "QLineEdit:hover {\n"
                                              "background-color: rgb(33, 33, 45);\n"
                                              "border: 3px solid;\n"
                                              "border-color: rgb(154, 160, 231);\n"
                                              "border-radius: 10px;\n"
                                              "padding:2px 2px 2px 2px\n"
                                              "}")
        self.lineEdit_save_file.setText("")
        self.lineEdit_save_file.setFrame(True)
        self.lineEdit_save_file.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_save_file.setPlaceholderText("")
        self.lineEdit_save_file.setObjectName("lineEdit_save_file")
        self.lineEdit_count_generat_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_count_generat_2.setGeometry(QtCore.QRect(1565, 115, 80, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_count_generat_2.setFont(font)
        self.lineEdit_count_generat_2.setWhatsThis("")
        self.lineEdit_count_generat_2.setStyleSheet("QLineEdit {\n"
                                                    "background-color: rgb(33, 33, 45);\n"
                                                    "border: 3px solid;\n"
                                                    "border-color: rgb(1, 130, 100);\n"
                                                    "border-radius: 10px;\n"
                                                    "padding:2px 2px 2px 2px;\n"
                                                    "color: grey;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLineEdit:hover {\n"
                                                    "background-color: rgb(33, 33, 45);\n"
                                                    "border: 3px solid;\n"
                                                    "border-color: rgb(154, 160, 231);\n"
                                                    "border-radius: 10px;\n"
                                                    "padding:2px 2px 2px 2px\n"
                                                    "}")
        self.lineEdit_count_generat_2.setText("")
        self.lineEdit_count_generat_2.setFrame(True)
        self.lineEdit_count_generat_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_count_generat_2.setPlaceholderText("")
        self.lineEdit_count_generat_2.setObjectName("lineEdit_count_generat_2")
        self.lineEdit_count_populations_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_count_populations_2.setGeometry(QtCore.QRect(1610, 75, 80, 35))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_count_populations_2.setFont(font)
        self.lineEdit_count_populations_2.setWhatsThis("")
        self.lineEdit_count_populations_2.setStyleSheet("QLineEdit {\n"
                                                        "background-color: rgb(33, 33, 45);\n"
                                                        "border: 3px solid;\n"
                                                        "border-color:  rgb(1, 130, 100);\n"
                                                        "border-radius: 10px;\n"
                                                        "padding:2px 2px 2px 2px;\n"
                                                        "color: grey;\n"
                                                        "}\n"
                                                        "\n"
                                                        "QLineEdit:hover {\n"
                                                        "background-color: rgb(33, 33, 45);\n"
                                                        "border: 3px solid;\n"
                                                        "border-color: rgb(154, 160, 231);\n"
                                                        "border-radius: 10px;\n"
                                                        "padding:2px 2px 2px 2px\n"
                                                        "}")
        self.lineEdit_count_populations_2.setText("")
        self.lineEdit_count_populations_2.setFrame(True)
        self.lineEdit_count_populations_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_count_populations_2.setPlaceholderText("")
        self.lineEdit_count_populations_2.setObjectName("lineEdit_count_populations_2")
        self.label_count_generat_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_count_generat_2.setGeometry(QtCore.QRect(1420, 120, 135, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_count_generat_2.setFont(font)
        self.label_count_generat_2.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_count_generat_2.setObjectName("label_count_generat_2")
        self.label_count_populations_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_count_populations_3.setGeometry(QtCore.QRect(1420, 80, 190, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_count_populations_3.setFont(font)
        self.label_count_populations_3.setStyleSheet("color:rgb(212, 212, 212)")
        self.label_count_populations_3.setObjectName("label_count_populations_3")
        Main.setCentralWidget(self.centralwidget)

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

        # Кнопки
        self.Button_kod.clicked.connect(self.encrypt_qui)
        self.Button_dekod.clicked.connect(self.decrypt_qui)
        self.Button_decrypt_al.clicked.connect(self.decrypt_al_qui)
        self.Button_test_run.clicked.connect(self.decrypt_test_al_qui)
        self.Button_test_stop.clicked.connect(self.stop_tests)
        self.Button_load_test_params.clicked.connect(self.load_test_params)
        self.Button_view_test_res.clicked.connect(self.view_results)

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText("Произошла ошибка")
        msg.setInformativeText(message)
        msg.exec_()

    def show_message(self, message, title="Информация", icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def encrypt_qui(self):
        try:
            if self.lineEdit_bits.text() != "":
                bits = self.lineEdit_bits.text().strip()

                if bits != "" and all(char in "01 " for char in bits):
                    bits_clean = re.findall(r'[01]', bits)
                    bits_formatted = ' '.join(bits_clean)
                    if len(bits_clean) >= 4:
                        flag_ver_encrypt = "merkle" if self.comboBox_kod.currentText() == "Алгоритм Меркла-Хелмана" else ""

                        args = ["C:/Program Files/pypy/pypy3.exe", "Logic_pypy.py", "encrypt_qui", flag_ver_encrypt, bits_formatted]

                        result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
                        if result.returncode != 0:
                            raise RuntimeError(result.stderr.strip())

                        output = result.stdout.strip()
                        self.label_kod.setPlainText(output)
                    else:
                        self.show_error("Минимальное количество битов: 4")
                else:
                    self.show_error("Вписаны могут быть только цифры: 1 или 0. Использование других цифр или спец.знаков запрещено")
            else:
                self.show_error("Введите битовую последовательность перед кодированием")
        except Exception as e:
            self.show_error(str(e))

    def decrypt_qui(self):
        try:
            self.Button_dekod.setEnabled(False)
            if self.lineEdit_bits.text() != "":
                bits = self.lineEdit_bits.text().strip()
                if bits != "" and all(char in "01 " for char in bits):
                    bits_clean = re.findall(r'[01]', bits)
                    bits_formatted = ' '.join(bits_clean)
                    if len(bits_clean) >= 4:
                        if os.path.getsize("temp_data.json") != 0:
                            with open("temp_data.json", "r") as f:
                                data = json.load(f)
                            bit_input = data["bit_input"]
                            if bit_input == bits_formatted:
                                args = ["C:/Program Files/pypy/pypy3.exe", "Logic_pypy.py", "decrypt_qui"]
                                result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
                                if result.returncode != 0:
                                    raise RuntimeError(result.stderr.strip())
                                output = result.stdout.strip()
                                self.label_dekod.setPlainText(output)
                            else:
                                self.show_error("Сначала требуется выполнить кодирование последовательности")
                        else:
                            self.show_error("Сначала требуется выполнить кодирование последовательности")
                    else:
                        self.show_error("Минимальное количество битов: 4")
                else:
                    self.show_error("Вписаны могут быть только цифры: 1 или 0")
            else:
                self.show_error("Введите битовую последовательность перед решением задачи")
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.Button_dekod.setEnabled(True)

    def decrypt_al_qui(self):
        try:
            self.Button_decrypt_al.setEnabled(False)  # Блокируем кнопку
            if self.lineEdit_bits.text() != "":
                bits = self.lineEdit_bits.text().strip()
                if bits != "" and all(char in "01 " for char in bits):
                    bits_clean = re.findall(r'[01]', bits)
                    bits_formatted = ' '.join(bits_clean)
                    if len(bits_clean) >= 4:
                        if os.path.getsize("temp_data.json") != 0:
                            with open("temp_data.json", "r") as f:
                                data = json.load(f)
                            bit_input = data["bit_input"]
                            if bit_input == bits_formatted:
                                if self.check_numeric_fields():
                                    multi = "" if self.checkBox_multi.isChecked() else "s"
                                    if self.comboBox_dekod_al.currentText() == "Сброс с сохранением лучшей особи":
                                        flag_input = ""
                                    elif self.comboBox_dekod_al.currentText() == "Без эвристики":
                                        flag_input = "∞"
                                    else:
                                        flag_input = "S"
                                    funk_input = "" if self.comboBox_dekod_al_2.currentText() == "Одноточечный" else "S"
                                    gen_input = "" if self.comboBox_dekod_al_3.currentText() == "Классическая" else "S"

                                    args = [
                                        "C:/Program Files/pypy/pypy3.exe", "Logic_pypy.py", "decrypt_al_qui",
                                        flag_input, funk_input, gen_input,
                                        self.lineEdit_count_populations.text(),
                                        self.lineEdit_count_generat.text(),
                                        self.lineEdit_rate_mut.text(),
                                        self.lineEdit_rate_mut_evr.text(),
                                        self.lineEdit_evrist_n.text(),
                                        multi
                                    ]

                                    # Очистим поле перед запуском
                                    self.label_decrypt_al.clear()

                                    # Запускаем поток
                                    self.worker = PyPyWorker(args)
                                    self.worker.output_signal.connect(self.label_decrypt_al.appendPlainText)
                                    # Когда поток закончится — включим кнопку обратно
                                    self.worker.finished.connect(lambda: self.Button_decrypt_al.setEnabled(True))
                                    self.worker.start()
                            else:
                                self.show_error("Сначала требуется выполнить кодирование последовательности")
                                self.Button_decrypt_al.setEnabled(True)
                        else:
                            self.show_error("Сначала требуется выполнить кодирование последовательности")
                            self.Button_decrypt_al.setEnabled(True)
                    else:
                        self.show_error("Минимальное количество битов: 4")
                        self.Button_decrypt_al.setEnabled(True)
                else:
                    self.show_error("Вписаны могут быть только цифры: 1 или 0")
                    self.Button_decrypt_al.setEnabled(True)
            else:
                self.show_error("Введите битовую последовательность перед решением задачи")
                self.Button_decrypt_al.setEnabled(True)
        except Exception as e:
            self.show_error(str(e))
            self.Button_decrypt_al.setEnabled(True)

    def check_numeric_fields(self):
        try:
            values = [
                int(self.lineEdit_count_populations.text().strip()),
                int(self.lineEdit_count_generat.text().strip()),
                float(self.lineEdit_rate_mut.text().strip()),
                float(self.lineEdit_rate_mut_evr.text().strip()),
                int(self.lineEdit_evrist_n.text().strip())
            ]

            if int(self.lineEdit_count_populations.text().strip()) <= 3:
                self.show_error("Должно быть минимум 4 особи в поколении")
                self.Button_decrypt_al.setEnabled(True)
                return False

            if int(self.lineEdit_count_generat.text().strip()) <=0 or int(self.lineEdit_evrist_n.text().strip()) <=0:
                self.show_error("Начальные данные не могут быть отрицательными или равными 0")
                self.Button_decrypt_al.setEnabled(True)
                return False

            if int(self.lineEdit_count_generat.text().strip()) <= 3:
                self.show_error("Должно быть минимум 4 поколения")
                self.Button_decrypt_al.setEnabled(True)
                return False
            if int(self.lineEdit_evrist_n.text().strip()) <= 3:
                self.show_error("Минимальная точка эвристики - 4 поколения")
                self.Button_decrypt_al.setEnabled(True)
                return False

            # Проверка: вероятности от 0 до 1 включительно
            if not (0 <= values[2] <= 1):
                self.show_error("Вероятность мутаций (обычная) должна быть от 0 до 1.")
                self.Button_decrypt_al.setEnabled(True)
                return False

            if not (0 <= values[3] <= 1):
                self.show_error("Вероятность мутаций должна быть в диапозоне от 0 до 1.")
                self.Button_decrypt_al.setEnabled(True)
                return False

            return True
        except ValueError:
            self.show_error("Введите начальные данные в виде чисел (допускается дробное число с точкой для вероятностей мутаций).")
            self.Button_decrypt_al.setEnabled(True)
            return False

    def load_test_params(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self.centralwidget, "Выберите файл конфигурации", "", "JSON Files (*.json)"
            )
            if file_path:
                self.config_file_path = file_path  # сохраняем путь к файлу
                self.show_message("Конфигурация загружена.", title="Успех", icon=QMessageBox.Information)
        except Exception as e:
            self.show_error(f"Не удалось загрузить конфигурацию:\n{str(e)}")

    def check_numeric_fields_test(self):
        try:
            # Проверка числовых полей
            values = [
                int(self.lineEdit_count_populations_2.text().strip()),
                int(self.lineEdit_count_generat_2.text().strip()),
                int(self.lineEdit_count_test.text().strip()),
                int(self.lineEdit_len.text().strip()),
            ]

            if int(self.lineEdit_count_populations_2.text().strip()) <= 3:
                self.show_error("Должно быть минимум 4 особи в поколении")
                self.Button_test_run.setEnabled(True)
                return False

            if int(self.lineEdit_count_generat_2.text().strip()) <= 3:
                self.show_error("Минимальная размерность задачи - 4")
                self.Button_test_run.setEnabled(True)
                return False

            if int(self.lineEdit_count_generat_2.text().strip()) <= 3:
                self.show_error("Должно быть минимум 4 поколения")
                self.Button_test_run.setEnabled(True)
                return False

            if int(self.lineEdit_count_generat_2.text().strip()) <=0 or int(self.lineEdit_count_test.text().strip()) <=0:
                self.show_error("Начальные данные не могут быть отрицательными или равными 0")
                self.Button_test_run.setEnabled(True)
                return False

            if not self.config_file_path or not os.path.exists(self.config_file_path):
                self.show_error("Файл конфигурации не загружен.")
                self.Button_test_run.setEnabled(True)
                return False

            return True

        except ValueError:
            self.show_error("Введите начальные данные в виде целых чисел в разделе тестирования.")
            self.Button_test_run.setEnabled(True)
            return False

    def save_filename(self):
        try:
            if self.checkBox_save_test_res.isChecked():
                save_file = self.lineEdit_save_file.text().strip()
                if not save_file or re.search(r'[<>:"/\\|?*\s]', save_file):
                    return False
                else:
                    return save_file
            else:
                return ""

        except ValueError:
            self.show_error("Непредвиденная ошибка. Обратитесть к разработчику.")
            self.Button_test_run.setEnabled(True)
            return False

    def save_filename_true(self):
        try:
            if self.checkBox_save_test_res.isChecked():
                save_file = self.lineEdit_save_file.text().strip()
                if not save_file or re.search(r'[<>:"/\\|?*\s]', save_file):
                    raise ValueError("Неверное имя файла")
                else:
                    return True
            else:
                return True

        except ValueError:
            self.show_error("Неверное имя файла. Возможно вы ввели некорректные символы")
            self.Button_test_run.setEnabled(True)
            return False

    def decrypt_test_al_qui(self):
        try:
            if self.check_numeric_fields_test():
                if self.save_filename_true():
                    save_file = self.save_filename()
                    multi = "" if self.checkBox_multi_test.isChecked() else "s"

                    if self.comboBox_dekod_al_4.currentText() == "Сброс с сохранением лучшей особи":
                        flag_input = ""
                    elif self.comboBox_dekod_al_4.currentText() == "Без эвристики":
                        flag_input = "∞"
                    else:
                        flag_input = "S"
                    gen_input = "" if self.comboBox_dekod_al_5.currentText() == "Классическая" else "S"

                    args = [
                        "C:/Program Files/pypy/pypy3.exe", "Logic_pypy.py", "decrypt_test_al_qui",
                        flag_input, gen_input,
                        self.lineEdit_count_test.text(),
                        self.lineEdit_count_populations_2.text(),
                        self.lineEdit_count_generat_2.text(),
                        self.config_file_path,
                        save_file,
                        multi,
                        self.lineEdit_len.text(),
                    ]
                    # Очистим поле перед запуском
                    self.label_test.clear()
                    # Запускаем поток
                    self.worker = PyPyWorker(args)
                    self.worker.output_signal.connect(self.label_test.appendPlainText)
                    # Когда поток закончится — включим кнопку обратно
                    self.worker.finished.connect(lambda: self.Button_test_run.setEnabled(True))
                    self.worker.start()

        except Exception as e:
            self.show_error(str(e))
            self.Button_decrypt_al.setEnabled(True)

    def stop_tests(self):
        if hasattr(self, "worker") and self.worker.isRunning():
            self.worker.stop()

    def view_results(self):
        try:
            subprocess.run(
                ["C:/Users/Soundhugs/AppData/Local/Programs/Python/Python312/python.exe", "Tab_Gr_result.py"])
        except Exception as e:
            self.show_error(str(e))

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        # self.lineEdit_bits.setText("0011 0000 0101 0111 0011 0001 1101")
        self.lineEdit_bits.setText("0011 0000 0101 0111 0011 00")
        self.lineEdit_count_populations.setText("1700")
        self.lineEdit_count_populations_2.setText("1700")
        self.lineEdit_count_generat.setText("200000")
        self.lineEdit_count_generat_2.setText("200000")
        self.lineEdit_rate_mut.setText("1")
        self.lineEdit_rate_mut_evr.setText("0.5")
        self.lineEdit_evrist_n.setText("500")
        self.lineEdit_count_test.setText("1")
        self.lineEdit_len.setText("28")
        self.lineEdit_save_file.setText('28_бит_тестирование')
        Main.setWindowTitle(_translate("Main",
                                       "Hellman-GenAL: Программное средство для решения задачи о ранце модифицированной моделью Голдберга"))
        self.Button_dekod.setText(_translate("Main", "Решение задачи"))
        self.comboBox_kod.setItemText(0, _translate("Main", "Алгоритм Меркла-Хелмана"))
        self.comboBox_kod.setItemText(1, _translate("Main", "Модифицированный алгоритм Меркла-Хелмана"))
        self.lineEdit_bits.setPlaceholderText(_translate("Main", "Введите битовую последовательность. Минимум 4 бита."))
        self.lineEdit_save_file.setPlaceholderText(_translate("Main", "Введите название файла без формата"))
        self.label_name_1.setText(_translate("Main", "Создание условий задачи"))
        self.Button_kod.setText(_translate("Main", "Создание"))
        self.label_name_2.setText(
            _translate("Main", "Решение задачи с помощью модифицированной модели Голдберга"))
        self.checkBox_save_test_res.setText(_translate("Main", "Сохранять результаты в файл"))
        self.checkBox_multi.setText(_translate("Main", "Использовать распараллеливание"))
        self.checkBox_multi_test.setText(_translate("Main", "Использовать распараллеливание"))
        self.comboBox_dekod_al.setItemText(0, _translate("Main", "Сброс с сохранением лучшей особи"))
        self.comboBox_dekod_al.setItemText(1, _translate("Main", "Сброс без сохранения лучшей особи"))
        self.comboBox_dekod_al.setItemText(2, _translate("Main", "Без эвристики"))
        self.label_evrist.setText(_translate("Main", "Тип эвристики"))
        self.comboBox_dekod_al_2.setItemText(0, _translate("Main", "Одноточечный"))
        self.comboBox_dekod_al_2.setItemText(1, _translate("Main", "Двухточечный"))
        self.label_crossover.setText(_translate("Main", "Кроссовер"))
        self.label_populations.setText(_translate("Main", "Тип начальной популяции"))
        self.comboBox_dekod_al_3.setItemText(0, _translate("Main", "Классическая"))
        self.comboBox_dekod_al_3.setItemText(1, _translate("Main", "Прогрессивная"))
        self.label_count_populations.setText(_translate("Main", "Численность популяции:"))
        self.label_count_generat.setText(_translate("Main", "Число поколений:"))
        self.label_rate_mut.setText(_translate("Main", "Вероятность мутации:"))
        self.label_count_populations_2.setText(_translate("Main", "Вероятность мутации при эвристике:"))
        self.label_evrist_n.setText(_translate("Main", "Точка эвристики:"))
        self.Button_decrypt_al.setText(_translate("Main", "Решение задачи"))
        self.label_name_3.setText(_translate("Main", "Блок тестирования"))
        self.comboBox_dekod_al_4.setItemText(0, _translate("Main", "Сброс с сохранением лучшей особи"))
        self.comboBox_dekod_al_4.setItemText(1, _translate("Main", "Сброс без сохранения лучшей особи"))
        self.comboBox_dekod_al_4.setItemText(2, _translate("Main", "Без эвристики"))
        self.label_evrist_test.setText(_translate("Main", "Тип эвристики"))
        self.label_populations_2.setText(_translate("Main", "Тип начальной популяции"))
        self.comboBox_dekod_al_5.setItemText(0, _translate("Main", "Классическая"))
        self.comboBox_dekod_al_5.setItemText(1, _translate("Main", "Прогрессивная"))
        self.label_count_test.setText(_translate("Main", "Число тестирований:"))
        self.label_len.setText(_translate("Main", "Размерность задачи:"))
        self.Button_load_test_params.setText(_translate("Main", "Импорт конфига"))
        self.Button_test_run.setText(_translate("Main", "Запуск тестирования"))
        self.Button_test_stop.setText(_translate("Main", "Остановка"))
        self.Button_view_test_res.setText(_translate("Main", "Просмотр"))
        self.label_view_test_res.setText(_translate("Main", "Простотр результатов тестирования"))
        self.label_evrist_n_2.setText(_translate("Main", "Название файла:"))
        self.label_count_generat_2.setText(_translate("Main", "Число поколений:"))
        self.label_count_populations_3.setText(_translate("Main", "Численность популяции:"))

if __name__ == "__main__":
    import sys

    # with open("temp_data.json", "w") as f:
    #     pass
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QMainWindow()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.show()
    sys.exit(app.exec_())
