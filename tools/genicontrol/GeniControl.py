﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2012 by Christoph Schueler <github.com/Christoph2,
##                                      cpu12.gems@googlemail.com>
##
##  All Rights Reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##

import wx
import genicontrol.dataitems as dataitems
#import genicontrol.view
from genicontrol.view.mcpanel import MCPanel
from genicontrol.view.refpanel import RefPanel
from genicontrol.model.NullModel import NullModel
from genicontrol.model.config import DataitemConfiguration
from genicontrol.controller.GUIController import GUIController
import genicontrol.controlids as controlids
from genicontrol.configuration import Config as Config
from genicontrol.view.GridControl import GridControl

TR = wx.GetTranslation

CONTROL_MODE_AUTOMATIC              = 0
CONTROL_MODE_CONSTANT_PRESSURE      = 1
CONTROL_MODE_PROPORTIONAL_PRESSURE  = 2
CONTROL_MODE_CONSTANT_FREQUENCY     = 3

import led

class TabPanel(wx.Panel):
    def __init__(self, parent):
        """"""

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)

        self.SetSizer(sizer)

class InfoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer = self.addValues(DataitemConfiguration['StringValues'])
        grid = GridControl(self, DataitemConfiguration['InfoValues'], dataitems.DATAITEMS)
        sizer.Add(grid, 1, wx.ALL, 5)
        self.SetSizer(sizer)

    def addValues(self, values):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for datapoint, displayName,idCode in values:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            st = wx.StaticText(self, label = displayName)
            hsizer.Add(st, 1, wx.ALL, 5)
            tc = wx.TextCtrl(self, idCode, "n/a", style = wx.ALIGN_RIGHT)
            tc.Enable(False)
            hsizer.Add(tc, 1, wx.ALL, 5)
            sizer.Add(hsizer) # , 1, wx.ALL, 5)
        return sizer

    def setValue(self, controlID, value):
        control = self.GetWindowById(controlID)
        control.SetValue(value)

class TestNB(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size = (21, 21), style = wx.BK_DEFAULT | wx.BK_BOTTOM)
        tabOne = TabPanel(self)
        self.AddPage(MCPanel(self), "Measurement + Control")
        self.AddPage(tabOne, "Busmonitor")
        self.AddPage(RefPanel(self), "References")
        self.AddPage(tabOne, "Parameters")
        self.AddPage(InfoPanel(self), "Info")


class GBFrame(wx.Frame):
    def __init__(self, parent, size = None, pos = None):
        wx.Frame.__init__(self, parent, -1, "GeniControl", size = size, pos = pos)
        self.initStatusBar()
        self.createMenuBar()
        self.locale = None
        #self.updateLanguage(wx.LANGUAGE_ITALIAN)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

##
##        self.log = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
##        if wx.Platform == "__WXMAC__":
##            self.log.MacCheckSpelling(False)
##

        # Set the wxWindows log target to be this textctrl
        #wx.Log_SetActiveTarget(wx.LogTextCtrl(self.log))

        # for serious debugging
        wx.Log_SetActiveTarget(wx.LogStderr())
        #wx.Log_SetTraceMask(wx.TraceMessages

        self.notebook = TestNB(self, wx.NewId())
        if not pos:
            self.Center()
        wx.LogMessage("Started...")

    def updateLanguage(self, lang):
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(lang)
        if self.locale.IsOk():
            self.locale.AddCatalog('wxpydemo')
        else:
            self.locale = None

    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def menuData(self):
        return [(TR("&File"), (
                    ("&Save snapshot", "Save current measurement values to a file.", self.onSaveSnapShot),
                    ("Save &parameter", "", self.onSaveParameter),
                    ("Save &info", "Save parameter scaling information to a file.", self.onSaveInfo),
                    ("&Load paramter", "", self.onLoadParamter),
                    ("", "", ""),
                    ("&Exit", "Exit GeniControl", self.OnCloseWindow)))

                ]

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler,
                       kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

    def onSaveSnapShot(self, event): pass
    def onSaveParameter(self, event): pass
    def onSaveInfo(self, event): pass
    def onLoadParamter(self, event): pass

    def OnCloseWindow(self, event):
        wx.LogMessage("Exiting...")
        wx.LogMessage("%s %s" % (self.GetSize(), self.GetPosition()))
        self.saveConfiguration()
        self.Destroy()

    def saveConfiguration(self):
        size = self.Size
        pos = self.Position
        config = Config()
        config.posX = pos.x
        config.posY = pos.y
        config.sizeX = size.x
        config.sizeY = size.y


class GeniControlApp(wx.PySimpleApp):
    def __init__(self):
        super(GeniControlApp, self).__init__()

def main():
    config = Config()
    config.loadConfiguration()
    size = wx.Size(config.sizeX, config.sizeY)
    app = GeniControlApp()
    frame = GBFrame(None, size)

    controller = GUIController(NullModel, frame)

    frame.Show(True)
    app.MainLoop()
    config.saveConfiguration()

if __name__ == '__main__':
    main()

