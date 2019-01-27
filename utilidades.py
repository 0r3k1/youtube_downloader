#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from urllib.request import urlopen
from six import BytesIO

def children(parent, hijo):
    children = parent.GetChildren()
    hijos = []

    for child in children:
        widget = child.GetWindow()
        if isinstance(widget, hijo):
            hijos.append(widget)

    return hijos

def miniatura(url_miniatura):
    img = urlopen(url_miniatura).read()
    return BytesIO(img)

def video_peso(peso):
    pesos = ("bits", "bytes", "MB", "GB")
    aux = peso
    size = 0
    cont = -1

    while aux > 1:
        size = aux
        aux /= 1024
        cont += 1

    return "{0}/{1}".format(round(size, 1), pesos[cont])

def exist_dir(path):
    if not os.path.isdir(path):
        first_path = os.getcwd()
        dir = path.split(os.sep)
        os.chdir(os.sep.join(dir[:len(dir)-1]))
        os.mkdir(dir[len(dir)-1])
        os.chdir(first_path)

def back_dir(path):
    dir = path.split(os.sep)
    return os.sep.join(dir[:len(dir)-1])

def get_query(opt):
    return "0, '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}'".format(
    opt.video_formato, opt.video_directorio,
    opt.musica_formato, opt.musica_directorio,
    opt.lista_formato, opt.lista_directorio, opt.lista_carpeta, opt.lista_enumera
    )

def rename(path, last, new):
    name = os.path.join(path, new)
    other = os.path.join(path, last)

    os.rename(other, name)


class _opt(object):
    def __init__(self):
        self.video_formato = None
        self.video_directorio = None

        self.musica_formato = None
        self.musica_directorio = None

        self.lista_formato = None
        self.lista_directorio = None
        self.lista_carpeta = True
        self.lista_enumera = True
