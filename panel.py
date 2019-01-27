#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx, os, yt
from utilidades import rename

class PopupMenu(wx.Menu):
    def __init__(self, parent):
        super(PopupMenu, self).__init__()
        self.parent = parent

        eItem = wx.MenuItem(self, wx.ID_ANY, "Eliminar")
        aItem = wx.MenuItem(self, wx.ID_ANY, "Abrir ubicacion")
        rItem = wx.MenuItem(self, wx.ID_ANY, "Reproducir")

        self.Append(eItem)
        self.Append(aItem)
        self.Append(rItem)

        self.Bind(wx.EVT_MENU, self.onDel, eItem)
        self.Bind(wx.EVT_MENU, self.onOpen, aItem)
        self.Bind(wx.EVT_MENU, self.onPlay, rItem)

    def onDel(self, event):
        self.parent.Destroy()
        self.parent.update_croller()

    def onOpen(self, event):
        os.startfile(self.parent.path)

    def onPlay(self, event):
        os.startfile(os.path.join(self.parent.path, "{0}.{1}".format(self.parent.stream.titulo, self.parent.stream.flujo.extension)))

class panel(wx.Panel):
    def __init__(self, parent, id, stream, path):
        wx.Frame.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER)
                #__init__(self, parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=TAB_TRAVERSAL, name=PanelNameStr)
        self.id = id
        self.state = False
        self.stream = stream
        self.path = path
        self.parent = parent
        self.SetBackgroundColour((109, 144, 156))

        Image = wx.Bitmap(wx.Image(stream.miniatura))
        txt_descripcion = "Tipo: {0}  Size: {1}  Duracion: {2}".format(stream.categoria, stream.peso, stream.duracion)
        titulo = stream.titulo

        if len(titulo) > 35:
            titulo = "{0}...".format(titulo[0:32])

        self.mainsz = wx.BoxSizer(wx.HORIZONTAL)
        self.container = wx.BoxSizer(wx.VERTICAL)

        self.mini = wx.StaticBitmap(self, wx.ID_ANY, Image, wx.DefaultPosition, wx.DefaultSize, 0)
        self.mainsz.Add(self.mini, 0, wx.ALL, 10)

        self.titulo = wx.StaticText(self, wx.ID_ANY, titulo, wx.DefaultPosition, wx.DefaultSize, 0)
        self.titulo.Wrap(-1)
        self.container.Add(self.titulo, 0, wx.ALL|wx.EXPAND, 5)

        self.progres_bar = wx.Gauge(self, wx.ID_ANY, stream.flujo.get_filesize(), wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.progres_bar.SetValue(0)
        self.container.Add(self.progres_bar, 0, wx.ALL|wx.EXPAND, 5)

        self.descarga = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.descarga.Wrap(-1)
        self.container.Add(self.descarga, 0, wx.ALL|wx.EXPAND, 5)

        self.descripcion = wx.StaticText(self, wx.ID_ANY, txt_descripcion, wx.DefaultPosition, wx.DefaultSize, 0)
        self.descripcion.Wrap(-1)
        self.container.Add(self.descripcion, 0, wx.ALL|wx.EXPAND, 5)

        self.mainsz.Add(self.container, 0, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(self.mainsz)

        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.mini.Bind(wx.EVT_RIGHT_UP, self.onclick)
        self.titulo.Bind(wx.EVT_RIGHT_UP, self.onclick)
        self.progres_bar.Bind(wx.EVT_RIGHT_UP, self.onclick)
        self.descarga.Bind(wx.EVT_RIGHT_UP, self.onclick)
        self.descripcion.Bind(wx.EVT_RIGHT_UP, self.onclick)

    def get_children_item(self, item):
        children = self.container.GetChildren()
        hijos = []

        for child in children:
            widget = child.GetWindow()
            if isinstance(widget, item):
                hijos.append(widget)

        return hijos

    def callback(self, total, recvd, ratio, rate, eta):
        t = yt.video_peso(total)
        r = yt.video_peso(recvd)

        gauge = self.get_children_item(wx.Gauge)
        gauge[0].SetValue(recvd)

        progress = self.get_children_item(wx.StaticText)
        progress[1].SetLabel(u"{0} de {1} / Tiempo restante: [{2}/sec]".format(r, t, round(eta)))

    def descargar(self, lista):
        self.SetBackgroundColour((51, 153, 255))
        self.Refresh()
        self.stream.flujo.download(filepath=self.path, quiet=True, callback=self.callback, meta=True)
        self.SetBackgroundColour((109, 144, 156))
        self.Refresh()

        try:
            if lista and self.stream.name:
                rename(self.path, self.stream.flujo.filename, self.stream.name)
        except:
            pass

    def onRightDown(self, event):
        if self.state:
            self.PopupMenu(PopupMenu(self), event.GetPosition())

    def onclick(self, event):
        self.onRightDown(event)

    def update_croller(self):
        self.parent.SetupScrolling(scroll_x=True, scroll_y=True)
