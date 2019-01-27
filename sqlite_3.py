#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from utilidades import _opt

class sqlite_3(object):
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "dat")
        self.exist_dir()
        self.exist = False
        if self.crear_tabla():
            self.con = sqlite3.connect(os.path.join(self.path, "opt.db"))
            self.cursor = self.con.cursor()

    def exist_dir(self):
        if not os.path.isdir(self.path):
            os.mkdir("dat")

    def crear_tabla(self):
        if not os.path.isfile(os.path.join(self.path, "opt.db")):
            self.con = sqlite3.connect(os.path.join(self.path, "opt.db"))
            self.cursor = self.con.cursor()
            self.exist = True
            query = """
            create table opciones(
            id integer prymary key not null,
            video_formato txt not null,
            video_directorio txt not null,
            musica_formato txt not null,
            musica_directorio txt not null,
            lista_formato txt not null,
            lista_directorio txt not null,
            lista_carpeta integer not null,
            lista_enumera integer not null
            );
            """
            self.cursor.execute(query)
            return False
        return True

    def insert(self, values):
        query = """insert into opciones (
        id,
        video_formato,
        video_directorio,
        musica_formato,
        musica_directorio,
        lista_formato,
        lista_directorio,
        lista_carpeta,
        lista_enumera
        ) values({0})
        """.format(values)
        self.cursor.execute(query)
        self.con.commit()

    def get_values(self):
        self.cursor.execute("select * from opciones")
        opt = _opt
        for registro in self.cursor:
            opt.video_formato = registro[1]
            opt.video_directorio = registro[2]
            opt.musica_formato = registro[3]
            opt.musica_directorio = registro[4]
            opt.lista_formato = registro[5]
            opt.lista_directorio = registro[6]
            opt.lista_carpeta = registro[7]
            opt.lista_enumera = registro[8]

        return opt

    def update(self, opt):
        query = "update opciones set "
        query += "video_formato = '{0}',".format(opt.video_formato)
        query += "video_directorio = '{0}',".format(opt.video_directorio)
        query += "musica_formato = '{0}',".format(opt.musica_formato)
        query += "musica_directorio = '{0}',".format(opt.musica_directorio)
        query += "lista_formato = '{0}',".format(opt.lista_formato)
        query += "lista_directorio = '{0}',".format(opt.lista_directorio)
        query += "lista_carpeta = {0},".format(opt.lista_carpeta)
        query += "lista_enumera = {0}".format(opt.lista_enumera)

        self.cursor.execute(query)
        self.con.commit()

    def close(self):
        self.con.close()

    def __del__(self):
        if self.exist:
            self.con.close()

def main():
    sql = sqlite_3()
    sql.get_values()

if __name__ == '__main__':
    main()
