#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx, os
from utilidades import _opt
from sqlite_3 import sqlite_3

class optionFrame(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"Opciones", pos=wx.DefaultPosition, size=wx.Size(500,510), style=wx.DEFAULT_DIALOG_STYLE)
        self.parent = parent
        self.list_video_format = ["best"  ,"mp4", "webm", "flv", "3gp"]
        self.list_music_format = ["best"  ,"web", "ogg", "m4a"]

        self.initUi()
        self.set_param()

        self.Centre(wx.BOTH)
        self.ShowModal()

    def initUi(self):
        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER)
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Video", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )

        bSizer51 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText51 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Formato", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText51.Wrap( -1 )
        bSizer51.Add( self.m_staticText51, 0, wx.ALL, 5 )

        self.video_formato = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.list_video_format, 0 )
        self.video_formato.SetSelection( 0 )
        bSizer51.Add( self.video_formato, 1, wx.ALL, 5 )


        bSizer2.Add( bSizer51, 1, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Directorio", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        bSizer6.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.video_directorio = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.video_directorio, 1, wx.ALL, 5 )

        self.video_examinar = wx.Button( self.m_panel2, wx.ID_ANY, u"Examinar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.video_examinar, 0, wx.ALL, 5 )


        bSizer2.Add( bSizer6, 1, wx.EXPAND, 5 )


        self.m_panel2.SetSizer( bSizer2 )
        self.m_panel2.Layout()
        bSizer2.Fit( self.m_panel2 )
        bSizer1.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER )
        bSizer21 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText11 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Musica", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        bSizer21.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer52 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer21.Add( bSizer52, 1, wx.EXPAND, 5 )

        bSizer511 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText511 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Formato", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText511.Wrap( -1 )
        bSizer511.Add( self.m_staticText511, 0, wx.ALL, 5 )

        self.musica_formato = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.list_music_format, 0 )
        self.musica_formato.SetSelection( 0 )
        bSizer511.Add( self.musica_formato, 1, wx.ALL, 5 )


        bSizer21.Add( bSizer511, 1, wx.EXPAND, 5 )

        bSizer61 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText61 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Directorio", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText61.Wrap( -1 )
        bSizer61.Add( self.m_staticText61, 0, wx.ALL, 5 )

        self.musica_directorio = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.musica_directorio, 1, wx.ALL, 5 )

        self.musica_examinar = wx.Button( self.m_panel3, wx.ID_ANY, u"Examinar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.musica_examinar, 0, wx.ALL, 5 )


        bSizer21.Add( bSizer61, 1, wx.EXPAND, 5 )


        self.m_panel3.SetSizer( bSizer21 )
        self.m_panel3.Layout()
        bSizer21.Fit( self.m_panel3 )
        bSizer1.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )

        self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER )
        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText12 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Listas de Reproduccion", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        bSizer22.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer53 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer22.Add( bSizer53, 1, wx.EXPAND, 5 )

        bSizer512 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText512 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Formato", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText512.Wrap( -1 )
        bSizer512.Add( self.m_staticText512, 0, wx.ALL, 5 )

        self.lista_formato = wx.Choice( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.list_video_format, 0 )
        self.lista_formato.SetSelection( 0 )
        bSizer512.Add( self.lista_formato, 1, wx.ALL, 5 )


        bSizer22.Add( bSizer512, 1, wx.EXPAND, 5 )

        bSizer62 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText62 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Directorio", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )
        bSizer62.Add( self.m_staticText62, 0, wx.ALL, 5 )

        self.lista_directorio = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer62.Add( self.lista_directorio, 1, wx.ALL, 5 )

        self.lista_examinar = wx.Button( self.m_panel4, wx.ID_ANY, u"Examinar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer62.Add( self.lista_examinar, 0, wx.ALL, 5 )


        bSizer22.Add( bSizer62, 1, wx.EXPAND, 5 )

        bSizer5121 = wx.BoxSizer( wx.HORIZONTAL )

        self.lista_carpeta = wx.CheckBox( self.m_panel4, wx.ID_ANY, u"Crear carpeta para las listas de reproduccion", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5121.Add(self.lista_carpeta, 0, wx.ALL, 5)

        bSizer22.Add(bSizer5121, 1, wx.EXPAND, 5)

        bSizer789 = wx.BoxSizer( wx.HORIZONTAL )
        self.lista_enumera = wx.CheckBox( self.m_panel4, wx.ID_ANY, u"Enumerar los videos", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer789.Add(self.lista_enumera, 0, wx.ALL, 5)
        bSizer22.Add(bSizer789, 1, wx.EXPAND, 5)

        self.m_panel4.SetSizer(bSizer22)
        self.m_panel4.Layout()
        bSizer22.Fit(self.m_panel4)
        bSizer1.Add(self.m_panel4, 1, wx.EXPAND|wx.ALL, 5)

        bSizer85 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_acept = wx.Button( self, wx.ID_ANY, u"Aceptar", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_cancel = wx.Button( self, wx.ID_ANY, u"Cancelar", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer85.Add(self.btn_cancel, 0, wx.ALL, 5)
        bSizer85.Add(self.btn_acept, 0, wx.ALL, 5)

        bSizer1.Add(bSizer85, 0, wx.ALIGN_RIGHT, 5)


        self.SetSizer(bSizer1)
        self.Layout()

        self.video_examinar.Bind(wx.EVT_BUTTON, self.video_on_click)
        self.musica_examinar.Bind(wx.EVT_BUTTON, self.musica_on_click)
        self.lista_examinar.Bind(wx.EVT_BUTTON, self.lista_on_click)
        self.btn_acept.Bind(wx.EVT_BUTTON, self.aceptar)
        self.btn_cancel.Bind(wx.EVT_BUTTON, self.cancelar)

    def set_param(self):
        sqlite = sqlite_3()
        opt = sqlite.get_values()

        video_index = self.list_video_format.index(opt.video_formato)
        music_index = self.list_music_format.index(opt.musica_formato)
        list_index  = self.list_video_format.index(opt.lista_formato)

        self.video_formato.SetSelection(video_index)
        self.video_directorio.SetValue(opt.video_directorio)
        self.musica_formato.SetSelection(music_index)
        self.musica_directorio.SetValue(opt.musica_directorio)
        self.lista_formato.SetSelection(list_index)
        self.lista_directorio.SetValue(opt.lista_directorio)
        self.lista_carpeta.SetValue(True if (opt.lista_carpeta == 1) else False)
        self.lista_enumera.SetValue(True if (opt.lista_enumera == 1) else False)


    def __del__(self):
        pass

    def selec_dir(self):
        with wx.DirDialog(self, "Choose a directory:", style=wx.DD_CHANGE_DIR) as fileDialog:
            first_path = os.getcwd()
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            os.chdir(first_path)
            return fileDialog.GetPath()

    def video_on_click(self, event):
        self.video_directorio.SetValue(self.selec_dir())
        event.Skip()

    def musica_on_click(self, event):
        self.musica_directorio.SetValue(self.selec_dir())
        event.Skip()

    def lista_on_click(self, event):
        self.lista_directorio.SetValue(self.selec_dir())
        event.Skip()

    def aceptar(self, event):
        sqlite = sqlite_3()
        opt = _opt()

        opt.video_formato = self.video_formato.GetString(self.video_formato.GetSelection())
        opt.video_directorio = self.video_directorio.GetValue()
        opt.musica_formato = self.musica_formato.GetString(self.musica_formato.GetSelection())
        opt.musica_directorio = self.musica_directorio.GetValue()
        opt.lista_formato = self.lista_formato.GetString(self.lista_formato.GetSelection())
        opt.lista_directorio = self.lista_directorio.GetValue()
        opt.lista_carpeta = 1 if self.lista_carpeta.GetValue() else 0
        opt.lista_enumera = 1 if self.lista_enumera.GetValue() else 0

        sqlite.update(opt)

        self.Destroy()
        event.Skip()

    def cancelar(self, event):
        self.Destroy()
        event.Skip()
