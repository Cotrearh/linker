import math
from PyQt4 import QtSql
from functools import partial

import re
import time
from PyQt4 import QtGui
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtGui import QTreeWidgetItemIterator
from PyQt4.QtSql import QSqlQuery

from DB import TerminDBUtils
from DB.BrokenLinksDeleter import BrokenLinksDeleter
from DB.TerminsRefresher import TerminsRefresher, clear_local_termis
from DB.data_base import get_local_connection, get_remote_connection
from DB.queries import show_termins_in_list_query, show_termins_in_list_count_query, show_brokenlinks_in_list_query, \
    show_brokenlinks_in_list_count_query, update_local_termin_query, update_remote_termin_query, \
    update_remote_termin_query_OC
from GUI.PyQt import mainwindow_ui
from config import Config
from slots.SelectLinkForReplace import SelectLinkForReplace
from slots.link_selector_slots import LinkSelectorDialog
from slots.settings_slots import Settings
from widgets.LinkerTextEditor.ExtendedTextEditor import ExtendedTextEdit
from utils.StringUtils import toInitialHtmlFormat


class MainWindow(QMainWindow, mainwindow_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.insert_link_attempts = 0

        self.RefreshThread = None

        self.local_cn = get_local_connection()
        self.remote_cn = get_remote_connection()
        self.setupUi(self)

        self.onlyClassified = False
        self.onlyClassifiedCheck.clicked.connect(self.switchOnlyClassified)

        self.terminNameLabel.setWordWrap(True)

        self.root = QTreeWidgetItem(self.terminsTreeWidget, ['description'])
        self.terminsTreeWidget.setRootIndex(self.terminsTreeWidget.indexFromItem(self.root))
        self.refreshTerminsListBtn.clicked.connect(self.refresh_termins_list)
        self.statusbar.showMessage('Версия программы: ' + Config.VERSION, -1)

        self.terminsPerPageComboBos.currentIndexChanged.connect(partial(self.show_termins_in_list, 1))
        self.searchLineEdit.textChanged.connect(partial(self.show_termins_in_list, 1))
        self.showLinkedCheck.clicked.connect(partial(self.show_termins_in_list, 1))

        self.root_brokenlinks = QTreeWidgetItem(self.brokenLinksTree, ['description'])
        self.brokenLinksTree.setRootIndex(self.brokenLinksTree.indexFromItem(self.root_brokenlinks))

        self.brokenlinksComboBox.currentIndexChanged.connect(partial(self.show_brokenlinks_in_list, 1))
        self.brokenlinksSearhLine.textChanged.connect(partial(self.show_brokenlinks_in_list, 1))

        self.show_termins_in_list(1)
        self.show_brokenlinks_in_list(1)

        self.brokenLinksTree.itemClicked.connect(self.brokenLinksTree_itemClicked)
        # self.terminsTreeWidget.itemClicked.connect(self.termin_tree_itemClicked)
        self.terminsTreeWidget.itemSelectionChanged.connect(self.termin_tree_itemClicked)

        self.refreshTerminListAction.triggered.connect(self.refresh_termins_list)
        self.clearTerminsListAction.triggered.connect(self.clear_termins_list)

        self.insertLinkBtn.clicked.connect(self.insert_link)

        self.saveBtn.clicked.connect(self.saveToDB)
        self.continueBtn.clicked.connect(self.saveAndContimue)
        self.passBtn.clicked.connect(self.passTerminBtn)

        self.currentPage = 1
        self.current_uuid = None

        self.decomposeLinksCheck.clicked.connect(partial(self.textEdit.decompose_deleted_link),
                                                 self.decomposeLinksCheck.isChecked())

        self.BLD = None  # BrokenLinksDeleter
        self.brokenLinkOkBtn.clicked.connect(self.brockenlink_ok_btn)
        self.deleteAllBrokenBtn.clicked.connect(self.delete_All_Broken_Btn)
        self.seectReplacementBrokenLinkBtn.clicked.connect(self.select_link_for_replace)
        self.brokenLinksNewUuid = None

        self.settingsAction.triggered.connect(self.openSettings)

    # Общие

    def openSettings(self):
        sw = Settings()
        sw.reopenConnectionTrigger.connect(self.reconnect)
        sw.exec_()

    def reconnect(self):
        print("RECON")
        self.remote_cn = get_remote_connection()

    # вкладка Расстановка ссылок
    def switchOnlyClassified(self):
        self.onlyClassified = self.onlyClassifiedCheck.isChecked()

    def saveToDB(self):
        if self.terminsTreeWidget.currentItem() is not None:
            html = self.textEdit.toHtml()
            if "##status##1##word##" not in html and "##status##2##word##" not in html:
                return self.save()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText('Не все найденные ссылки в определении были приняты. '
                            'Пожалуйста, проверьте все найденные ссылки и утвердите их. Также вы можете сохранить все '
                            'однозначные ссылки, при это неоднозначные будут удалены.')
                msg.setWindowTitle('Имеются не принятые ссылки')
                btnyes = msg.addButton("Сохранить однозначные ссылки", QMessageBox.YesRole)
                btnNotSave = msg.addButton("Сохранить принятые ссылки", QMessageBox.RejectRole)
                btnno = msg.addButton("Вернуться", QMessageBox.RejectRole)
                msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                msg.exec_()
                if msg.clickedButton() == btnyes:
                    return self.save(save_not_accepted=True)
                elif msg.clickedButton() == btnNotSave:
                    return self.save()
                elif msg.clickedButton() == btnno:
                    return False
        else:
            return False

    def save(self, save_not_accepted=False):
        text = self.textEdit.toInitialHtmlFormat()
        links = re.findall(r'<[Aa][^>]*>.*?</[Aa]>', text)
        for l in links:
            print("LINK - " + l)
            if "termin##" in l:
                href = re.findall(r'href=([^>]*?)>', l)[0]
                if "status##1##" in l:
                    if save_not_accepted:
                        print("HREF - " + href)
                        new_href = '"termin;' + href.split("##")[1].__str__() + '"'
                        print("NEW HREF - " + new_href)
                        new_l = l.replace(href, new_href)
                        print("NEW LINK - " + new_l)
                        # заменить и сохранить ссылку
                        text = text.replace(l, new_l)
                    else:
                        new_l = re.findall(r'<[Aa][^>]*>(.*?)</[Aa]>', l)[0]
                        print("RES TEXT - " + new_l)
                        text = text.replace(l, new_l)
                elif "status##2##" in l:
                    new_l = re.findall(r'<[Aa][^>]*>(.*?)</[Aa]>', l)[0]
                    print("RES TEXT - " + new_l)
                    # удалить ссылку, потому что не однозначная
                    text = text.replace(l, new_l)
                elif "status##" not in l:
                    print("HREF - " + href)
                    new_href = '"termin;' + href.split("##")[1].__str__() + '"'
                    print("NEW HREF - " + new_href)
                    new_l = l.replace(href, new_href)
                    print("NEW LINK - " + new_l)
                    text = text.replace(l, new_l)
                    # заменить и сохранить ссылку, т.к. она принята
                print('\n')
                print(text)

        local_update = QSqlQuery(self.local_cn)
        local_update.prepare(update_local_termin_query)
        local_update.bindValue(":linked", 1)
        local_update.bindValue(":uuid", self.current_uuid)

        remote_update = QSqlQuery(self.remote_cn)
        if self.onlyClassified:
            remote_update.prepare(update_remote_termin_query_OC)
        else:
            remote_update.prepare(update_remote_termin_query)
        remote_update.bindValue(":definition", text)
        remote_update.bindValue(":uuid", self.current_uuid)

        QtSql.QSqlDatabase.database('SQLiteConnection').transaction()
        QtSql.QSqlDatabase.database('PGconnection').transaction()
        local_status = False
        remote_status = False
        if remote_update.exec_():
            remote_status = True
        else:
            print(remote_update.lastQuery())
            print(remote_update.lastError().text())
        if local_update.exec_():
            local_status = True
        else:
            print(local_update.lastQuery())
            print(local_update.lastError().text())
        if local_status and remote_status:
            QtSql.QSqlDatabase.database('SQLiteConnection').commit()
            QtSql.QSqlDatabase.database('PGconnection').commit()
            return True
        else:
            QtSql.QSqlDatabase.database('SQLiteConnection').rollback()
            QtSql.QSqlDatabase.database('PGconnection').rollback()
            return False

    def saveAndContimue(self):
        if self.saveToDB():
            pos = int(self.terminsTreeWidget.currentItem().text(2))
            # self.root.takeChild(self.terminsTreeWidget.currentItem())
            self.show_termins_in_list(self.currentPage)
            self.go_to_termin_on_position(pos)

    def passTerminBtn(self):
        if int(self.terminsTreeWidget.currentItem().text(2)) == int(self.terminsPerPageComboBos.currentText()):
            self.show_termins_in_list(self.currentPage + 1)
            it = QTreeWidgetItemIterator(self.terminsTreeWidget)
            it.value()
            it += 1
            self.terminsTreeWidget.setCurrentItem(it.value())
            it.value().setSelected(True)
            return

        it = QTreeWidgetItemIterator(self.terminsTreeWidget)
        i = 0
        while it.value():
            if i == int(self.terminsTreeWidget.currentItem().text(2)):
                it += 1
                self.terminsTreeWidget.setCurrentItem(it.value())
                it.value().setSelected(True)
                return
            it += 1
            i += 1

    def go_to_termin_on_position(self, position):
        print(position)
        if position == int(self.terminsPerPageComboBos.currentText()):
            self.show_termins_in_list(self.currentPage + 1)
            it = QTreeWidgetItemIterator(self.terminsTreeWidget)
            it.value()
            it += 1
            self.terminsTreeWidget.setCurrentItem(it.value())
            it.value().setSelected(True)
            return

        it = QTreeWidgetItemIterator(self.terminsTreeWidget)
        i = 0
        while it.value():
            if i == position:
                if self.showLinkedCheck.isChecked():
                    it += 1
                self.terminsTreeWidget.setCurrentItem(it.value())
                it.value().setSelected(True)
                return
            it += 1
            i += 1

    # TODO убирать пробелы на концах выделения, если они там есть
    def insert_link(self):
        if not self.textEdit.textCursor().charFormat().isAnchor() \
                and '<a href="termin;' not in self.textEdit.textCursor().selection().toHtml() \
                and '</a>' not in self.textEdit.textCursor().selection().toHtml():
            self.insert_link_attempts = 0
            w = LinkSelectorDialog(self.textEdit.textCursor().selectedText(),
                                   toInitialHtmlFormat(self.textEdit.textCursor().selection().toHtml()), self.onlyClassified)
            w.insert_trigger.connect(self.textEdit.insert_link)
            w.exec_()
        else:
            if self.insert_link_attempts == 2:
                self.insert_link_attempts = 0
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText('Вы пытаетесь вставить ссылку в фрагмент текста, который уже содержит ссылки или части '
                            'ссылок. Пожалуйста, измените границы фрагмента или удалите ссылки в выбранном фрагменте.')
                msg.setWindowTitle('Невозможно вставить ссылку')
                btnyes = msg.addButton("Ок", QMessageBox.YesRole)
                msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                msg.exec_()
                if msg.clickedButton() == btnyes:
                    msg.close()
            else:
                self.insert_link_attempts += 1

    def clear_termins_list(self):
        if clear_local_termis():
            self.root.takeChildren()
            self.root_brokenlinks.takeChildren()

    def refresh_termins_list(self):
        self.RefreshThread = TerminsRefresher(self.onlyClassified)
        self.RefreshThread.finishTrigger.connect(partial(self.show_termins_in_list, 1))
        self.RefreshThread.finishTrigger.connect(partial(self.show_brokenlinks_in_list, 1))
        self.RefreshThread.finishTrigger.connect(self.RefreshThread.progress.close)
        self.RefreshThread.count_trigger.connect(self.RefreshThread.progress.setValue)
        self.RefreshThread.msg_trigger.connect(self.RefreshThread.progress.setLabelText)
        self.RefreshThread.start()
        self.RefreshThread.progress.exec_()

    def show_termins_in_list(self, page):
        self.currentPage = page
        # фильтрация списка терминов
        search_word = self.searchLineEdit.text()
        if search_word.strip() != '':
            search_str = search_word
        else:
            search_str = ''

        # показ уже обработанных терминов
        if self.showLinkedCheck.isChecked():
            show_linked = 1
        else:
            show_linked = 0

        query = QSqlQuery(self.local_cn)
        LIMIT = int(self.terminsPerPageComboBos.currentText())
        OFFSET = (page - 1) * LIMIT
        query.prepare(show_termins_in_list_query)
        query.bindValue(':search_str', search_str + '%')
        query.bindValue(':linked', show_linked)
        query.bindValue(':limit', LIMIT.__str__())
        query.bindValue(':offset', OFFSET.__str__())
        if query.exec_():
            self.root.takeChildren()
            i = 1
            f = QFont()
            f.setBold(True)
            while query.next():
                c = QTreeWidgetItem()
                c.setText(0, query.value(0))  # Заглавное слово
                c.setData(1, 0, query.value(1))  # uuid
                c.setData(2, 0, i)  # номерок
                if query.value(2) == 1:
                    c.setFont(0, f)
                self.root.addChild(c)
                i += 1

            pages = 1
            query.prepare(show_termins_in_list_count_query)
            query.bindValue(':search_str', search_str + '%')
            query.bindValue(':linked', show_linked)
            if query.exec_() and query.next():
                try:
                    pages = math.ceil(query.value(0) / LIMIT)
                except:
                    pages = 1

            self.draw_paginator(pages, page)
        else:
            print(query.lastError().text())
            print("not exec")
        self.terminsTreeWidget.scrollToTop()

    def draw_paginator(self, pages, current_page):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        for i in reversed(range(self.terminListPaginatorLayout.count())):
            self.terminListPaginatorLayout.itemAt(i).widget().close()
            self.terminListPaginatorLayout.itemAt(i).widget().setParent(None)
        i = 1
        flag1 = True
        flag2 = True
        while i <= pages:
            if (abs(current_page - i) <= 2) or (abs(pages - i) <= 2) or (i <= 3):
                btn = QPushButton(i.__str__())
                btn.clicked.connect(partial(self.show_termins_in_list, i))
                btn.setSizePolicy(sizePolicy)
                if i == current_page:
                    btn.setAutoFillBackground(True)
                    btn.setStyleSheet("background-color: rgb(179,255,255)")
                self.terminListPaginatorLayout.addWidget(btn)
            else:
                if i < current_page and flag1:
                    flag1 = False
                    btn = QPushButton("...")
                    btn.clicked.connect(partial(self.show_termins_in_list, current_page - 6))
                    btn.setSizePolicy(sizePolicy)
                    self.terminListPaginatorLayout.addWidget(btn)
                if i > current_page and flag2:
                    flag2 = False
                    btn = QPushButton("...")
                    btn.clicked.connect(partial(self.show_termins_in_list, current_page + 6))
                    btn.setSizePolicy(sizePolicy)
                    self.terminListPaginatorLayout.addWidget(btn)
            i += 1

    def termin_tree_itemClicked2(self):
        self.verticalWidget.setEnabled(False)
        self.insert_link_attempts = 0
        if self.terminsTreeWidget.currentItem() is not None:
            self.textEdit.clear()
            self.current_uuid = self.terminsTreeWidget.currentItem().text(1)
            self.terminNameLabel.setText("Термин: " + self.terminsTreeWidget.currentItem().text(0))
            if TerminDBUtils.checkTerminExists(self.current_uuid, self.onlyClassified):
                # print(TerminDBUtils.getDefinition(self.current_uuid) + '\n\n')
                self.textEdit.insertHtml(TerminDBUtils.getDefinition(self.current_uuid, self.onlyClassified))
                # print(self.textEdit.toHtml() + '\n\n')
                self.textEdit.seacrh_links_in_text(5, self.current_uuid)
                self.textEdit.setText(self.textEdit.toHtml().replace(" </span>", "</span> "))
                # print(TerminDBUtils.getDefinition(current_uuid) + '\n\n')
                # print(self.textEdit.toInitialHtmlFormat() + '\n\n')
                # print(self.textEdit.toHtml() + '\n\n')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText('Запрашиваемый термин не найден в удалённой БД. Возможно он был удален или Вы подключились '
                            'к другой БД. Пожалуйста, обновите список терминов.')
                msg.setWindowTitle('Термин не найден')
                btnyes = msg.addButton("Ок", QMessageBox.YesRole)
                msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                msg.exec_()
                if msg.clickedButton() == btnyes:
                    msg.close()
        self.verticalWidget.setEnabled(True)
        self.terminsTreeWidget.setFocus()

    def termin_tree_itemClicked(self):
        self.verticalWidget.setEnabled(False)
        self.insert_link_attempts = 0
        uuids = []
        TE = ExtendedTextEdit()
        if self.terminsTreeWidget.currentItem() is not None:
            TE.clear()
            query = QSqlQuery(self.local_cn)

            if query.exec_("SELECT uuid FROM termins"):
                while query.next():
                    self.current_uuid = query.value(0)
                    uuids.append(query.value(0))
            else:
                print(query.lastError().text())
                self.current_uuid = self.terminsTreeWidget.currentItem().text(1)
            
            #print(uuids)
            
            total_links = 0
            single_term = 0
            multiple_term = 0
            length = len(uuids)
            count = 0
            start = time.time()
            with open("report" + time.time().__str__() + ".txt", 'a') as out:
                out.write("total;single;multiple;\n")
                for uuid in uuids:
                    count += 1
                    print (count, sep=' ', end=' ', flush=True)
                    TE.clear()
                    self.current_uuid = uuid
                    if TerminDBUtils.checkTerminExists(self.current_uuid, self.onlyClassified):
                        TE.insertHtml(TerminDBUtils.getDefinition(self.current_uuid, self.onlyClassified))
                        TE.seacrh_links_in_text(5, self.current_uuid)
                        TE.setText(TE.toHtml().replace(" </span>", "</span> "))
                                
                        single_term += TE.single_term
                        multiple_term += TE.multiple_term
                    
                        out.write((TE.single_term + TE.multiple_term).__str__() + ";" + TE.single_term.__str__() + ";" + TE.multiple_term.__str__() + ";\n")
                                
                        TE.single_term = 0
                        TE.multiple_term = 0
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText('Запрашиваемый термин не найден в удалённой БД. Возможно он был удален или Вы подключились '
                                    'к другой БД. Пожалуйста, обновите список терминов.')
                        msg.setWindowTitle('Термин не найден')
                        btnyes = msg.addButton("Ок", QMessageBox.YesRole)
                        msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                        msg.exec_()
                        if msg.clickedButton() == btnyes:
                            msg.close()
            end = time.time()
            print("\nTotal time:")
            print(end - start)
            print("SINGLE:")
            print(single_term)
            print("MULTIPLE:")
            print(multiple_term)
        self.verticalWidget.setEnabled(True)
        self.terminsTreeWidget.setFocus()

    # вкладка Битые ссылки

    def show_brokenlinks_in_list(self, page):
        # фильтрация списка терминов
        search_word = self.brokenlinksSearhLine.text()
        if search_word.strip() != '':
            search_str = search_word
        else:
            search_str = ''

        query = QSqlQuery(self.local_cn)
        LIMIT = int(self.brokenlinksComboBox.currentText())
        OFFSET = (page - 1) * LIMIT
        query.prepare(show_brokenlinks_in_list_query)
        query.bindValue(':search_str', search_str + '%')
        query.bindValue(':limit', LIMIT.__str__())
        query.bindValue(':offset', OFFSET.__str__())
        if query.exec_():
            self.root_brokenlinks.takeChildren()
            while query.next():
                c = QTreeWidgetItem()
                c.setText(0, query.value(0))  # Заглавное слово
                c.setData(1, 0, query.value(1))  # uuid
                self.root_brokenlinks.addChild(c)

            pages = 1
            query.prepare(show_brokenlinks_in_list_count_query)
            query.bindValue(':search_str', search_str + '%')
            if query.exec_() and query.next():
                try:
                    pages = math.ceil(query.value(0) / LIMIT)
                except:
                    pages = 1

            self.draw_brokenlinks_paginator(pages, page)
        else:
            print(query.lastError().text())
            print("not exec")
        self.brokenLinksTree.scrollToTop()

    def draw_brokenlinks_paginator(self, pages, current_page):
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        for i in reversed(range(self.brokenLinksPaginatorLayout.count())):
            self.brokenLinksPaginatorLayout.itemAt(i).widget().close()
            self.brokenLinksPaginatorLayout.itemAt(i).widget().setParent(None)
        i = 1
        flag1 = True
        flag2 = True
        while i <= pages:
            if (abs(current_page - i) <= 2) or (abs(pages - i) <= 2) or (i <= 3):
                btn = QPushButton(i.__str__())
                btn.clicked.connect(partial(self.show_brokenlinks_in_list, i))
                btn.setSizePolicy(sizePolicy)
                if i == current_page:
                    btn.setAutoFillBackground(True)
                    btn.setStyleSheet("background-color: rgb(179,255,255)")
                self.brokenLinksPaginatorLayout.addWidget(btn)
            else:
                if i < current_page and flag1:
                    flag1 = False
                    btn = QPushButton("...")
                    btn.clicked.connect(partial(self.show_brokenlinks_in_list, current_page - 6))
                    btn.setSizePolicy(sizePolicy)
                    self.brokenLinksPaginatorLayout.addWidget(btn)
                if i > current_page and flag2:
                    flag2 = False
                    btn = QPushButton("...")
                    btn.clicked.connect(partial(self.show_brokenlinks_in_list, current_page + 6))
                    btn.setSizePolicy(sizePolicy)
                    self.brokenLinksPaginatorLayout.addWidget(btn)
            i += 1

    def brokenLinksTree_itemClicked(self):
        self.brokenLinksActionsWidget.setEnabled(True)
        self.deleteAllToThisBtn.setChecked(True)
        self.brokenRepalcementText.clear()
        self.brokenLinksNewUuid = None
        self.label_2.setText('Заглавное слово: ' + self.brokenLinksTree.currentItem().text(0))

    def brockenlink_ok_btn(self):
        if self.deleteAllToThisBtn.isChecked():
            # delete all to this
            self.brokenLinksTab.setEnabled(False)
            self.BLD = BrokenLinksDeleter(0, uuid=self.brokenLinksTree.currentItem().text(1), onlyClassified=self.onlyClassified)
            self.BLD.finishTrigger.connect(partial(self.show_brokenlinks_in_list, 1))
            self.BLD.finishTrigger.connect(self.BLD.d.close)
            self.BLD.finishTrigger.connect(self.brokenLinksTab.setEnabled)
            self.BLD.start()
            self.BLD.d.exec_()
        elif self.replaceAllToThisBtn.isChecked():
            # check? that selected and replace? then delete this
            if self.brokenLinksNewUuid is not None:
                self.brokenLinksTab.setEnabled(False)
                self.BLD = BrokenLinksDeleter(1, uuid=self.brokenLinksTree.currentItem().text(1),
                                              new_uuid=self.brokenLinksNewUuid, onlyClassified=self.onlyClassified)
                self.BLD.finishTrigger.connect(partial(self.show_brokenlinks_in_list, 1))
                self.BLD.finishTrigger.connect(self.BLD.d.close)
                self.BLD.finishTrigger.connect(self.brokenLinksTab.setEnabled)
                self.BLD.start()
                self.BLD.d.exec_()
            else:
                self.select_link_for_replace()

    def delete_All_Broken_Btn(self):
        self.brokenLinksTab.setEnabled(False)
        self.BLD = BrokenLinksDeleter(2, onlyClassified=self.onlyClassified)
        self.BLD.finishTrigger.connect(partial(self.show_brokenlinks_in_list, 1))
        self.BLD.finishTrigger.connect(self.BLD.d.close)
        self.BLD.finishTrigger.connect(self.brokenLinksTab.setEnabled)
        self.BLD.start()
        self.BLD.d.exec_()

    def select_link_for_replace(self):
        w = SelectLinkForReplace(self.brokenLinksTree.currentItem().text(0), self.onlyClassified)
        # w = SelectLinkForReplace('АВА')
        w.exec_()
        if w.status:
            self.brokenRepalcementText.setText(w.name)
            self.brokenLinksNewUuid = w.selected_uuid
            self.replaceAllToThisBtn.setChecked(True)
