# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/QT/mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1029, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.linkerTab = QtGui.QWidget()
        self.linkerTab.setObjectName(_fromUtf8("linkerTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.linkerTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter = QtGui.QSplitter(self.linkerTab)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.verticalWidget = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalWidget.setObjectName(_fromUtf8("verticalWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.onlyClassifiedCheck = QtGui.QCheckBox(self.verticalWidget)
        self.onlyClassifiedCheck.setVisible(False)
        # self.onlyClassifiedCheck.setChecked(True)
        # self.onlyClassifiedCheck.setObjectName(_fromUtf8("onlyClassifiedCheck"))
        # self.verticalLayout_3.addWidget(self.onlyClassifiedCheck)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.refreshTerminsListBtn = QtGui.QPushButton(self.verticalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshTerminsListBtn.sizePolicy().hasHeightForWidth())
        self.refreshTerminsListBtn.setSizePolicy(sizePolicy)
        self.refreshTerminsListBtn.setObjectName(_fromUtf8("refreshTerminsListBtn"))
        self.horizontalLayout_4.addWidget(self.refreshTerminsListBtn)
        self.showLinkedCheck = QtGui.QCheckBox(self.verticalWidget)
        self.showLinkedCheck.setVisible(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showLinkedCheck.sizePolicy().hasHeightForWidth())
        self.showLinkedCheck.setSizePolicy(sizePolicy)
        self.showLinkedCheck.setObjectName(_fromUtf8("showLinkedCheck"))
        self.horizontalLayout_4.addWidget(self.showLinkedCheck)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.searchLineEdit = QtGui.QLineEdit(self.verticalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchLineEdit.sizePolicy().hasHeightForWidth())
        self.searchLineEdit.setSizePolicy(sizePolicy)
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.horizontalLayout_5.addWidget(self.searchLineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.terminsTreeWidget = QtGui.QTreeWidget(self.verticalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.terminsTreeWidget.sizePolicy().hasHeightForWidth())
        self.terminsTreeWidget.setSizePolicy(sizePolicy)
        self.terminsTreeWidget.setObjectName(_fromUtf8("terminsTreeWidget"))
        self.verticalLayout_3.addWidget(self.terminsTreeWidget)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label = QtGui.QLabel(self.verticalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_6.addWidget(self.label)
        self.terminsPerPageComboBos = QtGui.QComboBox(self.verticalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.terminsPerPageComboBos.sizePolicy().hasHeightForWidth())
        self.terminsPerPageComboBos.setSizePolicy(sizePolicy)
        self.terminsPerPageComboBos.setObjectName(_fromUtf8("terminsPerPageComboBos"))
        self.terminsPerPageComboBos.addItem(_fromUtf8(""))
        self.terminsPerPageComboBos.addItem(_fromUtf8(""))
        self.terminsPerPageComboBos.addItem(_fromUtf8(""))
        self.horizontalLayout_6.addWidget(self.terminsPerPageComboBos)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.widget = QtGui.QWidget(self.verticalWidget)
        self.widget.setMaximumSize(QtCore.QSize(500, 16777215))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.terminListPaginatorLayout = QtGui.QHBoxLayout()
        self.terminListPaginatorLayout.setObjectName(_fromUtf8("terminListPaginatorLayout"))
        self.horizontalLayout_3.addLayout(self.terminListPaginatorLayout)
        self.verticalLayout_3.addWidget(self.widget)
        self.verticalWidget_2 = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget_2.sizePolicy().hasHeightForWidth())
        self.verticalWidget_2.setSizePolicy(sizePolicy)
        self.verticalWidget_2.setObjectName(_fromUtf8("verticalWidget_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.insertLinkBtn = QtGui.QPushButton(self.verticalWidget_2)
        self.insertLinkBtn.setObjectName(_fromUtf8("insertLinkBtn"))
        self.horizontalLayout_2.addWidget(self.insertLinkBtn)
        self.decomposeLinksCheck = QtGui.QCheckBox(self.verticalWidget_2)
        self.decomposeLinksCheck.setChecked(True)
        self.decomposeLinksCheck.setObjectName(_fromUtf8("decomposeLinksCheck"))
        self.horizontalLayout_2.addWidget(self.decomposeLinksCheck)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.terminNameLabel = QtGui.QLabel(self.verticalWidget_2)
        self.terminNameLabel.setObjectName(_fromUtf8("terminNameLabel"))
        self.verticalLayout_4.addWidget(self.terminNameLabel)
        self.textEdit = ExtendedTextEdit(self.verticalWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(500, 0))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout_4.addWidget(self.textEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.passBtn = QtGui.QPushButton(self.verticalWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passBtn.sizePolicy().hasHeightForWidth())
        self.passBtn.setSizePolicy(sizePolicy)
        self.passBtn.setObjectName(_fromUtf8("passBtn"))
        self.horizontalLayout.addWidget(self.passBtn)
        self.saveBtn = QtGui.QPushButton(self.verticalWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveBtn.sizePolicy().hasHeightForWidth())
        self.saveBtn.setSizePolicy(sizePolicy)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout.addWidget(self.saveBtn)
        self.continueBtn = QtGui.QPushButton(self.verticalWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.continueBtn.sizePolicy().hasHeightForWidth())
        self.continueBtn.setSizePolicy(sizePolicy)
        self.continueBtn.setObjectName(_fromUtf8("continueBtn"))
        self.horizontalLayout.addWidget(self.continueBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.splitter)
        self.tabWidget.addTab(self.linkerTab, _fromUtf8(""))
        self.brokenLinksTab = QtGui.QWidget()
        self.brokenLinksTab.setObjectName(_fromUtf8("brokenLinksTab"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.brokenLinksTab)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.splitter_2 = QtGui.QSplitter(self.brokenLinksTab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.verticalWidget1 = QtGui.QWidget(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget1.sizePolicy().hasHeightForWidth())
        self.verticalWidget1.setSizePolicy(sizePolicy)
        self.verticalWidget1.setObjectName(_fromUtf8("verticalWidget1"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.verticalWidget1)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.brokenlinksSearhLine = QtGui.QLineEdit(self.verticalWidget1)
        self.brokenlinksSearhLine.setObjectName(_fromUtf8("brokenlinksSearhLine"))
        self.verticalLayout_5.addWidget(self.brokenlinksSearhLine)
        self.brokenLinksTree = QtGui.QTreeWidget(self.verticalWidget1)
        self.brokenLinksTree.setObjectName(_fromUtf8("brokenLinksTree"))
        self.verticalLayout_5.addWidget(self.brokenLinksTree)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_3 = QtGui.QLabel(self.verticalWidget1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_11.addWidget(self.label_3)
        self.brokenlinksComboBox = QtGui.QComboBox(self.verticalWidget1)
        self.brokenlinksComboBox.setObjectName(_fromUtf8("brokenlinksComboBox"))
        self.brokenlinksComboBox.addItem(_fromUtf8(""))
        self.brokenlinksComboBox.addItem(_fromUtf8(""))
        self.brokenlinksComboBox.addItem(_fromUtf8(""))
        self.brokenlinksComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_11.addWidget(self.brokenlinksComboBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem2)
        self.deleteAllBrokenBtn = QtGui.QPushButton(self.verticalWidget1)
        self.deleteAllBrokenBtn.setObjectName(_fromUtf8("deleteAllBrokenBtn"))
        self.horizontalLayout_11.addWidget(self.deleteAllBrokenBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.widget_2 = QtGui.QWidget(self.verticalWidget1)
        self.widget_2.setMinimumSize(QtCore.QSize(500, 0))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.brokenLinksPaginatorLayout = QtGui.QHBoxLayout()
        self.brokenLinksPaginatorLayout.setObjectName(_fromUtf8("brokenLinksPaginatorLayout"))
        self.horizontalLayout_9.addLayout(self.brokenLinksPaginatorLayout)
        self.verticalLayout_5.addWidget(self.widget_2)
        self.brokenLinksActionsWidget = QtGui.QWidget(self.splitter_2)
        self.brokenLinksActionsWidget.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.brokenLinksActionsWidget.sizePolicy().hasHeightForWidth())
        self.brokenLinksActionsWidget.setSizePolicy(sizePolicy)
        self.brokenLinksActionsWidget.setObjectName(_fromUtf8("brokenLinksActionsWidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.brokenLinksActionsWidget)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_2 = QtGui.QLabel(self.brokenLinksActionsWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_6.addWidget(self.label_2)
        self.brokenLinkMainWordLabel = QtGui.QLabel(self.brokenLinksActionsWidget)
        self.brokenLinkMainWordLabel.setText(_fromUtf8(""))
        self.brokenLinkMainWordLabel.setObjectName(_fromUtf8("brokenLinkMainWordLabel"))
        self.verticalLayout_6.addWidget(self.brokenLinkMainWordLabel)
        self.groupBox = QtGui.QGroupBox(self.brokenLinksActionsWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.deleteAllToThisBtn = QtGui.QRadioButton(self.groupBox)
        self.deleteAllToThisBtn.setChecked(True)
        self.deleteAllToThisBtn.setObjectName(_fromUtf8("deleteAllToThisBtn"))
        self.verticalLayout_7.addWidget(self.deleteAllToThisBtn)
        self.replaceAllToThisBtn = QtGui.QRadioButton(self.groupBox)
        self.replaceAllToThisBtn.setObjectName(_fromUtf8("replaceAllToThisBtn"))
        self.verticalLayout_7.addWidget(self.replaceAllToThisBtn)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.seectReplacementBrokenLinkBtn = QtGui.QPushButton(self.groupBox)
        self.seectReplacementBrokenLinkBtn.setObjectName(_fromUtf8("seectReplacementBrokenLinkBtn"))
        self.horizontalLayout_8.addWidget(self.seectReplacementBrokenLinkBtn)
        self.brokenRepalcementText = QtGui.QLineEdit(self.groupBox)
        self.brokenRepalcementText.setReadOnly(True)
        self.brokenRepalcementText.setObjectName(_fromUtf8("brokenRepalcementText"))
        self.horizontalLayout_8.addWidget(self.brokenRepalcementText)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem3)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.brokenLinkOkBtn = QtGui.QPushButton(self.groupBox)
        self.brokenLinkOkBtn.setObjectName(_fromUtf8("brokenLinkOkBtn"))
        self.horizontalLayout_10.addWidget(self.brokenLinkOkBtn)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.horizontalLayout_7.addWidget(self.splitter_2)
        self.tabWidget.addTab(self.brokenLinksTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1029, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.settingsAction = QtGui.QAction(MainWindow)
        self.settingsAction.setObjectName(_fromUtf8("settingsAction"))
        self.refreshTerminListAction = QtGui.QAction(MainWindow)
        self.refreshTerminListAction.setObjectName(_fromUtf8("refreshTerminListAction"))
        self.clearTerminsListAction = QtGui.QAction(MainWindow)
        self.clearTerminsListAction.setObjectName(_fromUtf8("clearTerminsListAction"))
        self.menu.addAction(self.settingsAction)
        self.menu_2.addAction(self.refreshTerminListAction)
        self.menu_2.addAction(self.clearTerminsListAction)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Средство расстановки ссылок", None))
        # self.onlyClassifiedCheck.setToolTip(_translate("MainWindow", "Режим работы только с классифицированными терминами", None))
        # self.onlyClassifiedCheck.setText(_translate("MainWindow", "Только классифицированные", None))
        self.refreshTerminsListBtn.setText(_translate("MainWindow", "Обновить список", None))
        self.showLinkedCheck.setText(_translate("MainWindow", "Показать обработанные", None))
        self.searchLineEdit.setPlaceholderText(_translate("MainWindow", "Фильтр", None))
        self.terminsTreeWidget.headerItem().setText(0, _translate("MainWindow", "Список заглавных слов", None))
        self.label.setText(_translate("MainWindow", "Выводить по", None))
        self.terminsPerPageComboBos.setItemText(0, _translate("MainWindow", "50", None))
        self.terminsPerPageComboBos.setItemText(1, _translate("MainWindow", "100", None))
        self.terminsPerPageComboBos.setItemText(2, _translate("MainWindow", "200", None))
        self.insertLinkBtn.setText(_translate("MainWindow", "Вставить ссылку", None))
        self.decomposeLinksCheck.setToolTip(_translate("MainWindow", "Удаляемая ссылка по возможности будет разделяться на более малеькие, входящие в её состав", None))
        self.decomposeLinksCheck.setText(_translate("MainWindow", "Декомпозировать удаляемые ссылки", None))
        self.terminNameLabel.setText(_translate("MainWindow", "Термин:", None))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.passBtn.setText(_translate("MainWindow", "Пропустить", None))
        self.saveBtn.setText(_translate("MainWindow", "Сохранить", None))
        self.continueBtn.setText(_translate("MainWindow", "Продолжить", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.linkerTab), _translate("MainWindow", "Расстановка ссылок", None))
        self.brokenlinksSearhLine.setPlaceholderText(_translate("MainWindow", "Фильтр", None))
        self.brokenLinksTree.headerItem().setText(0, _translate("MainWindow", "Список заглавных слов", None))
        self.label_3.setText(_translate("MainWindow", "Выводить по", None))
        self.brokenlinksComboBox.setItemText(0, _translate("MainWindow", "20", None))
        self.brokenlinksComboBox.setItemText(1, _translate("MainWindow", "50", None))
        self.brokenlinksComboBox.setItemText(2, _translate("MainWindow", "100", None))
        self.brokenlinksComboBox.setItemText(3, _translate("MainWindow", "200", None))
        self.deleteAllBrokenBtn.setToolTip(_translate("MainWindow", "Удалить все битые ссылки, ведущие на несуществующие термины", None))
        self.deleteAllBrokenBtn.setText(_translate("MainWindow", "Удалить все", None))
        self.label_2.setText(_translate("MainWindow", "Заглавное слово:", None))
        self.groupBox.setTitle(_translate("MainWindow", "Действия:", None))
        self.deleteAllToThisBtn.setText(_translate("MainWindow", "Удалить все ссылки на это заглавное слово", None))
        self.replaceAllToThisBtn.setText(_translate("MainWindow", "Заменить все ссылки ссылками на:", None))
        self.seectReplacementBrokenLinkBtn.setText(_translate("MainWindow", "Выбрать", None))
        self.brokenLinkOkBtn.setText(_translate("MainWindow", "Применить", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.brokenLinksTab), _translate("MainWindow", "Актуализация ссылок", None))
        self.menu.setTitle(_translate("MainWindow", "Меню", None))
        self.menu_2.setTitle(_translate("MainWindow", "Расстановка ссылок", None))
        self.settingsAction.setText(_translate("MainWindow", "Настройки", None))
        self.refreshTerminListAction.setText(_translate("MainWindow", "Обновить список терминов", None))
        self.clearTerminsListAction.setText(_translate("MainWindow", "Очистить список терминов", None))

from widgets.LinkerTextEditor.ExtendedTextEditor import ExtendedTextEdit
