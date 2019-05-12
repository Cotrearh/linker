from PyQt4 import QtSql
from PyQt4.QtCore import QThread
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QProgressDialog
from PyQt4.QtSql import QSqlQuery

from DB.data_base import get_local_connection, get_remote_connection
from DB.queries import replace_uuid_in_links_query, full_delete_local_termin_by_uuid, select_all_broken_query, \
    find_all_termins_contains_link_to_uuid, update_definition_query, update_definition_query_OC, \
    find_all_termins_contains_link_to_uuid_OC, replace_uuid_in_links_query_OC
from utils.StringUtils import delete_uuid_from_definition


class BrokenLinksDeleter(QThread):
    finishTrigger = pyqtSignal(bool)
    count_trigger = pyqtSignal(int)
    error_trigger = pyqtSignal(str)

    # mode: 0 - delete all to this, 1 - replace, 2 - delete all to all
    def __init__(self, mode, uuid=None, new_uuid=None, onlyClassified=False):
        super().__init__()
        self.mode = mode
        self.local_cn = get_local_connection()
        self.remote_cn = get_remote_connection()
        self.new_uuid = new_uuid
        self.uuid = uuid
        self.d = self.draw_progress_dialog()
        self.onlyClassified = onlyClassified

    def run(self):
        if self.mode == 0:
            self.delete_all_links_to_this_word(self.uuid)
        elif self.mode == 1:
            self.replace_all_links_to_this_word()
        elif self.mode == 2:
            self.delete_all_links_to_all_words()

    def draw_progress_dialog(self):
        d = QProgressDialog('Обработка битых ссылок', 'Отмена', 0, 0)
        d.setWindowModality(Qt.WindowModal)
        d.setCancelButton(None)
        d.setWindowTitle('Обработка битых ссылок')
        d.setMaximumWidth(500)
        return d

    def delete_all_links_to_this_word(self, uuid):
        remote_query = QSqlQuery(self.remote_cn)
        remote_query2 = QSqlQuery(self.remote_cn)
        local_query = QSqlQuery(self.local_cn)
        if self.onlyClassified:
            remote_query.prepare(find_all_termins_contains_link_to_uuid_OC(uuid))
        else:
            remote_query.prepare(find_all_termins_contains_link_to_uuid(uuid))
        local_query.prepare(full_delete_local_termin_by_uuid)
        local_query.bindValue(":uuid", uuid)
        s1, s2 = False, False
        QtSql.QSqlDatabase.database('SQLiteConnection').transaction()
        QtSql.QSqlDatabase.database('PGconnection').transaction()
        if remote_query.exec_():
            s1 = True
            while remote_query.next():
                # update definition
                new_definition = delete_uuid_from_definition(uuid, remote_query.value(1))
                if self.onlyClassified:
                    remote_query2.prepare(update_definition_query_OC)
                else:
                    remote_query2.prepare(update_definition_query)
                remote_query2.bindValue(":uuid", remote_query.value(0))
                remote_query2.bindValue(":definition", new_definition)
        else:
            print(remote_query.lastError().text())
            print(remote_query.lastQuery())
        if local_query.exec_():
            s2 = True
        else:
            print(local_query.lastError().text())
            print(local_query.lastQuery())
        if s1 and s2:
            QtSql.QSqlDatabase.database('SQLiteConnection').commit()
            QtSql.QSqlDatabase.database('PGconnection').commit()
        else:
            QtSql.QSqlDatabase.database('SQLiteConnection').rollback()
            QtSql.QSqlDatabase.database('PGconnection').rollback()
        self.finishTrigger.emit(True)

    def replace_all_links_to_this_word(self):
        remote_query = QSqlQuery(self.remote_cn)
        local_query = QSqlQuery(self.local_cn)
        if self.onlyClassified:
            remote_query.prepare(replace_uuid_in_links_query_OC(self.uuid, self.new_uuid))
        else:
            remote_query.prepare(replace_uuid_in_links_query(self.uuid, self.new_uuid))
        local_query.prepare(full_delete_local_termin_by_uuid)
        local_query.bindValue(":uuid", self.uuid)
        s1, s2 = False, False
        QtSql.QSqlDatabase.database('SQLiteConnection').transaction()
        QtSql.QSqlDatabase.database('PGconnection').transaction()
        if remote_query.exec_():
            s1 = True
        else:
            print(remote_query.lastError().text())
            print(remote_query.lastQuery())
        if local_query.exec_():
            s2 = True
        else:
            print(local_query.lastError().text())
            print(local_query.lastQuery())
        if s1 and s2:
            QtSql.QSqlDatabase.database('SQLiteConnection').commit()
            QtSql.QSqlDatabase.database('PGconnection').commit()
        else:
            QtSql.QSqlDatabase.database('SQLiteConnection').rollback()
            QtSql.QSqlDatabase.database('PGconnection').rollback()
        self.finishTrigger.emit(True)

    def delete_all_links_to_all_words(self):
        local_query = QSqlQuery(self.local_cn)
        local_query.prepare(select_all_broken_query)
        while local_query.next():
            self.delete_all_links_to_this_word(local_query.value(0))
        self.finishTrigger.emit(True)
