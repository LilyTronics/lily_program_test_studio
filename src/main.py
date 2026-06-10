"""
Run the application.
"""

import wx

import src.app_data as AppData

from src.controllers.controller_main import ControllerMain


def run_main():
    app = wx.App(redirect=False)
    app.SetAppName(AppData.EXE_NAME)
    ControllerMain(f"{AppData.APP_NAME} V{AppData.VERSION}")
    app.MainLoop()


if __name__ == "__main__":

    run_main()
