# -*- coding: utf-8 -*-
import time
import wx
from ppadb.client import Client as AdbClient


APP_TITLE = u'性能工具'
APP_ICON = 'resource/1111.ico'


class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    id_open = wx.NewId()
    id_save = wx.NewId()
    id_quit = wx.NewId()
    id_help = wx.NewId()
    id_about = wx.NewId()

    def __init__(self, parent):
        '''构造函数'''

        wx.Frame.__init__(self, parent, -1, APP_TITLE)
        self.SetBackgroundColour(wx.Colour(224, 224, 224))
        self.SetSize((800, 600))
        self.Center()

        icon = wx.Icon(APP_ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.SetWindowStyle(wx.DEFAULT_FRAME_STYLE)

        self._CreateMenuBar()  # 菜单栏
        # self._CreateToolBar()  # 工具栏
        self._CreateStatusBar()  # 状态栏

    def _CreateMenuBar(self):
        '''创建菜单栏'''

        self.mb = wx.MenuBar()

        # 文件菜单
        m = wx.Menu()
        m.Append(self.id_open, u"获取当前设备信息")
        m.Append(self.id_save, u"获取当前文件路径")
        m.AppendSeparator()
        m.Append(self.id_quit, u"退出系统")
        self.mb.Append(m, u"工具")

        self.Bind(wx.EVT_MENU, self.OnOpen, id=self.id_open)
        self.Bind(wx.EVT_MENU, self.OnSave, id=self.id_save)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=self.id_quit)

        # 帮助菜单
        m = wx.Menu()
        m.Append(self.id_help, u"帮助主题")
        m.Append(self.id_about, u"关于...")
        self.mb.Append(m, u"帮助")

        self.Bind(wx.EVT_MENU, self.OnHelp, id=self.id_help)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=self.id_about)

        self.SetMenuBar(self.mb)

    def _CreateToolBar(self):
        '''创建工具栏'''

        bmp_open = wx.Bitmap('resource/cheese.ico', wx.BITMAP_TYPE_ANY)  # 请自备按钮图片
        bmp_save = wx.Bitmap('resource/cookedrice.ico', wx.BITMAP_TYPE_ANY)  # 请自备按钮图片
        bmp_help = wx.Bitmap('resource/hamburguer.ico', wx.BITMAP_TYPE_ANY)  # 请自备按钮图片
        bmp_about = wx.Bitmap('resource/pizza.ico', wx.BITMAP_TYPE_ANY)  # 请自备按钮图片

        self.tb = wx.ToolBar(self)
        self.tb.SetToolBitmapSize((16, 16))

        self.tb.AddLabelTool(self.id_open, u'打开文件', bmp_open, shortHelp=u'打开', longHelp=u'打开文件')
        self.tb.AddLabelTool(self.id_save, u'保存文件', bmp_save, shortHelp=u'保存', longHelp=u'保存文件')
        self.tb.AddSeparator()
        self.tb.AddLabelTool(self.id_help, u'帮助', bmp_help, shortHelp=u'帮助', longHelp=u'帮助')
        self.tb.AddLabelTool(self.id_about, u'关于', bmp_about, shortHelp=u'关于', longHelp=u'关于...')

        # self.Bind(wx.EVT_TOOL_RCLICKED, self.OnOpen, id=self.id_open)

        self.tb.Realize()

    def _CreateStatusBar(self):
        '''创建状态栏'''

        self.status_bar = self.CreateStatusBar(3)
        self.status_bar.SetStatusWidths([-1, -2, -1])
        self.status_bar.SetStatusStyles([wx.SB_RAISED, wx.SB_RAISED, wx.SB_RAISED])

        self.status_bar.SetStatusText("你好", 0)

        self.timer_time = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer_time)
        self.timer_time.Start(1000)
        # 创建一个定时器
        self.timer_device = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_devices, self.timer_device)

        # 启动定时器，设置间隔为5000毫秒（5秒）
        self.timer_device.Start(5000)
        # 初始化ADB客户端
        self.client = AdbClient(host="127.0.0.1", port=5037)

        # 初始化设备列表
        self.update_devices(None)
        self.Bind(wx.EVT_TIMER, self.update_devices, self.timer_device)



    def OnOpen(self, evt):
        '''打开文件'''

        self.status_bar.SetStatusText(u'打开文件', 1)

    def OnSave(self, evt):
        '''保存文件'''

        self.status_bar.SetStatusText(u'保存文件', 1)

    def OnQuit(self, evt):
        '''退出系统'''

        self.status_bar.SetStatusText(u'退出系统', 1)
        self.Destroy()

    def OnHelp(self, evt):
        '''帮助'''

        self.status_bar.SetStatusText(u'帮助', 1)

    def OnAbout(self, evt):
        '''关于'''

        self.status_bar.SetStatusText(u'关于', 1)
    def update_time(self, event):
        # 获取当前时间并更新显示
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.status_bar.SetStatusText(current_time,2)

    def update_devices(self, event):
        # 获取当前连接的设备列表
        devices = self.client.devices()
        device_list = [device.serial for device in devices]
        # 更新状态栏显示
        if device_list:
            self.status_bar.SetStatusText("连接的设备: " + ", ".join(device_list),1)
        else:
            self.status_bar.SetStatusText("没有连接的设备",1)



class mainApp(wx.App):
    def OnInit(self):
        self.SetAppName(APP_TITLE)
        self.Frame = mainFrame(None)
        self.Frame.Show()
        return True


if __name__ == "__main__":
    app = mainApp()
    app.MainLoop()
