#!/usr/bin/env python
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

import datetime
import logging
import wx
from wx.lib.scrolledpanel import ScrolledPanel
import genicontrol.dataitems as dataitems
import genicontrol.controlids as controlids
from genicontrol.model.config import DataitemConfiguration
from genicontrol.view.GridControl import GridControl


class InfoPanel(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer = self.addValues(DataitemConfiguration['StringValues'])
        self.grid = GridControl(self, DataitemConfiguration['InfoValues'], dataitems.DATAITEMS)
        sizer.Add(self.grid, 1, wx.ALL, 5)
        self.SetSizerAndFit(sizer)
        ctl = self.FindWindowById(controlids.ID_STR_PRODUCT_NAME)
        ctl.SetValue('GeniBus Simulation')
        ctl = self.FindWindowById(controlids.ID_STR_SOFTWARE_NAME1)
        ctl.SetValue('GeniControl')
        ctl = self.FindWindowById(controlids.ID_STR_COMPILE_DATE1)
        ctl.SetValue('%s' % str(datetime.date.today()))
        ctl = self.FindWindowById(controlids.ID_STR_PROTOCOL_CODE)
        ctl.SetValue('GB')
        ctl = self.FindWindowById(controlids.ID_STR_DEVELOPERS)
        ctl.SetValue('CS')
        ctl = self.FindWindowById(controlids.ID_STR_SERIAL_NO)
        ctl.SetValue('RT')
        self.SetupScrolling()

    def addValues(self, values):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for datapoint, displayName,idCode in values:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            st = wx.StaticText(self, label = displayName)
            hsizer.Add(st, 1, wx.ALL, 5)
            tc = wx.TextCtrl(self, idCode, "n/a", style = wx.ALIGN_LEFT)
            tc.Enable(False)
            hsizer.Add(tc, 1, wx.ALL, 5)
            sizer.Add(hsizer) # , 1, wx.ALL, 5)
        return sizer

    def setValue(self, controlID, value):
        control = self.GetWindowById(controlID)
        control.SetValue(value)


    def setItem(self, item, physEntity, factor, unit, zero, _range):
        self.grid.setItem(item, physEntity, factor, unit, zero, _range)

