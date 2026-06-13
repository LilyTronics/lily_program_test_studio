"""
Main controller.
"""

import wx

from src.models.application_settings import ApplicationSettings
from src.models.process_registry import ProcessesRegistry
from src.views.view_dialog_progress import ViewDialogProgress
from src.views.view_dialogs import ViewDialogs
from src.views.view_frame_main import ViewFrameMain


class ControllerMain:

    def __init__(self, title, logger):
        self._log = logger
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

    ##################
    # Event handlers #
    ##################

    def _on_view_close(self, event):
        self._app_settings.store_main_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._app_settings.store_main_window_position(*self._view.GetPosition())
            self._app_settings.store_main_window_size(*self._view.GetSize())
        event.Skip()


if __name__ == "__main__":

    from src.main import run_main

    run_main(True)
