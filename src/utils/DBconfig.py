# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser


class DBConfig:
    def __init__(self, fin, gen=False):
        self.__file = fin
        self.__cfgParser = ConfigParser()

        if not gen:
            self.reload()

    def reload(self):
        self.__cfgParser.read(self.__file)

        self.DB = self.__cfgParser.get('DB', 'db')
        self.DB_MODE = self.__cfgParser.get('DB', 'mode')

        self.DB_HOST = self.__cfgParser.get(self.DB, 'host')
        self.DB_PORT = self.__cfgParser.getint(self.DB, 'port')
        self.DB_USER = self.__cfgParser.get(self.DB, 'user')
        self.DB_PASSWORD = self.__cfgParser.get(self.DB, 'passwd')
        self.DB_NAME = self.__cfgParser.get(self.DB, 'name')

        if self.DB_MODE == "LOCAL":
            self.DB_HOST = "127.0.0.1"
