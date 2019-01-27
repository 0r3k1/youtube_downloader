#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx, time, threading, os, yt, webbrowser
import wx.adv
from wx.lib.scrolledpanel import ScrolledPanel
from utilidades import children, _opt, exist_dir, back_dir, get_query
from option import optionFrame
from sqlite_3 import sqlite_3
from panel import panel

myEVT_STREAM = wx.NewEventType()
EVT_STREAM = wx.PyEventBinder(myEVT_STREAM, 1)

class threadEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid, value=None):
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        return self._value

class streamThread(threading.Thread):
    def __init__(self, parent, value, opt):
        threading.Thread.__init__(self)
        self._parent = parent
        self._value = value
        self.opt = opt

    def run(self):
        if "playlist?list=" in self._value:
            streamL = yt.listStream(self._value, self.opt.lista_formato)
            stream = streamL.get_list_stream()

            if self.opt.lista_carpeta == 1:
                path = os.path.join(self.opt.lista_directorio, streamL.list_title)
                if not self.opt.lista_directorio == path:
                    exist_dir(path)

                    sqlite = sqlite_3()
                    self.opt.lista_directorio = path
                    sqlite.insert(get_query(self.opt))
                    sqlite.close()
        else:
            stream = yt.stream(self._value, self.opt.video_formato)

        evt = threadEvent(myEVT_STREAM, -1, stream)
        wx.PostEvent(self._parent, evt)

class PopupMenu(wx.Menu):
    def __init__(self, parent):
        super(PopupMenu, self).__init__()
        self.parent = parent

        newItem = wx.MenuItem(self, wx.ID_ANY, "Pegar Link")
        miniItem = wx.MenuItem(self, wx.ID_ANY, "Minimizar")
        closeItem = wx.MenuItem(self, wx.ID_ANY, "Cerrar")

        self.Append(newItem)
        self.Append(miniItem)
        self.Append(closeItem)

        self.Bind(wx.EVT_MENU, self.onMinimize, miniItem)
        self.Bind(wx.EVT_MENU, self.onClose, closeItem)
        self.Bind(wx.EVT_MENU, self.onNew, newItem)

    def onMinimize(self, event):
        self.parent.Iconize()

    def onClose(self, event):
        self.parent.Close()

    def onNew(self, event):
        self.parent.onworker(event)

class myScrolledPanel(ScrolledPanel):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, dir=wx.VSCROLL):
        ScrolledPanel.__init__(self, parent, id, pos, size, dir)
        self.SetScrollRate(5,5)
        self.SetScrollbar(wx.VERTICAL, 0, 20, 50)
        self.parent = parent
        self.mainsz = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainsz)

        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)

    def onRightDown(self, event):
        self.PopupMenu(PopupMenu(self.parent), event.GetPosition())

