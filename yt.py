#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pafy, os
from utilidades import *

class video(object):
    def __init__(self):
        self.titulo = ""
        self.categoria = None
        self.miniatura = None
        self.duracion = None
        self.peso = None

class streamL(video):
    def __init__(self):
        self.flujo = None
        self.name = None

class stream(video):
    def __init__(self, url, formato):
        self.video = pafy.new(url)
        self.flujo = self.video.getbest("mp4" if (formato == "best") else formato)
        if not self.flujo:
            self.flujo = self.video.getbest()
        self.conect()

    def conect(self):
        self.titulo = self.video.title
        self.categoria = self.video.category
        self.miniatura = miniatura(self.video.thumb)
        self.duracion = self.video.duration
        self.peso = video_peso(self.flujo.get_filesize())

class listStream(object):
    def __init__(self, url, formato):
        self.video = pafy.get_playlist(url)
        self.lista = []
        self.list_title = self.video["title"]
        self.formato = "mp4" if (formato == "best") else formato
        self.conect()

    def conect(self):
        for i in range(len(self.video["items"])):
            new_video = streamL()

            new_video.flujo = self.video["items"][i]["pafy"].getbest(self.formato)
            if not new_video.flujo:
                new_video.flujo = self.video["items"][i]["pafy"].getbest()
            new_video.name = "{0:0>2} - {1}".format(i+1, new_video.flujo.filename)
            new_video.titulo = self.video["items"][i]["pafy"].title
            new_video.categoria = self.video["items"][i]["pafy"].category
            new_video.miniatura = miniatura(self.video["items"][i]["pafy"].thumb)
            new_video.duracion = self.video["items"][i]["pafy"].duration
            new_video.peso = video_peso(new_video.flujo.get_filesize())

            self.lista.append(new_video)
            print(new_video.titulo)

    def get_list_stream(self):
        return self.lista
