"""
Main view for the application.
"""

import wx


class ViewFrameMain(wx.Frame):

    # Minimum screen resolution: 1366×768 / 1280x720 (still used on older laptops, anno 2026)
    _MIN_WINDOW_SIZE = (800, 700)

    def __init__(self, title):
        super().__init__(None, title=title)

        panel = wx.Panel(self)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_input_controls(panel), 2, wx.EXPAND | wx.ALL, 10)
        box.Add(self._create_start_button(panel), 0, wx.ALIGN_CENTER | wx.ALL, 10)
        box.Add(self._create_console(panel), 3, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(box)
        self.SetInitialSize(self._MIN_WINDOW_SIZE)


    def _create_input_controls(self, parent):
        lbl_work_order = wx.StaticText(parent, wx.ID_ANY, "Work order:")
        txt_work_order = wx.TextCtrl(parent, size=(200, -1))
        lbl_process = wx.StaticText(parent, wx.ID_ANY, "Process:")
        cmb_process = wx.ComboBox(parent, style=wx.CB_READONLY)
        lbl_serials = wx.StaticText(parent, wx.ID_ANY, "Serial numbers:")
        lst_serials = wx.ListCtrl(parent, style=wx.LC_REPORT)

        btn_load_wo = wx.Button(parent, wx.ID_ANY, "Load work order")
        btn_add_snr = wx.Button(parent, wx.ID_ANY, "Add serial number")
        btn_del_snr = wx.Button(parent, wx.ID_ANY, "Remove serial number")

        grid = wx.GridBagSizer(5, 5)
        grid.Add(btn_load_wo, (0, 0), wx.DefaultSpan)
        grid.Add(btn_add_snr, (0, 2), wx.DefaultSpan)
        grid.Add(btn_del_snr, (0, 3), wx.DefaultSpan)

        grid.Add(lbl_work_order, (2, 0), wx.DefaultSpan)
        grid.Add(txt_work_order, (3, 0), wx.DefaultSpan, wx.EXPAND)
        grid.Add(lbl_process, (4, 0), wx.DefaultSpan)
        grid.Add(cmb_process, (5, 0), wx.DefaultSpan, wx.EXPAND)
        grid.Add(lbl_serials, (2, 2), wx.DefaultSpan)
        grid.Add(lst_serials, (3, 2), (4, 2), wx.EXPAND)

        grid.AddGrowableCol(3)
        grid.AddGrowableRow(6)

        return grid

    def _create_start_button(self, parent):
        btn_start = wx.Button(parent, wx.ID_ANY, "START", size=(200, 50))
        btn_start.SetFont(wx.Font(
            14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        return btn_start

    def _create_console(self, parent):
        lbl_console = wx.StaticText(parent, wx.ID_ANY, "Log messages:")
        txt_console = wx.TextCtrl(parent, style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY |
                                    wx.TE_RICH)
        txt_console.SetFont(wx.Font(
            9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))

        grid = wx.GridBagSizer(5, 5)
        grid.Add(lbl_console, (0, 0), wx.DefaultSpan)
        grid.Add(txt_console, (1, 0), wx.DefaultSpan, wx.EXPAND)
        grid.AddGrowableCol(0)
        grid.AddGrowableRow(1)

        return grid


if __name__ == "__main__":

    from src.main import run_main

    run_main()
