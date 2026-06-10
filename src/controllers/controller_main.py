"""
Main controller.
"""

from src.views.view_frame_main import ViewFrameMain


class ControllerMain:

    def __init__(self, title):
        self._view = ViewFrameMain(title)
        self._view.Show()


if __name__ == "__main__":

    from src.main import run_main

    run_main()
