import wx
from adb.client import Client as AdbClient


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        # 创建状态栏
        self.status_bar = self.CreateStatusBar()

        # 创建一个面板
        panel = wx.Panel(self)

        # 创建一个选择框
        self.choice = wx.Choice(panel, pos=(20, 20))
        self.choice.Bind(wx.EVT_CHOICE, self.on_choice)

        # 创建一个定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_devices, self.timer)

        # 启动定时器，设置间隔为5000毫秒（5秒）
        self.timer.Start(5000)

        # 设置窗口属性
        self.SetTitle("ADB设备连接状态")
        self.SetSize((400, 200))
        self.Centre()

        # 初始化ADB客户端
        self.client = AdbClient(host="127.0.0.1", port=5037)

        # 初始化设备列表
        self.update_devices(None)

    def update_devices(self, event):
        # 获取当前连接的设备列表
        devices = self.client.devices()
        device_list = [device.serial for device in devices]

        # 更新选择框选项
        self.choice.Clear()
        self.choice.AppendItems(device_list)

        # 更新状态栏显示
        if device_list:
            self.status_bar.SetStatusText("连接的设备: " + ", ".join(device_list))
        else:
            self.status_bar.SetStatusText("没有连接的设备")

    def on_choice(self, event):
        # 获取选择的设备
        selected_device = self.choice.GetStringSelection()
        self.status_bar.SetStatusText("当前选择的设备: " + selected_device)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
