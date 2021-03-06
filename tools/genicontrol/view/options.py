#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2014 by Christoph Schueler <github.com/Christoph2,
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
from wx.lib.masked import ipaddrctrl
from wx.lib.masked import TextCtrl
from genicontrol.serialport import serialAvailable
from genilib.gui.controls import createLabeledControl
from genilib.configuration import Config

ID_IPADDR       = wx.NewId()
ID_SUBNET       = wx.NewId()
ID_PORT         = wx.NewId()
ID_POLL         = wx.NewId()
ID_SERIAL_PORT  = wx.NewId()

ID_RB_TCPIP     = wx.NewId()
ID_RB_SERIAL    = wx.NewId()
ID_RB_SIM       = wx.NewId()

def fixIP(addr):
    return '.'.join(["%3s" % j for j in [i.strip() for i in addr.split('.')]])


class OptionsView(wx.Dialog):
    def __init__(self, parent, controller, model):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, u'Options')
        self.tcpControls = []
        self.serialControls = []
        self.simControls = []
        self.controller = controller
        self.model = model
        #self.model.registerObserver(self)

    def createControls(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        staticBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, " Driver " ), wx.VERTICAL )

        gridsizer = wx.FlexGridSizer(3 ,2)

        self.radioTcp = wx.RadioButton(self, ID_RB_TCPIP, " Arduino / TCP ", style = wx.RB_GROUP)
        gridsizer.Add(self.radioTcp, 1, wx.ALL, 5)

        gridsizer2 = wx.FlexGridSizer(3 ,2)
        self.addr = createLabeledControl(self, 'Server IP-address', ipaddrctrl.IpAddrCtrl(self, id = ID_IPADDR), gridsizer2, self.tcpControls)
        self.mask = createLabeledControl(self, 'Subnet-mask', ipaddrctrl.IpAddrCtrl(self, id = ID_SUBNET),gridsizer2, self.tcpControls )
        self.port = createLabeledControl(self, 'Server-port', TextCtrl(self, id = ID_PORT, mask = '#####'), gridsizer2, self.tcpControls)
        gridsizer.Add(gridsizer2, 1, wx.ALL | wx.ALIGN_TOP, 5)

        self.radioSerial = wx.RadioButton(self, ID_RB_SERIAL, " Serial Port ")
        gridsizer.Add(self.radioSerial, 1, wx.ALL, 5)

        boxSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.serialPort = createLabeledControl(self, 'Port', TextCtrl(self, id = ID_SERIAL_PORT), boxSizer2, self.serialControls)
        gridsizer.Add(boxSizer2, 1, wx.ALL, 5)

        self.radioSim = wx.RadioButton(self, ID_RB_SIM, " Simulator ")
        gridsizer.Add(self.radioSim, 1, wx.ALL, 5)
        st = wx.StaticText(self, label = '')
        gridsizer.Add(st, 1, wx.ALL, 5)

        staticBox.Add(gridsizer)
        sizer.Add(staticBox, 1, wx.ALL, 5)

        boxSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.poll = createLabeledControl(self, 'Polling interval', TextCtrl(self, id = ID_POLL, mask = '#####'), boxSizer3)
        sizer.Add(boxSizer3, flag=wx.ALL, border=5)

        self.logfile = wx.CheckBox(self, label='Write logfile')
        self.logfile.SetValue(False)
        sizer.Add(self.logfile, flag=wx.ALL, border=5)
  
        self.Bind(wx.EVT_CHECKBOX, self.SetLogWrite, self.logfile)

        line = wx.StaticLine(self, style = wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)
        btnsizer = wx.StdDialogButtonSizer()
        okButton = wx.Button(self, id = wx.ID_OK)
        okButton.SetDefault()
        btnsizer.Add(okButton)

        cancelButton = wx.Button(self, id = wx.ID_CANCEL)
        btnsizer.AddButton(cancelButton)

        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        if not serialAvailable:
            radioSerial.Enable(False)

        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, self.radioTcp)
        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, self.radioSerial)
        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, self.radioSim)

        self.SetSizerAndFit(sizer)

    def SetLogWrite(self, event):
        if self.logfile.GetValue():
            self.logfilewanted = '1'
        else:
            self.logfilewanted = '0'

    def setInitialValues(self):
        self.addr.SetValue(self.model.getServerIP())
        self.mask.SetValue(self.model.getSubnetMask())
        self.port.SetValue(self.model.getServerPort())
        self.poll.SetValue(self.model.getPollingInterval())
        self.logfile.SetValue(bool(self.model.getLogFileWanted()))
        self.serialPort.SetValue(self.model.getSerialPort())
        self.driver = self.model.getNetworkDriver()
        if self.driver == 0:
            value = 'Simulator'
            button = self.radioSim
        elif self.driver == 1:
            value = 'Arduino / TCP'
            button = self.radioTcp
        elif self.driver == 2:
            value = 'Serial'
            button = self.radioSerial
        button.SetValue(True)
        self.enableRadioButton(button.GetId())

    def show(self):
        self.Centre()
        return self.ShowModal()

    def onDriverSelected(self, event):
        self.enableRadioButton(event.GetId())

    def enableRadioButton(self, controlId):
        if controlId == ID_RB_TCPIP:
            self.enableTcpControls(True)
            self.enableSerialControls(False)
            self.enableSimControls(False)
            self.driver = 1
        elif controlId == ID_RB_SERIAL:
            self.enableTcpControls(False)
            self.enableSerialControls(True)
            self.enableSimControls(False)
            self.driver = 2
        elif controlId == ID_RB_SIM:
            self.enableTcpControls(False)
            self.enableSerialControls(False)
            self.enableSimControls(True)
            self.driver = 0

    def enableControls(self, controls, enable):
        for control in controls:
            control.Enable(enable)

    def enableTcpControls(self, enable):
        self.enableControls(self.tcpControls, enable)

    def enableSerialControls(self, enable):
        self.enableControls(self.serialControls, enable)

    def enableSimControls(self, enable):
        self.enableControls(self.simControls, enable)


