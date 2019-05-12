from PyQt4 import QtSql
from PyQt4.QtCore import pyqtSignal

from PyQt4.QtGui import QDialog

from DB.data_base import open_connection_to_remote
from GUI.PyQt.settings_ui import Ui_settings as ui
from config import Config


class Settings(ui, QDialog):
    reopenConnectionTrigger = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cancelBtn.clicked.connect(self.close)
        self.saveBtn.clicked.connect(self.save)
        self.fill_fields()

    def fill_fields(self):
        self.nameEdit.setText(Config.DB_NAME.__str__())
        self.hostEdit.setText(Config.DB_HOST.__str__())
        self.portEdit.setText(Config.DB_PORT.__str__())
        self.userEdit.setText(Config.DB_USER_NAME.__str__())
        self.passwordEdit.setText(Config.DB_PASSWORD.__str__())

    def save(self):
        settings = Config.get_settings()
        settings.setValue('DB_NAME', self.nameEdit.text())
        settings.setValue('DB_HOST', self.hostEdit.text())
        settings.setValue('DB_PORT', self.portEdit.text())
        settings.setValue('DB_USER_NAME', self.userEdit.text())
        settings.setValue('DB_PASSWORD', self.passwordEdit.text())
        Config.load_settings()
        QtSql.QSqlDatabase.database('PGconnection').close()
        if open_connection_to_remote() is not None:
            self.reopenConnectionTrigger.emit()
            self.close()
