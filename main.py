import wx
import numpy as np
import colorsys

from pynput.mouse import Controller

mouse = Controller()

class RotatingWindow(wx.Frame):
    def __init__(self, theta, radius, initial_color):
        super().__init__(None, -1, '魔法陣', size=(30, 30), style=wx.NO_BORDER | wx.FRAME_SHAPED)

        self.theta = theta
        self.radius = radius/4
        self.color = initial_color

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(3)  # 100msごとに更新

        self.Show()

    def on_timer(self, event):
        # 角度を更新
        self.theta += 0.01

        # 新しい位置を計算
        x = np.cos(self.theta) * self.radius + mouse.position[0] + self.radius + 7
        y = np.sin(self.theta) * self.radius + mouse.position[1] + self.radius + 4

        # ウィンドウの位置を更新
        self.SetPosition((int(x), int(y)))

        # 色を更新
        self.color = (self.color + 0.01) % 1
        r, g, b = colorsys.hsv_to_rgb(self.color, 1, 1)
        self.SetBackgroundColour(wx.Colour(int(r*255), int(g*255), int(b*255)))
        self.ClearBackground()

app = wx.App(False)

# 角度の範囲を設定します（0から2πまで）
theta = np.linspace(0, 2*np.pi, 80)

# 各角度に対してウィンドウを作成します
for i, t in enumerate(theta):
    initial_color = i / len(theta)
    RotatingWindow(t, 200, initial_color)

app.MainLoop()