'''
Created on Apr 26, 2014

@author: Eric
'''

import  wx
from gui import DictListUI
from database import DictDB

#----------------------------------------------------------------------

    
if __name__ == "__main__":
    DictDB.DatabaseBackup()
    app = wx.App(False)
    frame = DictListUI.DictListCtrlFrame()
    app.MainLoop()
    
    