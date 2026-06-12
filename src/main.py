"""
Run the application.
"""

import wx

import src.app_data as AppData

from src.controllers.controller_main import ControllerMain
from src.models.logger import Logger


def run_main():
    logger = Logger(AppData.APP_LOG_FILE)
    logger.info("Application started")
    logger.info(f"Application path    : {AppData.APP_PATH}")
    logger.info(f"Processes path      : {AppData.PROCESSES_PATH}")
    logger.info(f"Application log file: {AppData.APP_LOG_FILE}")

    app = wx.App(redirect=False)
    app.SetAppName(AppData.EXE_NAME)
    ControllerMain(f"{AppData.APP_NAME} V{AppData.VERSION}")
    app.MainLoop()

    logger.info("Application stopped")
    logger.shut_down()

if __name__ == "__main__":

    run_main()
