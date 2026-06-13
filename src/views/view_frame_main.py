"""
Main view for the application.
"""

import wx

import src.app_data as AppData
import src.views.gui_sizes as GuiSizes

from src.views.view_list_autosize import ListAutosize
from src.views.view_panel_logger import ViewPanelLogger


class ViewFrameMain(wx.Frame):

    # Minimum screen resolution: 1366×768 / 1280x720 (still used on older laptops, anno 2026)
    _MIN_WINDOW_SIZE = (1000, 700)

    def __init__(self, title):
        super().__init__(None, title=title)

        panel = wx.Panel(self)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_input_controls(panel), 2, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_start_button(panel), 0, wx.ALIGN_CENTER | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_console(panel), 3, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        panel.SetSizer(box)
        self.SetInitialSize(self._MIN_WINDOW_SIZE)


    def _create_input_controls(self, parent):
        btn_load_wo = wx.Button(parent, wx.ID_ANY, "Load work order")
        btn_add_snr = wx.Button(parent, wx.ID_ANY, "Add serial number")
        btn_del_snr = wx.Button(parent, wx.ID_ANY, "Remove serial number")

        lbl_work_order = wx.StaticText(parent, wx.ID_ANY, "Work order:")
        txt_work_order = wx.TextCtrl(parent, size=GuiSizes.WIDTH_LARGE)
        lbl_process = wx.StaticText(parent, wx.ID_ANY, "Process:")
        self._cmb_process = wx.ComboBox(parent, style=wx.CB_READONLY, size=GuiSizes.WIDTH_LARGE)
        lbl_serials = wx.StaticText(parent, wx.ID_ANY, "Serial numbers:")
        lst_serials = ListAutosize(parent, wx.ID_ANY)
        lst_serials.add_cols(["Serial number"], [0])

        grid = wx.GridBagSizer(*GuiSizes.GRID_SPACING)
        grid.Add(btn_load_wo, (0, 0), wx.DefaultSpan)
        grid.Add(btn_add_snr, (0, 2), wx.DefaultSpan)
        grid.Add(btn_del_snr, (0, 3), wx.DefaultSpan)

        grid.Add(lbl_work_order, (2, 0), wx.DefaultSpan)
        grid.Add(txt_work_order, (3, 0), wx.DefaultSpan)
        grid.Add(lbl_process, (4, 0), wx.DefaultSpan)
        grid.Add(self._cmb_process, (5, 0), wx.DefaultSpan)
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
        nb = wx.Notebook(parent)
        app_log = ViewPanelLogger(nb, AppData.APP_LOG_FILE)
        proc_log = ViewPanelLogger(nb)
        nb.AddPage(app_log, "Application log")
        nb.AddPage(proc_log, "Process log")
        return nb

    ##########
    # Public #
    ##########

    def init_processes(self, process_names):
        self._cmb_process.SetItems(sorted(process_names))


if __name__ == "__main__":

    from src.main import run_main

    run_main()
