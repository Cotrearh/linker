# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/QT/select_link_dialog.ui'
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

class Ui_select_link_dialog(object):
    def setupUi(self, select_link_dialog):
        select_link_dialog.setObjectName(_fromUtf8("select_link_dialog"))
        select_link_dialog.resize(1200, 600)
        select_link_dialog.setMinimumSize(QtCore.QSize(1200, 600))
        self.verticalLayout = QtGui.QVBoxLayout(select_link_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(select_link_dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.filterEdit = QtGui.QLineEdit(select_link_dialog)
        self.filterEdit.setObjectName(_fromUtf8("filterEdit"))
        self.verticalLayout.addWidget(self.filterEdit)
        self.splitter = QtGui.QSplitter(select_link_dialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeWidget = QtGui.QTreeWidget(self.splitter)
        self.treeWidget.setMinimumSize(QtCore.QSize(300, 0))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.textEdit = QtGui.QTextEdit(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalWidget_2 = QtGui.QWidget(select_link_dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget_2.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_2.setSizePolicy(sizePolicy)
        self.horizontalWidget_2.setObjectName(_fromUtf8("horizontalWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cancelBtn = QtGui.QPushButton(self.horizontalWidget_2)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.horizontalLayout_2.addWidget(self.cancelBtn)
        self.AcceptBtn = QtGui.QPushButton(self.horizontalWidget_2)
        self.AcceptBtn.setObjectName(_fromUtf8("AcceptBtn"))
        self.horizontalLayout_2.addWidget(self.AcceptBtn)
        self.verticalLayout.addWidget(self.horizontalWidget_2)

        self.retranslateUi(select_link_dialog)
        QtCore.QMetaObject.connectSlotsByName(select_link_dialog)

    def retranslateUi(self, select_link_dialog):
        select_link_dialog.setWindowTitle(_translate("select_link_dialog", "Выбор ссылки", None))
        self.label.setText(_translate("select_link_dialog", "Выбор ссылки", None))
        self.filterEdit.setPlaceholderText(_translate("select_link_dialog", "Фильтр", None))
        self.treeWidget.headerItem().setText(0, _translate("select_link_dialog", "Термины", None))
        self.cancelBtn.setText(_translate("select_link_dialog", "Отмена", None))
        self.AcceptBtn.setText(_translate("select_link_dialog", "Принять", None))

