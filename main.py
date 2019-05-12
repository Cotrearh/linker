import sys

from PyQt4 import QtGui
from PyQt4.QtGui import QApplication

from DB.data_base import open_connection_to_remote, open_connection_to_local
from config import Config
from slots.main_window_slots import MainWindow

if __name__ == '__main__':
    Config()

    app = QApplication(sys.argv)
    app.setFont(QtGui.QFont(Config.DEFAULT_FONT, int(Config.DEFAULT_FONT_SIZE)))


    open_connection_to_remote()
    open_connection_to_local()

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