class OptionsModel(object):

    def __init__(self):
        self.config = Config("GeniControl")

    def initialize(self):
        pass

    def load(self):
        self.config.load()
        self.driver = self.config.get('network', 'driver')
        self.serverIP = fixIP(self.config.get('network', 'serverip'))
        self.subnetMask = fixIP(self.config.get('network', 'subnetmask'))
        self.serverport = str(self.config.get('network', 'serverport'))
        self.pollinginterval = str(self.config.get('general', 'pollinginterval'))
        self.logfilewanted = self.config.get('general', 'logfilewanted')
        self.serialPort = self.config.get('serial', 'serialport')

    def save(self):
        pass

    def getNetworkDriver(self):
        return self.driver

    def getServerIP(self):
        return self.serverIP

    def getSubnetMask(self):
        return self.subnetMask

    def getServerPort(self):
        return self.serverport

    def getPollingInterval(self):
        return self.pollinginterval

    def getLogFileWanted(self):
        if self.logfilewanted == '1':
            return True
        else:
            return False

    def getSerialPort(self):
        return self.serialPort

    def setNetworkDriver(self, value):
        self.config.set('network', 'driver', value)

    def setServerIP(self, value):
        self.config.set('network', 'serverip', fixIP(value))

    def setSubnetMask(self, value):
        self.config.set('network', 'subnetmask', fixIP(value))

    def setServerPort(self, value):
        self.config.set('network', 'serverport',  value)

    def setPollingInterval(self, value):
        self.config.set('general', 'pollinginterval', value)

    def setLogFileWanted(self, value):
        if value:
            self.config.set('general', 'logfilewanted', '1')
        else:
            self.config.set('general', 'logfilewanted', '0')

    def setSerialPort(self, value):
        self.config.set('serial', 'serialport', value)


class OptionsController(object):

    def __init__(self, parent, model):
        self.model = model
        self.view = OptionsView(parent, self, model)
        self.model.initialize()
        self.model.load()
        self.view.createControls()
        self.view.setInitialValues()

    def execute(self):
        # Disable/Enable Controls.
        result = self.view.show()
        if result == wx.ID_OK:
            #self.model.save()
            self.model.setServerIP(self.view.addr.GetValue())
            self.model.setSubnetMask(self.view.mask.GetValue())
            self.model.setServerPort(self.view.port.GetValue())
            self.model.setPollingInterval(self.view.poll.GetValue())
            self.model.setLogFileWanted(self.view.logfile.GetValue())
            self.model.setNetworkDriver(self.view.driver)
            self.model.setSerialPort(self.view.serialPort.GetValue())

        else:
            pass
        self.view.Destroy()


def showOptionsDialogue(parent):
    model = OptionsModel()
    controller = OptionsController(parent, model)
    controller.execute()


def testDialog():
    showOptionsDialog(None)


def main():
    class TestApp(wx.PySimpleApp):
        def __init__(self):
            super(TestApp, self).__init__()

    app = TestApp()
    testDialog()

if __name__ == '__main__':
    main()

