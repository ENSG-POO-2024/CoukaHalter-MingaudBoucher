import sys
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QTextEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from game_window import MainWindow


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(501, 390)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("../assets/pokeball.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        Dialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 270, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Yes
        )
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-20, -20, 571, 411))
        self.label.setMidLineWidth(-2)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../assets/launch.png"))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(150, 80, 201, 41))
        self.textEdit.setObjectName("textEdit")
        self.label.raise_()
        self.buttonBox.raise_()
        self.textEdit.raise_()

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            self.openGameWindow
        )

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pokemon Python Launcher"))
        self.textEdit.setHtml(
            _translate(
                "Dialog",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:16pt; font-weight:600; color:#26a269;">Pokemon Python </span></p></body></html>',
            )
        )

    def openGameWindow(self):
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        window = MainWindow()
        window.show()


class MainLauncherWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainLauncherWindow()
    window.show()
    sys.exit(app.exec_())
