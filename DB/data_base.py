# -*- coding: utf-8 -*-

from PyQt4 import QtSql
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QSizePolicy

from config import Config


def get_local_connection():
    d = QtSql.QSqlDatabase.database('SQLiteConnection')
    if d.open():
        return d
    else:
        # диалог устранения ошибок
        return local_db_unreachable_alert()


def get_remote_connection():
    d = QtSql.QSqlDatabase.database('PGconnection')
    if d.open():
        return d
    else:
        # диалог устранения ошибок
        return remote_db_unreachable_alert()


def open_connection_to_remote():
    db = QtSql.QSqlDatabase.addDatabase('QPSQL', 'PGconnection')
    db.setHostName(Config.DB_HOST)
    db.setDatabaseName(Config.DB_NAME)
    db.setUserName(Config.DB_USER_NAME)
    db.setPort(Config.DB_PORT)
    db.setPassword(Config.DB_PASSWORD)
    if not db.open():
        print("Удаленная база данных не открылась!")
        print("-" + db.lastError().text() + "-")
        print(str(db.lastError().type()))
        return remote_db_unreachable_alert()
    else:
        # print("Удаленная база данных открылась!")
        if not db.driver().hasFeature(QtSql.QSqlDriver.Transactions):
            print('ТРАНЗАКЦИИ НЕ ДОСТУПНЫ!')
        return db


def open_connection_to_local():
    local_db = QtSql.QSqlDatabase.addDatabase('QSQLITE', 'SQLiteConnection')
    local_db.setDatabaseName(Config.LOCAL_DB_NAME)
    if not local_db.open():
        print("Локальная база данных не открылась!")
        print("-" + local_db.lastError().text() + "-")
        print(str(local_db.lastError().type()))
        return local_db_unreachable_alert()
    else:
        if not local_db.driver().hasFeature(QtSql.QSqlDriver.Transactions):
            print('ТРАНЗАКЦИИ НЕ ДОСТУПНЫ!')
        return local_db


def local_db_unreachable_alert():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Локальная БД не доступна. Проверьте правильность настроек базы данных и повторите попытку.'
                ' Либо нажмите "Отмена" и попробуйте подключиться позже.')
    msg.setWindowTitle('БД не отвечает')
    msg.setMaximumHeight(16000000)
    msg.setMaximumWidth(16000000)
    btnyes = msg.addButton("Повторить попытку", QMessageBox.YesRole)
    msg.addButton("Отмена", QMessageBox.NoRole)
    msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    msg.exec_()
    if msg.clickedButton() == btnyes:
        Config.load_settings()
        return open_connection_to_local()
    else:
        return None


def remote_db_unreachable_alert():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Удаленная БД не доступна. Проверьте правильность настроек базы данных и повторите попытку.'
                ' Либо нажмите "Отмена" и попробуйте подключиться позже.')
    msg.setWindowTitle('БД не отвечает')
    msg.setMaximumHeight(16000000)
    msg.setMaximumWidth(16000000)
    btnyes = msg.addButton("Повторить попытку", QMessageBox.YesRole)
    msg.addButton("Отмена", QMessageBox.NoRole)
    msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    msg.exec_()
    if msg.clickedButton() == btnyes:
        Config.load_settings()
        return open_connection_to_remote()
    else:
        return None
