import re

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QTextBrowser
from PyQt4.QtGui import QTextCursor

from DB.TerminDBUtils import prepareLinkFromWordInDB
from slots.link_clicked_dialog_slots import LinkClickedDialog
from slots.link_selector_slots import LinkSelectorDialog
from utils.StringUtils import stoplist, stoplist_list, stoplist_non_chars, toInitialHtmlFormat


class ExtendedTextEdit(QTextBrowser):
    def __init__(self, *__args, onlyClassified=False):
        super().__init__(*__args)
        self.setOpenExternalLinks(False)
        self.setOpenLinks(False)
        self.anchorClicked.connect(self.link_clicked)
        self.decompose_deleted_link_flag = True
        self.exclude_uuid = None
        self.onlyClassified = onlyClassified
        self.total_links = 0
        self.single_term = 0
        self.multiple_term = 0

    def decompose_deleted_link(self, flag):
        self.decompose_deleted_link_flag = flag

    def link_clicked(self, link):
        # print(link)
        # print("HTML - " + re.sub(r'</*[Aa][^>]*>', '', toInitialHtmlFormat(self.textCursor().selection().toHtml())))
        HTML = re.sub(r'</*[Aa][^>]*>', '', toInitialHtmlFormat(self.textCursor().selection().toHtml()))
        try:
            link = link.toString()
        except:
            link = link.__str__()

        if "termin##" in link:
            attributes = link.split('##')
            # если есть параметр статуса в ссылке, значит работаем с ней как с новой ссылкой
            if "status" in link:
                if attributes[3] == '1':
                    w = LinkClickedDialog(attributes[1], attributes[5], HTML, self.decompose_deleted_link_flag,
                                          self.exclude_uuid, self.onlyClassified)
                    w.cancel_trigger.connect(w.close)
                    w.accept_trigger.connect(self.insert_link)
                    w.exec_()
                elif attributes[3] == '2':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText('Фрагменту определения <b>"' + self.textCursor().selectedText() +
                                '"</b> соответствуют несколько терминов. Выберите действие.')
                    msg.setWindowTitle('Найдено несколько ссылок')
                    btnyes = msg.addButton("Выбрать из списка", QMessageBox.YesRole)
                    btnno = msg.addButton("Удалить", QMessageBox.RejectRole)
                    btncancel = msg.addButton("Отмена", QMessageBox.RejectRole)
                    msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    msg.exec_()
                    if msg.clickedButton() == btnyes:
                        w = LinkSelectorDialog(attributes[5], HTML, self.onlyClassified)
                        w.insert_trigger.connect(self.insert_link)
                        w.exec_()
                    elif msg.clickedButton() == btnno:
                        self.insert_link(HTML)
                    elif msg.clickedButton() == btncancel:
                        msg.close()
            else:
                w = LinkClickedDialog(attributes[1], self.textCursor().selectedText(), HTML,
                                      self.decompose_deleted_link_flag, self.exclude_uuid, self.onlyClassified)
                w.cancel_trigger.connect(w.close)
                w.accept_trigger.connect(self.insert_link)
                w.exec_()
        elif "termin;" in link:
            attributes = link.split(';')
            w = LinkClickedDialog(attributes[1], self.textCursor().selectedText(), HTML,
                                  self.decompose_deleted_link_flag, self.exclude_uuid, self.onlyClassified)
            w.cancel_trigger.connect(w.close)
            w.accept_trigger.connect(self.insert_link)
            w.exec_()
        elif "source;" in link:
            pass  # ссылки на источники не трогаем
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Фрагмент определения <b>"' + self.textCursor().selectedText() +
                        '"</b> отмечен ссылкой неизвестного формата. Выберите действие.')
            msg.setWindowTitle('Ссылка неизвестного формата')
            btnyes = msg.addButton("Редактировать", QMessageBox.YesRole)
            btnno = msg.addButton("Удалить", QMessageBox.RejectRole)
            btncancel = msg.addButton("Отмена", QMessageBox.RejectRole)
            msg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            msg.exec_()
            if msg.clickedButton() == btnyes:
                w = LinkSelectorDialog(self.textCursor().selectedText(), HTML, self.onlyClassified)
                w.insert_trigger.connect(self.insert_link)
                w.exec_()
            elif msg.clickedButton() == btnno:
                self.insert_link(HTML)
            elif msg.clickedButton() == btncancel:
                msg.close()

    def insert_link(self, link):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.KeepAnchor)
        cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        cursor.insertHtml(link)
        self.setTextCursor(cursor)
        self.textCursor().endEditBlock()

    # вывод html для БД
    def toInitialHtmlFormat(self):
        return toInitialHtmlFormat(self.toHtml())

    # TODO возможно сделать так, чтобы ссылки не дублировались?
    def seacrh_links_in_text(self, n, exclude_uuid):
        self.exclude_uuid = exclude_uuid
        if self.toPlainText().strip() != '':
            cursor = self.textCursor()
            cursor.beginEditBlock()
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
            while not cursor.atEnd():
                QCoreApplication.processEvents()
                pos = cursor.position()
                if n > 1:
                    while len(cursor.selectedText().strip().split(' ')) < n:
                        QCoreApplication.processEvents()
                        cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)
                        # если первое выделенное слово в стоплисте, то идем далее
                        if cursor.selectedText().strip().lower() in stoplist \
                                and len(cursor.selectedText().strip().split(' ')) == 1:
                            cursor.clearSelection()
                        if cursor.charFormat().isAnchor():
                            cursor.clearSelection()
                            break
                        if "<a" in cursor.selection().toHtml() or "<A" in cursor.selection().toHtml() or "</a" \
                                in cursor.selection().toHtml() or "</A" in cursor.selection().toHtml():
                            cursor.clearSelection()
                            break
                        if cursor.atEnd():
                            break
                    while cursor.selectedText().strip().split(' ')[-1].lower() in stoplist_list:
                        QCoreApplication.processEvents()
                        cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.KeepAnchor)
                    while cursor.selectedText().strip()[-1:].lower() in stoplist_non_chars:
                        QCoreApplication.processEvents()
                        cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.KeepAnchor)
                    while cursor.selectedText().endswith(' '):
                        QCoreApplication.processEvents()
                        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                    WordInDB = prepareLinkFromWordInDB(cursor.selectedText().strip(), cursor.selection().toHtml(),
                                                       exclude_uuid)
                    if WordInDB is not None:
                        if "##status##1##" in WordInDB['link']:
                            self.single_term += 1
                        if "##status##2##" in WordInDB['link']:
                            self.multiple_term += 1
                        cursor.insertHtml(WordInDB['link'])
                    if cursor.atEnd():
                        break
                    cursor.setPosition(pos)
                    cursor.movePosition(QTextCursor.WordRight)
                    while cursor.charFormat().isAnchor() and not cursor.atEnd():
                        cursor.movePosition(QTextCursor.WordRight)
                elif n == 1:
                    QCoreApplication.processEvents()
                    cursor.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)
                    if cursor.charFormat().isAnchor():
                        cursor.clearSelection()
                    if "<a" in cursor.selection().toHtml() or "<A" in cursor.selection().toHtml() or "</a" \
                            in cursor.selection().toHtml() or "</A" in cursor.selection().toHtml():
                        cursor.clearSelection()
                    if cursor.selectedText().strip() not in stoplist and cursor.selectedText().strip() != '':
                        while cursor.selectedText().endswith(' '):
                            QCoreApplication.processEvents()
                            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                        WordInDB = prepareLinkFromWordInDB(cursor.selectedText().strip(), cursor.selection().toHtml(),
                                                           exclude_uuid)
                        if WordInDB is not None:
                            if "##status##1##" in WordInDB['link']:
                                self.single_term += 1
                            if "##status##2##" in WordInDB['link']:
                                self.multiple_term += 1
                            cursor.insertHtml(WordInDB['link'])
                    cursor.clearSelection()
            # print(len(list))
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
            self.textCursor().endEditBlock()
            n -= 1
            if n > 0:
                self.seacrh_links_in_text(n, exclude_uuid)
