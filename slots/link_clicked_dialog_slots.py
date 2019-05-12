from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QDialog
from PyQt4.QtSql import QSqlQuery

from DB.data_base import get_remote_connection
from DB.queries import get_name_and_short_def_query, get_name_and_short_def_query_OC
from GUI.PyQt.linkclickeddialog_ui import Ui_linkClickedDialog as ui
from slots.link_selector_slots import LinkSelectorDialog
from utils.StringUtils import remove_all_tags


class LinkClickedDialog(ui, QDialog):
    accept_trigger = pyqtSignal(str)
    delete_trigger = pyqtSignal(str)
    edit_trigger = pyqtSignal()
    cancel_trigger = pyqtSignal()

    def __init__(self, uuid, word, html, decompose_deleted, exclude_uuid, onlyClassified):
        super().__init__()
        self.uuid = uuid
        self.exclude_uuid = exclude_uuid
        self.decompose_deleted = decompose_deleted
        self.word = word
        self.html = html
        self.onlyClassified = onlyClassified
        self.setupUi(self)
        self.cancelBtn.clicked.connect(self.cancel_trigger.emit)
        self.acceptBtn.clicked.connect(self.accept_link)
        self.deleteBtn.clicked.connect(self.remove_link)
        self.editBtn.clicked.connect(self.edit_link)
        self.fill_fields()

    def fill_fields(self):
        query = QSqlQuery(get_remote_connection())
        if self.onlyClassified:
            query.prepare(get_name_and_short_def_query_OC)
        else:
            query.prepare(get_name_and_short_def_query)
        query.bindValue(':uuid', self.uuid)
        if query.exec_():
            if query.next():
                self.mainWordLabel.setText('Ссылка на термин: <b>' + query.value(0) + "</b>")
                short_def = remove_all_tags(query.value(1))
                if len(query.value(1)) < 299:
                    self.definitionLabel.setText("Определение: " + short_def)
                else:
                    self.definitionLabel.setText("Определение: " + short_def + '...')
            else:
                self.mainWordLabel.setText('Термин не найден')
                self.definitionLabel.setText("Возможно термин, на который ведет данная ссылка был удален или"
                                             " Вы подключились к другой БД. Пожалуйста, обновите список терминов.")
        else:
            print(query.lastError().text())
            print(query.lastQuery())

    def accept_link(self):
        link = "<a href=\"termin##" + self.uuid + "##initialhtml##" + \
               self.html.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;") + "\">" + self.html + "</a>"
        self.accept_trigger.emit(link)
        self.close()

    def edit_link(self):
        w = LinkSelectorDialog(self.word, self.html, self.onlyClassified)
        w.accept_trigger.connect(self.change_uuid)
        w.accept_trigger.connect(self.accept_link)
        w.exec_()

    def change_uuid(self, uuid):
        self.uuid = uuid

    def remove_link(self):
        link = self.html
        if self.decompose_deleted:
            link = self.decompose_link(link)
        self.accept_trigger.emit(link)
        self.close()
        # self.decompose_link(link)

    def decompose_link(self, text):
        n = len(text.split(' '))
        if n > 1:
            from widgets.LinkerTextEditor.ExtendedTextEditor import ExtendedTextEdit
            ete = ExtendedTextEdit(onlyClassified=self.onlyClassified)
            ete.setText(text)
            print(n)
            ete.seacrh_links_in_text(n - 1, self.exclude_uuid)
            text = ete.toHtml()
            ete.close()
        return text
