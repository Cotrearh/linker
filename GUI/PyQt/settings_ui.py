# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/QT/settings.ui'
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

class Ui_settings(object):
    def setupUi(self, settings):
        settings.setObjectName(_fromUtf8("settings"))
        settings.resize(400, 300)
        self.verticalLayout_2 = QtGui.QVBoxLayout(settings)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(settings)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tabWidget = QtGui.QTabWidget(settings)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.nameEdit = QtGui.QLineEdit(self.tab)
        self.nameEdit.setInputMask(_fromUtf8(""))
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameEdit)
        self.hostEdit = QtGui.QLineEdit(self.tab)
        self.hostEdit.setInputMask(_fromUtf8(""))
        self.hostEdit.setObjectName(_fromUtf8("hostEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.hostEdit)
        self.portEdit = QtGui.QLineEdit(self.tab)
        self.portEdit.setObjectName(_fromUtf8("portEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.portEdit)
        self.userEdit = QtGui.QLineEdit(self.tab)
        self.userEdit.setObjectName(_fromUtf8("userEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.userEdit)
        self.passwordEdit = QtGui.QLineEdit(self.tab)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.passwordEdit)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancelBtn = QtGui.QPushButton(settings)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.saveBtn = QtGui.QPushButton(settings)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout.addWidget(self.saveBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(settings)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(settings)

    def retranslateUi(self, settings):
        settings.setWindowTitle(_translate("settings", "Настройки", None))
        self.label.setText(_translate("settings", "Настройки программы", None))
        self.label_2.setText(_translate("settings", "Имя БД", None))
        self.label_3.setText(_translate("settings", "Хост", None))
        self.label_4.setText(_translate("settings", "Порт", None))
        self.label_5.setText(_translate("settings", "Пользователь", None))
        self.label_6.setText(_translate("settings", "Пароль", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("settings", "Подключение к БД", None))
        self.cancelBtn.setText(_translate("settings", "Закрыть", None))
        self.saveBtn.setText(_translate("settings", "Сохранить", None))

