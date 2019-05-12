# Класс синхронизации данных с удалённой БД.
import time

from PyQt4 import QtSql
from PyQt4.QtCore import QThread, pyqtSignal, Qt, QCoreApplication, QEventLoop
from PyQt4.QtGui import QProgressDialog
from PyQt4.QtSql import QSqlQuery

from DB.data_base import get_remote_connection, get_local_connection
from DB.queries import count_termins_on_server_query, select_termins_from_server_query, select_termin_by_uuid_query, \
    update_termin_from_server_query, add_termins_from_server_query, select_all_local_termins_query, \
    check_uuid_on_server_query, count_termins_local_query, delete_local_termins_by_uuid_list, \
    check_link_exist_by_uuid_query, \
    final_delete_local_termins_by_uuid_list, clear_all_termins_query, count_termins_on_server_query_OC, \
    select_termins_from_server_query_OC, check_uuid_on_server_query_OC, check_link_exist_by_uuid_query_OC
from utils.StringUtils import stem_str


class TerminsRefresher(QThread):
    finishTrigger = pyqtSignal()
    count_trigger = pyqtSignal(int)
    error_trigger = pyqtSignal(str)
    msg_trigger = pyqtSignal(str)

    def __init__(self, onlyClassified):
        super().__init__()
        self.onlyClassified = onlyClassified
        self.remote_cn = get_remote_connection()
        self.local_cn = get_local_connection()
        self.count = 0
        self.progress = self.draw_progress_dialog()

    def run(self):
        QtSql.QSqlDatabase.database('SQLiteConnection').transaction()
        if self.refresh():
            QtSql.QSqlDatabase.database('SQLiteConnection').commit()
            self.finishTrigger.emit()
        else:
            QtSql.QSqlDatabase.database('SQLiteConnection').rollback()
            self.finishTrigger.emit()

    def draw_progress_dialog(self):
        d = QProgressDialog('Обновление списка терминов', 'Отмена', 0, 10)
        d.setWindowModality(Qt.WindowModal)
        d.setCancelButton(None)
        # l = QLabel()
        # l.setWordWrap(True)
        # d.setLabel(l)
        d.setWindowTitle('Обновление списка терминов')
        d.setMaximumWidth(500)
        return d

    def refresh(self):
        start = time.time()
        print('Refreshing list')
        query = QSqlQuery(self.remote_cn)
        local_query = QSqlQuery(self.local_cn)
        local_delete_query = QSqlQuery(self.local_cn)
        finallocal_delete_query = QSqlQuery(self.local_cn)

        if self.onlyClassified:
            query.prepare(count_termins_on_server_query_OC)
        else:
            query.prepare(count_termins_on_server_query)
        local_query.prepare(count_termins_local_query)
        self.msg_trigger.emit('Подсчёт кол-ва терминов')
        if local_query.exec_() and local_query.next():
            print("LOCAL - " + local_query.value(0).__str__())
            self.count += local_query.value(0)
        else:
            return False
        if query.exec_() and query.next():
            print("REMOTE - " + query.value(0).__str__())
            self.count += query.value(0)
            cc = query.value(0)
            # self.count *= 2
        else:
            return False
        self.count += 1
        self.progress.setMaximum(self.count)

        cnt = 0
        # Удаление терминов, отсутствующих на сервере, из локальной БД
        uuid_list = []
        remove_uuid_list = []
        local_query.prepare(select_all_local_termins_query)
        if local_query.exec_():  # проходим по всем локальным терминам
            while local_query.next():
                QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
                if self.onlyClassified:
                    query.prepare(check_uuid_on_server_query_OC)
                else:
                    query.prepare(check_uuid_on_server_query)
                query.bindValue(':uuid', local_query.value(0))
                current_uuid = local_query.value(0).__str__()
                self.msg_trigger.emit('Проверка локальных терминов:\n' + local_query.value(1))
                if query.exec_():  # есть ли на сервере термин с таким УИДом?
                    QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
                    if not query.next():  # если нет
                        local_check_query = QSqlQuery(self.remote_cn)
                        if self.onlyClassified:
                            local_check_query.prepare(check_link_exist_by_uuid_query_OC(current_uuid))
                        else:
                            local_check_query.prepare(check_link_exist_by_uuid_query(current_uuid))
                        # проверяем, етсь ли термины, в которых есть ссылки на этот термин
                        if local_check_query.exec_():
                            if local_check_query.next():  # если есть
                                uuid_list.append("'" + current_uuid + "'")  # добавляем в список на пометку про удаление
                            else:  # если нет
                                # добавляем в список на окончательное удаление
                                remove_uuid_list.append("'" + current_uuid + "'")
                        else:
                            print(local_check_query.lastQuery())
                            print(local_check_query.lastError().text())
                            return False
                else:
                    print(query.lastQuery())
                    print(query.lastError().text())  # не получилось удалить - сообщи об ошибке
                    return False
                cnt += 1
                self.count_trigger.emit(cnt)
                if len(uuid_list) == 1000:
                    lst = ','.join(uuid_list)
                    local_delete_query.prepare(delete_local_termins_by_uuid_list(lst))
                    if not local_delete_query.exec_():  # пробуем удалить
                        print(local_delete_query.lastQuery())
                        print(local_delete_query.lastError().text())  # не получилось удалить - сообщи об ошибке
                        return False
                    uuid_list = []
                if len(remove_uuid_list) == 1000:
                    lst2 = ','.join(remove_uuid_list)
                    finallocal_delete_query.prepare(final_delete_local_termins_by_uuid_list(lst2))
                    if not finallocal_delete_query.exec_():  # пробуем удалить
                        print(finallocal_delete_query.lastQuery())
                        print(finallocal_delete_query.lastError().text())  # не получилось удалить - сообщи об ошибке
                        return False
                    remove_uuid_list = []
            if len(uuid_list) > 0:
                lst = ','.join(uuid_list)
                local_delete_query.prepare(delete_local_termins_by_uuid_list(lst))
                if not local_delete_query.exec_():  # пробуем удалить
                    print(local_delete_query.lastQuery())
                    print(local_delete_query.lastError().text())  # не получилось удалить - сообщи об ошибке
                    return False
            if len(remove_uuid_list) > 0:
                lst2 = ','.join(remove_uuid_list)
                finallocal_delete_query.prepare(final_delete_local_termins_by_uuid_list(lst2))
                if not finallocal_delete_query.exec_():  # пробуем удалить
                    print(finallocal_delete_query.lastQuery())
                    print(finallocal_delete_query.lastError().text())  # не получилось удалить - сообщи об ошибке
                    return False
        else:
            print(local_query.lastQuery())
            print(local_query.lastError().text())  # не получилось удалить - сообщи об ошибке
            return False

        # Добавление новых терминов с сервера
        portion = 0
        query_parts = []
        q = 1000
        i = int((cc) / q + 1)
        a = i
        print(i)
        while i > 0:
            count = 0
            inserted = 0
            if self.onlyClassified:
                query.prepare(select_termins_from_server_query_OC)
            else:
                query.prepare(select_termins_from_server_query)
            query.bindValue(':limit', q.__str__())
            query.bindValue(':offset', ((a - i) * q).__str__())
            if query.exec_():  # выбираем данные с сервера
                # print(query.lastQuery())
                while query.next():  # итерируемся по терминам
                    count += 1
                    local_query.prepare(select_termin_by_uuid_query)
                    local_query.bindValue(':uuid', query.value(0).__str__())
                    self.msg_trigger.emit('Получение терминов с сервера:\n' + query.value(1))
                    if local_query.exec_():
                        if local_query.next():  # если есть термин с таким УИДОМ
                            # print('3')
                            QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
                            # если заглавное слово(и другие атрибуты) изменилось
                            if (query.value(1).__str__().strip() != local_query.value(
                                    0).__str__().strip()) or local_query.value(1) == 1:
                                local_query.prepare(update_termin_from_server_query)
                                local_query.bindValue(':name', query.value(1).__str__().strip())
                                local_query.bindValue(':uuid', query.value(0).__str__().strip())
                                local_query.bindValue(':name_stemmed', stem_str(query.value(0).__str__().strip()))
                                if not local_query.exec_():  # попробовать обновить
                                    print("Ошибка при обновлении термина:" + local_query.value(0).__str__().strip() +
                                          " -> " + query.value(1).__str__().strip())
                                    print(local_query.lastQuery())
                                    print(local_query.lastError().text())  # не получилось обновить - сообщи об ошибке
                                    return False
                                # else:
                                #     print('UPDATED TERMIN - ' + query.value(1).__str__().strip())
                        else:  # если нет термина с таким УИДом, значит он новый и его надо добавить
                            QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
                            if portion < 100:
                                query_parts.append('(\'' + query.value(0).__str__().replace("'", "''")
                                                   + '\', \'' + query.value(1).__str__().replace("'", "''") +
                                                   '\', 0, 0, \'' + stem_str(
                                    query.value(1).__str__().replace("'", "''")) + '\')')
                                portion += 1
                                inserted += 1
                            else:
                                query_parts.append('(\'' + query.value(0).__str__().replace("'", "''")
                                                   + '\', \'' + query.value(1).__str__().replace("'", "''") +
                                                   '\', 0, 0, \'' + stem_str(
                                    query.value(1).__str__().replace("'", "''")) + '\')')
                                inserted += 1
                                portion = 0
                                q_s = ', '.join(query_parts)
                                local_query.prepare(add_termins_from_server_query(q_s))
                                if not local_query.exec_():  # пробовать добавить
                                    print("Ошибка при добавлении новых терминов: " + q_s)
                                    print(local_query.lastQuery())
                                    print(local_query.lastError().text())  # не получилось добавить - сообщи об ошибке
                                    return False
                                query_parts = []
                    else:
                        print("Обшибка обращения к БД.")
                        print(local_query.lastQuery())
                        print(local_query.lastError().text())  # не получилось - сообщи об ошибке
                        return False
                    cnt += 1
                    self.count_trigger.emit(cnt)
                    QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
                if len(query_parts) > 0:
                    q_s = ', '.join(query_parts)
                    local_query.prepare(add_termins_from_server_query(q_s))
                    if not local_query.exec_():  # пробовать добавить
                        print("Ошибка при добавлении новых терминов2: " + q_s)
                        print(local_query.lastQuery())
                        print(local_query.lastError().text())  # не получилось добавить - сообщи об ошибке
                        return False
                    # else:
                    #     print('INSERTED ' + len(query_parts).__str__() + ' TERMINS')
                    query_parts = []
            else:
                print(query.lastQuery())
                print(query.lastError().text())  # не получилось - сообщи об ошибке
                return False
            i -= 1
            # print("TOTAL - " + count.__str__())
            # print("INSERTED - " + inserted.__str__())
        # local_query.prepare(check_deleted_restored_query)
        # if not local_query.exec_():
        #     print("Ошибка при проверке списка удаленных терминов: " + q_s)
        #     print(local_query.lastQuery())
        #     print(local_query.lastError().text())  # не получилось добавить - сообщи об ошибке
        #     return False

        cnt += 1
        self.count_trigger.emit(cnt)
        end = time.time()
        print("Time elapsed:")
        print(end - start)
        return True


def clear_local_termis():
    local_query = QSqlQuery(get_local_connection())
    local_query.prepare(clear_all_termins_query)
    if local_query.exec_():
        return True
    else:
        return False
