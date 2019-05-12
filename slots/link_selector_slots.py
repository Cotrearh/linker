from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4.QtSql import QSqlQuery

from DB import TerminDBUtils
from DB.data_base import get_local_connection
from DB.queries import show_termins_in_link_selector_query
from GUI.PyQt.select_link_dialog_ui import Ui_select_link_dialog as ui
from utils.StringUtils import stem_str


class LinkSelectorDialog(ui, QDialog):
    accept_trigger = pyqtSignal(str)
    insert_trigger = pyqtSignal(str)

    def __init__(self, word, html, onlyClassified):
        super().__init__()
        self.setupUi(self)
        self.local_cn = get_local_connection()
        self.word = word
        self.html = html
        self.onlyClassified = onlyClassified
        self.filterEdit.setText(self.word)
        self.root = QTreeWidgetItem(self.treeWidget, ['description'])
        self.treeWidget.setRootIndex(self.treeWidget.indexFromItem(self.root))

        self.treeWidget.itemSelectionChanged.connect(self.tree_item_clicked)

        self.AcceptBtn.clicked.connect(self.ok_click)
        self.cancelBtn.clicked.connect(self.cancel_click)

        self.filterEdit.textChanged.connect(self.fill_fields)

        self.selected_uuid = None
        
        self.fill_fields()

    def ok_click(self):
        if self.selected_uuid is not None:
            self.accept_trigger.emit(self.selected_uuid)
            self.insert_trigger.emit("<a href=\"termin##" + self.selected_uuid + "##initialhtml##" +
                                     self.html.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;") +
                                     "\">" + self.html + "</a>")
            self.close()

    def cancel_click(self):
        self.close()

    def fill_fields(self):

        search_word = self.filterEdit.text()
        if search_word.strip() != '':
            search_str = stem_str(search_word)
        else:
            search_str = ''

        query = QSqlQuery(self.local_cn)
        LIMIT = 100
        OFFSET = 0
        query.prepare(show_termins_in_link_selector_query)
        query.bindValue(':search_str', search_str + '%')
        query.bindValue(':linked', 1)
        query.bindValue(':limit', LIMIT.__str__())
        query.bindValue(':offset', OFFSET.__str__())
        if query.exec_():
            self.root.takeChildren()
            while query.next():
                c = QTreeWidgetItem()
                c.setText(0, query.value(0))  # Заглавное слово
                c.setData(1, 0, query.value(1))  # uuid
                self.root.addChild(c)
        else:
            print(query.lastError().text())
            print("not exec")
        self.treeWidget.scrollToTop()

    def tree_item_clicked(self):
        if self.treeWidget.currentItem() is not None:
            self.textEdit.clear()
            self.selected_uuid = self.treeWidget.currentItem().text(1)
            if TerminDBUtils.checkTerminExists(self.selected_uuid, self.onlyClassified):
                self.textEdit.insertHtml(TerminDBUtils.getDefinition(self.selected_uuid, self.onlyClassified))
                self.textEdit.setText(self.textEdit.toHtml().replace(" </span>", "</span> "))
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