class Frame(wx.Frame):
    def __init__(self, parent, id=-1, title='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name="frame"):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
        self.SetIcon(wx.Icon(wx.IconLocation("img/logo.ico")))
        self.id = 0
        self.espera = 0
        self.peticiones = 0
        self.state = False
        self.pendiente = False
        self.opt = _opt()

        self.Bind(EVT_STREAM, self.onAdd)

        self.initUI()
        self.berificar_opciones()

        self.Centre(wx.BOTH)
        self.Show()

    def initUI(self):
        self.SetBackgroundColour((241, 240, 226))
        self.menuBar()
        self.toolBar()

        self.statusbar = self.CreateStatusBar(2)

        self.statusbar_update()

        self.scroller = myScrolledPanel(self)

    def statusbar_update(self):
        self.statusbar.SetStatusText("conexiones en espera: {0}".format(self.peticiones), 0)
        self.statusbar.SetStatusText("videos en progreso: {0}".format(self.espera), 1)

    def toolBar(self):
        toolbar = self.CreateToolBar()
        toolbar.SetToolBitmapSize((40, 40))
        toolbar.SetBackgroundColour((109, 144, 156))

        ntool = toolbar.AddTool(wx.ID_ANY, "Pegar Link", wx.Bitmap("iconos/pastex40.png"))
        otool = toolbar.AddTool(wx.ID_ANY, "Opciones", wx.Bitmap("iconos/toolx40.png"))
        htool = toolbar.AddTool(wx.ID_ANY, "Ayuda", wx.Bitmap("iconos/helpx40.png"))
        ctool = toolbar.AddTool(wx.ID_ANY, "Limpiar", wx.Bitmap("iconos/cleanx40.png"))
        dtool = toolbar.AddTool(wx.ID_ANY, "Donacion", wx.Bitmap("iconos/donax40.png"))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.onworker, ntool)
        self.Bind(wx.EVT_TOOL, self.options, otool)
        self.Bind(wx.EVT_TOOL, self.clean, ctool)
        self.Bind(wx.EVT_TOOL, self.donacion, dtool)
        self.Bind(wx.EVT_TOOL, self.help, htool)

    def menuBar(self):
        menu_bar = wx.MenuBar()

        fileMenu = wx.Menu()
        toolMenu = wx.Menu()
        helpMenu = wx.Menu()

        newItem = wx.MenuItem(fileMenu, wx.ID_ANY, "&Pegar Link\tCTRL+N")
        exitItem = wx.MenuItem(fileMenu, wx.ID_ANY, "&Salir\tCTRL+Q")

        newItem.SetBitmap(wx.Bitmap("iconos/newl.png"))
        exitItem.SetBitmap(wx.Bitmap("iconos/quit.png"))

        fileMenu.Append(newItem)
        fileMenu.AppendSeparator()
        fileMenu.Append(exitItem)

        prefItem = wx.MenuItem(toolMenu, wx.ID_ANY, "&Opciones\tCTRL+O")

        prefItem.SetBitmap(wx.Bitmap("iconos/pref.png"))

        toolMenu.Append(prefItem)

        helpItem = wx.MenuItem(helpMenu, wx.ID_ANY, "&Ayuda\tCTRL+H")
        aboutItem = wx.MenuItem(helpMenu, wx.ID_ANY, "&About\CTRL+A")

        helpItem.SetBitmap(wx.Bitmap("iconos/help.png"))
        aboutItem.SetBitmap(wx.Bitmap("iconos/about.png"))

        helpMenu.Append(helpItem)

        menu_bar.Append(fileMenu, "&Archivo")
        menu_bar.Append(toolMenu, "&Herramientas")
        menu_bar.Append(helpMenu, "&Ayuda")
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.onQuit, id=exitItem.GetId())
        self.Bind(wx.EVT_MENU, self.onworker, id=newItem.GetId())
        self.Bind(wx.EVT_MENU, self.options, id=prefItem.GetId())
        self.Bind(wx.EVT_MENU, self.help, id=helpItem.GetId())

    def onQuit(self, event):
        self.Close()

    def onworker(self, event):
        if not wx.TheClipboard.IsOpened():
            do = wx.TextDataObject()
            wx.TheClipboard.Open()
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()
            if success:
                url = do.GetText()
                if "www.youtube.com" in url:
                    self.peticiones += 1
                    self.statusbar_update()
                    worker = streamThread(self, url, self.opt)
                    worker.start()

    def crear_nodo(self, stream, path):
        nodo = panel(self.scroller, self.id, stream, path)
        self.scroller.mainsz.Add(nodo, 0, wx.ALL|wx.EXPAND, 2)
        self.scroller.SetupScrolling(scroll_x=True, scroll_y=True)
        self.id += 1
        self.espera += 1
        self.statusbar_update()

    def onAdd(self, event):
        self.peticiones -= 1
        self.statusbar_update()
        stream = event.GetValue()
        if isinstance(stream, yt.stream):
            path = self.opt.video_directorio
            exist_dir(path)
            if stream.categoria == "Music":
                if self.musica(stream.titulo):
                    stream.flujo = stream.video.getbestaudio(self.opt.musica_formato)
                    if not stream.flujo:
                        stream.flujo = stream.video.getbestaudio()
                    path = self.opt.musica_directorio
                    exist_dir(path)
            self.crear_nodo(stream, path)
        elif isinstance(stream, list):
            sqlite = sqlite_3()
            self.opt = sqlite.get_values()
            list_musica = False
            path = self.opt.lista_directorio
            exist_dir(path)
            for streamN in stream:
                if (list_musica and streamN.categoria == "Music") or streamN.categoria == "Music":
                    if self.musica(streamN.titulo):
                        streamN.flujo = streamN.video.getbestaudio(self.opt.musica_formato)
                        if not streamN.flujo:
                            streamN.flujo = streamN.video.getbestaudio()
                        path = self.opt.musica_directorio
                        exist_dir(path)
                    list_musica = self.lista_musica()
                self.crear_nodo(streamN, path)
            self.statusbar_update()
            self.opt.lista_directorio = back_dir(path)
            sqlite.insert(get_query(self.opt))

        hilo = threading.Thread(target=self.descargar)
        hilo.start()

    def descargar(self):
        if not self.state:
            self.state = True

            children = self.scroller.mainsz.GetChildren()

            for child in children:
                widget = child.GetWindow()
                if isinstance(widget, panel):
                    if not widget.state:
                        widget.descargar(self.opt.lista_enumera)
                        widget.state = True
                        self.espera -= 1
                        self.statusbar_update()

            self.state = False
            if self.pendiente:
                self.pendiente = False
                self.descargar()
        else:
            self.pendiente = True

    def berificar_opciones(self):
        sqlite = sqlite_3()
        if sqlite.exist:
            path = os.path.join(os.path.expandvars("%userprofile%"),"Downloads")
            sqlite.insert("0, 'best', '{0}', 'best', '{1}', 'best', '{2}', 1, 1".format(path, path, path))
        self.opt = sqlite.get_values()

    def options(self, event):
        op = optionFrame(self)
        op.Destroy()
        self.get_opt()

    def clean(self, event):
        children = self.scroller.mainsz.GetChildren()

        for child in children:
            widget = child.GetWindow()
            if isinstance(widget, panel):
                if widget.state:
                    widget.Destroy()
        self.scroller.SetupScrolling(scroll_x=True, scroll_y=True)

    def aboutBox(self, event):
        descripcion = """
        """

    def donacion(self, event):
        webbrowser.open("https://www.paypal.com/donate/?token=UcL22xOQ0VkvZ0uM844o2j_c7mwiNrpeTX_cvsfQRV4n0-jtM72hMidL_okrQC_jX69qmW&country.x=ES&locale.x=ES")

    def help(self, event):
        descripcion = """Full Video Downloader en una app que te ayuda a descargar tus
        videos y musica favorita de youtube, con Full Video Doenloader no solo podras descargar
        videos sino listas de reproduccion completas y sin restrinciones.
        """

        licence = """Full Video Downloader es  free software; puede redistribuirlo y / o modificarlo
        bajo los términos de la Licencia wxWindows Library Licencese.
        url: https://www.wxwidgets.org/about/licence/
        """

        info = wx.adv.AboutDialogInfo()
        info.SetIcon(wx.Icon('img/logo.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Full Video Downloader')
        info.SetVersion('1.0')
        info.SetDescription(descripcion)
        info.SetCopyright('(C) 2018 Cristobal Rodas')
        info.SetLicence(licence)
        info.AddDeveloper('Cristobal Rodas')
        info.AddDocWriter('Cristobal Rodas')
        info.AddArtist('The oreki crew')

        wx.adv.AboutBox(info)


    def musica(self, title):
        return wx.MessageBox("Se a detectado que el video puede ser una cancion\ndesea descargarlo como musica??",
        title, wx.YES_NO|wx.CENTRE) == 2

    def lista_musica(self):
        return wx.MessageBox("desea que toda la lista de reproduccion se descargada como musica??",
        "lista de reproduccion", wx.YES_NO|wx.CENTRE) == 2

    def get_opt(self):
        sqlite = sqlite_3()
        self.opt = sqlite.get_values()


def main():
    app = wx.App()
    frame = Frame(None, title="Youtube Dowloader")
    app.MainLoop()

if __name__ == "__main__":
    main()
