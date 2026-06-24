"""
Main controller.
"""

import wx

import src.models.id_manager as IdManager

from src.models.application_settings import ApplicationSettings
from src.models.process_registry import ProcessesRegistry
from src.models.process_runner import ProcessRunner
from src.models.work_order import WorkOrder
from src.views.view_dialog_progress import ViewDialogProgress
from src.views.view_dialogs import ViewDialogs
from src.views.view_frame_main import ViewFrameMain


class ControllerMain:

    _TIMER_SPEED = 100
    _BLINK_SPEED = 5

    def __init__(self, title, logger):
        self._log = logger
        self._blink_ticks = 0
        self._last_led_color = None
        self._process_state = 0
        self._app_settings = ApplicationSettings()
        self._view = ViewFrameMain(title)
        self._prepare_view()
        self._view.Show()
        wx.CallAfter(self._load_processes)

    ###########
    # Private #
    ###########

    def _prepare_view(self):
        value = self._app_settings.get_main_window_position()
        if -1 not in value:
            self._view.SetPosition(value)
        value = self._app_settings.get_main_window_size()
        if -1 not in value:
            self._view.SetSize(value)
        self._view.Maximize(self._app_settings.get_main_window_maximized())

        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)
        self._view.Bind(wx.EVT_BUTTON, self._on_load_work_order, id=IdManager.ID_BTN_LOAD_WO)
        self._view.Bind(wx.EVT_BUTTON, self._on_add_serial, id=IdManager.ID_BTN_ADD_SERIAL)
        self._view.Bind(wx.EVT_BUTTON, self._on_del_serial, id=IdManager.ID_BTN_DEL_SERIAL)
        self._view.Bind(wx.EVT_BUTTON, self._on_clear, id=IdManager.ID_BTN_CLEAR)
        self._view.Bind(wx.EVT_BUTTON, self._on_start, id=IdManager.ID_BTN_RUN)
        self._view.Bind(wx.EVT_BUTTON, self._on_abort, id=IdManager.ID_BTN_ABORT)

        self._update_timer = wx.Timer()
        self._update_timer.Bind(wx.EVT_TIMER, self._on_update_timer)
        self._update_timer.Start(self._TIMER_SPEED)

        self._view.enable_controls(True)

    def _load_processes(self):
        dlg_title = "Loading processes"
        self._log.debug(dlg_title)
        dlg = ViewDialogProgress(self._view, "Loading processes")
        try:
            ProcessesRegistry.load(dlg.update)
        except Exception as e:
            self._log.error(f"Error loading processes: {e}")
            ViewDialogs.show_message(self._view, f"Error loading drivers: {e}",
                                     dlg_title, wx.ICON_EXCLAMATION)
        dlg.Close()
        self._log.debug(f"{len(ProcessesRegistry.get_processes())} processes loaded")
        self._view.init_processes(ProcessesRegistry.get_process_names())

    def _clear_input(self):
        self._view.init_work_order("", "", [])

    def _run_on_process_start(self):
        self._view.enable_controls(False)
        self._view.show_process_log()
        self._view.clear_process_log()
        self._process_state = 1

    def _run_on_process_end(self):
        self._view.enable_controls(True)
        self._process_state = 0

    ##################
    # Event handlers #
    ##################

    def _on_load_work_order(self, event):
        dlg_title = "Load work order"
        filename = ViewDialogs.show_open_file(self._view, dlg_title,
                                              file_filter="JSON files|*.json")
        if filename is not None:
            self._log.debug(f"Load work order: {filename}")
            self._clear_input()
            try:
                WorkOrder.read_from_file(filename)
                self._view.init_work_order(WorkOrder.get_work_order(),
                                           WorkOrder.get_process(),
                                           WorkOrder.get_serial_numbers())
            except Exception as e:
                self._log.error(f"Error loading work order: {e}")
                ViewDialogs.show_message(self._view, f"Error loading work order: {e}",
                                        dlg_title, wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_add_serial(self, event):
        dlg_title = "Add serial number"
        value = ViewDialogs.show_text_input(self._view, "Enter one or more serial numbers, "
                                            "separate serial numbers with a comma:", dlg_title,
                                            width=500)
        if value is not None:
            parts = [x.strip() for x in value.split(",")]
            parts = [ x for x in parts if x != ""]
            self._view.append_serial_numbers(parts)
        event.Skip()

    def _on_del_serial(self, event):
        dlg_title = "Remove serial number"
        serial = self._view.get_selected_serial_number()
        if serial is None:
            ViewDialogs.show_message(self._view, "Select a serial number from the list.",
                                     dlg_title)
        else:
            result = ViewDialogs.show_confirm(self._view, f"Remove serial number: '{serial}'?",
                                              dlg_title)
            if result == wx.ID_YES:
                self._view.remove_serial_number(serial)
        event.Skip()

    def _on_clear(self, event):
        self._clear_input()
        event.Skip()

    def _on_start(self, event):
        settings = self._view.get_settings()
        try:
            settings["output_folder"] = WorkOrder.get_output_folder()
            self._log.info(f"Run process: '{settings["process"]}'")
            ProcessRunner.run_process(settings)
            self._run_on_process_start()
        except Exception as e:
            self._log.error(f"Error running process: {e}")
            ViewDialogs.show_message(self._view, f"Error running process: {e}",
                                        "Run process", wx.ICON_EXCLAMATION)
        event.Skip()

    def _on_abort(self, event):
        self._log.info("Abort process")
        ProcessRunner.abort()
        event.Skip()

    def _on_update_timer(self, event):
        if ProcessRunner.is_running():
            if self._blink_ticks == self._BLINK_SPEED:
                if self._last_led_color == self._view.LED_COLOR_ON:
                    self._last_led_color = self._view.LED_COLOR_OFF
                else:
                    self._last_led_color = self._view.LED_COLOR_ON
                self._blink_ticks = 0
            else:
                self._blink_ticks += 1
            self._view.update_status(ProcessRunner.get_duration_time())
        else:
            self._last_led_color = self._view.LED_COLOR_OFF
            if self._process_state == 1:
                self._run_on_process_end()

        self._view.set_led_color(self._last_led_color)
        event.Skip()

    def _on_view_close(self, event):
        self._app_settings.store_main_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._app_settings.store_main_window_position(*self._view.GetPosition())
            self._app_settings.store_main_window_size(*self._view.GetSize())
        event.Skip()


if __name__ == "__main__":

    from src.main import run_main

    run_main(True)
