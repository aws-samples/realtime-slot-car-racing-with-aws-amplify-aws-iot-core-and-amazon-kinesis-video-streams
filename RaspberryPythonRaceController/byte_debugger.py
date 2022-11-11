import wx
import json
from utils.byte_helper import ByteHelper, ByteArrayHelper

class Example(wx.Frame):
    sample_array_send = "[255, 255, 255, 255, 255, 255, 255, 219, 43]"
    sample_array_receive = "[255, 255, 255, 255, 255, 255, 255, 24, 248, 0, 0, 0, 0, 0, 108]"

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title)
        self.sending = True
        self.InitUI()
        self.Centre()
        self.changed_array = False

    def InitUI(self):

        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)

        font.SetPointSize(12)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Byte array')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel)
        tc.SetValue(self.sample_array_send)
        self.tc = tc
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT |
                 wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, label='Byte array to race track (9 bytes)')
        cb1.SetFont(font)
        self.cb1 = cb1
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, label='Byte array from race track (15 bytes)')
        cb2.SetFont(font)
        hbox4.Add(cb2, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)
        cb1.SetValue(True)
        cb2.SetValue(False)
        cb1.Bind(wx.EVT_CHECKBOX,
                 lambda event: self.on_press_option_checkbox(event, cb1, cb2))
        cb2.Bind(wx.EVT_CHECKBOX,
                 lambda event: self.on_press_option_checkbox(event, cb2, cb1))

        vbox.Add((-1, 10))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        my_btn = wx.Button(panel, label='Array => Object')
        my_btn.Bind(wx.EVT_BUTTON, lambda event: self.on_press(event, to_object=True, to_array=False))
        my_btn2 = wx.Button(panel, label='Object => Array')
        my_btn2.Bind(wx.EVT_BUTTON, lambda event: self.on_press(event, to_object=False, to_array=True))
        hbox5.Add(my_btn, flag=wx.LEFT, border=10)
        hbox5.Add(my_btn2, flag=wx.LEFT, border=10)
        vbox.Add(hbox5, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 25))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Output object')
        st2.SetFont(font)
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.tc2 = tc2
        hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                 border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)

    def on_press(self, _, to_object=False, to_array=False):
        if to_object and self.sending:
            int_array_input = self.tc.GetValue()
            int_array = json.loads(int_array_input)
            value = self.debug_sending_int_arr_to_object(int_array)
            self.tc2.SetValue(value)
        if to_object and not self.sending:
            int_array_input = self.tc.GetValue()
            int_array = json.loads(int_array_input)
            value = self.debug_receiving_int_arr_to_object(int_array)
            self.tc2.SetValue(value)
        if to_array:
            self.tc.SetValue("Bla21")

    def on_press_option_checkbox(self, _, cb1, cb2):
        cb2.SetValue(not cb1.GetValue())
        self.sending = self.cb1.GetValue()
        self.set_sample_byte_array(self.tc)

    def set_sample_byte_array(self, text_box):
        if self.changed_array:
            return
        if self.sending:
            text_box.SetValue(self.sample_array_send)
        else:
            text_box.SetValue(self.sample_array_receive)

    def debug_sending_int_arr_to_object(self, int_array):
        return json.dumps(ByteArrayHelper.sending_array_of_ints_to_object(int_array), indent=4)

    def debug_receiving_int_arr_to_object(self, int_array):
        return json.dumps(ByteArrayHelper.race_track_array_of_ints_to_object(int_array), indent=4)

def main():

    app = wx.App()
    ex = Example(None, title='Race track byte array debugger')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
