"""
Run the application.
"""

import wx

import src.app_data as AppData

from src.controllers.controller_main import ControllerMain
from src.models.console_redirect import ConsoleRedirect
from src.models.logger import Logger


def run_main(log_to_stdout=False):
    logger = Logger()
    logger.add_handler(open(AppData.APP_LOG_FILE, "w", encoding="utf-8"))
    ConsoleRedirect.enable_redirect()
    ConsoleRedirect.add_logger(logger)
    if log_to_stdout:
        logger.add_handler(ConsoleRedirect.org_stdout)
    logger.info("Application started")
    logger.info(f"Application path    : {AppData.APP_PATH}")
    logger.info(f"Processes path      : {AppData.PROCESSES_PATH}")
    logger.info(f"Application log file: {AppData.APP_LOG_FILE}")

    app = wx.App(redirect=False)
    app.SetAppName(AppData.EXE_NAME)
    ControllerMain(f"{AppData.APP_NAME} V{AppData.VERSION}", logger)
    app.MainLoop()

    logger.info("Application stopped")
    ConsoleRedirect.restore_redirect()


if __name__ == "__main__":

    run_main()
