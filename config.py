import os

from PyQt4.QtCore import QSettings


class Config:
    VERSION = '0.2.2'
    script_directory = os.path.dirname(os.path.realpath(__file__))

    DB_NAME = None
    DB_HOST = None
    DB_PORT = None
    DB_USER_NAME = None
    DB_PASSWORD = None

    LOCAL_DB_NAME = None

    DEFAULT_FONT_SIZE = None
    DEFAULT_FONT = None

    def __init__(self):
        Config.load_settings()

    @staticmethod
    def get_settings():
        settings = QSettings(os.path.dirname(os.path.realpath(__file__)) + "/settings.ini", QSettings.IniFormat)
        return settings

    @staticmethod
    def load_settings():
        settings = QSettings(os.path.dirname(os.path.realpath(__file__)) + "/settings.ini", QSettings.IniFormat)
        Config.DB_NAME = settings.value('DB_NAME')
        Config.DB_HOST = settings.value('DB_HOST')
        Config.DB_PORT = int(settings.value('DB_PORT'))
        Config.DB_USER_NAME = settings.value('DB_USER_NAME')
        Config.DB_PASSWORD = settings.value('DB_PASSWORD')

        Config.LOCAL_DB_NAME = Config.script_directory + settings.value('LOCAL_DB_NAME')

        Config.DEFAULT_FONT_SIZE = settings.value('DEFAULT_FONT_SIZE')
        Config.DEFAULT_FONT = settings.value('DEFAULT_FONT')

    #
    # def load_shortcuts(Config):
    #     pass
    #
    # def load_defaults(Config):
    #     pass
