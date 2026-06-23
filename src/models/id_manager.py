"""
ID manager for the controls
"""

import wx


ID_BTN_LOAD_WO = wx.NewIdRef()
ID_BTN_ADD_SERIAL = wx.NewIdRef()
ID_BTN_DEL_SERIAL = wx.NewIdRef()
ID_BTN_CLEAR = wx.NewIdRef()
ID_BTN_RUN = wx.NewIdRef()
ID_BTN_ABORT = wx.NewIdRef()


if __name__ == "__main__":

    from tests.unit_tests.model_tests.id_manager_test import IdManagerTest

    IdManagerTest().run(True)
