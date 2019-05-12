# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/QT/linkclickeddialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_linkClickedDialog(object):
    def setupUi(self, linkClickedDialog):
        linkClickedDialog.setObjectName(_fromUtf8("linkClickedDialog"))
        linkClickedDialog.resize(700, 400)
        linkClickedDialog.setMinimumSize(QtCore.QSize(700, 400))
        self.verticalLayout = QtGui.QVBoxLayout(linkClickedDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mainWordLabel = QtGui.QLabel(linkClickedDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainWordLabel.sizePolicy().hasHeightForWidth())
        self.mainWordLabel.setSizePolicy(sizePolicy)
        self.mainWordLabel.setText(_fromUtf8(""))
        self.mainWordLabel.setWordWrap(True)
        self.mainWordLabel.setObjectName(_fromUtf8("mainWordLabel"))
        self.verticalLayout.addWidget(self.mainWordLabel)
        self.definitionLabel = QtGui.QLabel(linkClickedDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.definitionLabel.sizePolicy().hasHeightForWidth())
        self.definitionLabel.setSizePolicy(sizePolicy)
        self.definitionLabel.setText(_fromUtf8(""))
        self.definitionLabel.setWordWrap(True)
        self.definitionLabel.setObjectName(_fromUtf8("definitionLabel"))
        self.verticalLayout.addWidget(self.definitionLabel)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalWidget = QtGui.QWidget(linkClickedDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget.sizePolicy().hasHeightForWidth())
        self.horizontalWidget.setSizePolicy(sizePolicy)
        self.horizontalWidget.setObjectName(_fromUtf8("horizontalWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancelBtn = QtGui.QPushButton(self.horizontalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelBtn.sizePolicy().hasHeightForWidth())
        self.cancelBtn.setSizePolicy(sizePolicy)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.deleteBtn = QtGui.QPushButton(self.horizontalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteBtn.sizePolicy().hasHeightForWidth())
        self.deleteBtn.setSizePolicy(sizePolicy)
        self.deleteBtn.setObjectName(_fromUtf8("deleteBtn"))
        self.horizontalLayout.addWidget(self.deleteBtn)
        self.editBtn = QtGui.QPushButton(self.horizontalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editBtn.sizePolicy().hasHeightForWidth())
        self.editBtn.setSizePolicy(sizePolicy)
        self.editBtn.setObjectName(_fromUtf8("editBtn"))
        self.horizontalLayout.addWidget(self.editBtn)
        self.acceptBtn = QtGui.QPushButton(self.horizontalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptBtn.sizePolicy().hasHeightForWidth())
        self.acceptBtn.setSizePolicy(sizePolicy)
        self.acceptBtn.setObjectName(_fromUtf8("acceptBtn"))
        self.horizontalLayout.addWidget(self.acceptBtn)
        self.verticalLayout.addWidget(self.horizontalWidget)

        self.retranslateUi(linkClickedDialog)
        QtCore.QMetaObject.connectSlotsByName(linkClickedDialog)

    def retranslateUi(self, linkClickedDialog):
        linkClickedDialog.setWindowTitle(_translate("linkClickedDialog", "Работа со ссылкой", None))
        self.cancelBtn.setText(_translate("linkClickedDialog", "Отмена", None))
        self.deleteBtn.setText(_translate("linkClickedDialog", "Удалить", None))
        self.editBtn.setText(_translate("linkClickedDialog", "Редактировать", None))
        self.acceptBtn.setText(_translate("linkClickedDialog", "Принять", None))

