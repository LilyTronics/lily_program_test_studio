"""
Main view for the application.
"""

import wx

import src.app_data as AppData
import src.models.id_manager as IdManager
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
        box.Add(self._create_buttons(panel), 0, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)
        box.Add(self._create_console(panel), 3, wx.EXPAND | wx.ALL, GuiSizes.BOX_SPACING)

        panel.SetSizer(box)
        self.SetInitialSize(self._MIN_WINDOW_SIZE)


    def _create_input_controls(self, parent):
        btn_load_wo = wx.Button(parent, IdManager.ID_BTN_LOAD_WO, "Load work order")
        btn_add_snr = wx.Button(parent, IdManager.ID_BTN_ADD_SERIAL, "Add serial number")
        btn_del_snr = wx.Button(parent, IdManager.ID_BTN_DEL_SERIAL, "Remove serial number")
        btn_clear = wx.Button(parent, IdManager.ID_BTN_CLEAR, "Clear input")

        lbl_work_order = wx.StaticText(parent, wx.ID_ANY, "Work order:")
        self._txt_work_order = wx.TextCtrl(parent, size=GuiSizes.WIDTH_LARGE)
        lbl_process = wx.StaticText(parent, wx.ID_ANY, "Process:")
        self._cmb_process = wx.ComboBox(parent, style=wx.CB_READONLY, size=GuiSizes.WIDTH_LARGE)
        lbl_serials = wx.StaticText(parent, wx.ID_ANY, "Serial numbers:")
        self._lst_serials = ListAutosize(parent, wx.ID_ANY)
        self._lst_serials.add_cols(["Serial number"], [0])

        grid = wx.GridBagSizer(*GuiSizes.GRID_SPACING)
        grid.Add(btn_load_wo, (0, 0), wx.DefaultSpan)
        grid.Add(btn_add_snr, (0, 2), wx.DefaultSpan)
        grid.Add(btn_del_snr, (0, 3), wx.DefaultSpan)
        grid.Add(btn_clear, (0, 4), wx.DefaultSpan)

        grid.Add(lbl_work_order, (2, 0), wx.DefaultSpan)
        grid.Add(self._txt_work_order, (3, 0), wx.DefaultSpan)
        grid.Add(lbl_process, (4, 0), wx.DefaultSpan)
        grid.Add(self._cmb_process, (5, 0), wx.DefaultSpan)
        grid.Add(lbl_serials, (2, 2), wx.DefaultSpan)
        grid.Add(self._lst_serials, (3, 2), (4, 3), wx.EXPAND)

        grid.AddGrowableCol(2)
        grid.AddGrowableRow(3)

        return grid

    def _create_buttons(self, parent):
        btn_start = wx.Button(parent, IdManager.ID_BTN_RUN, "RUN", size=(200, 50))
        btn_start.SetFont(wx.Font(
            14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn_abort = wx.Button(parent, IdManager.ID_BTN_ABORT, "ABORT", size=(100, 40))
        btn_abort.SetFont(wx.Font(
            12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.AddStretchSpacer(1)
        box.Add(btn_start, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, GuiSizes.BOX_SPACING)
        box.AddStretchSpacer(1)
        box.Add(btn_abort, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, GuiSizes.BOX_SPACING)
        return box

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

    def init_work_order(self, work_order, process, serial_numbers):
        self._txt_work_order.SetValue(work_order)
        if process not in self._cmb_process.GetItems():
            self._cmb_process.SetSelection(wx.NOT_FOUND)
            if process != "":
                raise Exception(f"The process '{process}' does not exist")
        else:
            self._cmb_process.SetValue(process)
        self._lst_serials.DeleteAllItems()
        self.append_serial_numbers(serial_numbers)

    def append_serial_numbers(self, serials):
        for serial in serials:
            item = wx.ListItem()
            item.SetId(self._lst_serials.GetItemCount())
            item.SetText(serial)
            self._lst_serials.InsertItem(item)

    def get_selected_serial_number(self):
        serial = None
        index = self._lst_serials.GetFirstSelected()
        if index != -1:
            serial = self._lst_serials.GetItemText(index)
        return serial

    def remove_serial_number(self, serial_number):
        index = self._lst_serials.FindItem(-1, serial_number)
        if index != -1:
            self._lst_serials.DeleteItem(index)

    def get_settings(self):
        return {
            "work_order": self._txt_work_order.GetValue().strip(),
            "process": self._cmb_process.GetValue().strip(),
            "serial_numbers": [
                self._lst_serials.GetItemText(i)
                for i in range(self._lst_serials.GetItemCount())
            ]
        }


if __name__ == "__main__":

    from src.main import run_main

    run_main()
