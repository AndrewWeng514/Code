import wx
import time
from ppadb.client import Client as AdbClient


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)


        # 创建状态栏
        self.status_bar = self.CreateStatusBar(2)  # 创建一个有两个字段的状态栏

        # 创建菜单栏
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        get_devices_item = file_menu.Append(wx.ID_ANY, "获取设备信息")
        menu_bar.Append(file_menu, "&文件")
        self.SetMenuBar(menu_bar)

        # 绑定菜单项点击事件
        self.Bind(wx.EVT_MENU, self.on_get_devices, get_devices_item)

        # 创建一个面板
        panel = wx.Panel(self)

        # 创建一个选择框
        self.choice = wx.Choice(panel, pos=(20, 20))
        self.choice.Bind(wx.EVT_CHOICE, self.on_choice)

        # 创建一个文本框来显示设备信息
        self.device_info_text = wx.TextCtrl(panel, pos=(20, 60), size=(760, 500),
                                            style=wx.TE_MULTILINE | wx.TE_READONLY)

        # 创建一个定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)

        # 启动定时器，设置间隔为1000毫秒（1秒）
        self.timer.Start(1000)

        # 设置窗口属性
        self.SetTitle("状态栏实时显示当前日期和时间及设备号")
        self.SetSize((800, 600))  # 设置窗口大小为800x600
        self.Centre()

        # 初始化ADB客户端
        self.client = AdbClient(host="127.0.0.1", port=5037)

        # 初始化设备列表
        self.update_devices()

    def update_time(self, event):
        # 获取当前日期和时间
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 更新状态栏显示
        self.status_bar.SetStatusText(current_time, 0)  # 更新第一个字段为当前时间

    def update_devices(self):
        # 获取当前连接的设备列表
        devices = self.client.devices()
        device_list = [device.serial for device in devices]

        # 更新选择框选项
        self.choice.Clear()
        self.choice.AppendItems(device_list)

        # 更新状态栏显示
        if device_list:
            self.status_bar.SetStatusText("连接的设备: " + ", ".join(device_list), 1)
        else:
            self.status_bar.SetStatusText("没有连接的设备", 1)

    def on_get_devices(self, event):
        # 获取当前连接的设备列表
        devices = self.client.devices()
        print(adb.)
        device_info = "\n".join([f"设备序列号: {device.serial}\n设备状态: {device.state}" for device in devices])

        # 更新文本框显示设备信息
        self.device_info_text.SetValue(device_info)

    def on_choice(self, event):
        # 获取选择的设备
        selected_device = self.choice.GetStringSelection()
        self.status_bar.SetStatusText("当前选择的设备: " + selected_device, 1)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show(True)
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
