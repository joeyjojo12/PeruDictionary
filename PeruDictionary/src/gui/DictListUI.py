import wx
import wx.lib.mixins.listctrl  as  listmix
import EntryUI
from database import EntryDB

#---------------------------------------------------------------------------

class DictListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class DictListCtrlFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,"Peru Dictionary",size=(1200,800))
        
        tID = wx.NewId()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.list = DictListCtrl(self, tID,
                                 style=wx.LC_REPORT 
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        sizer.Add(self.list, 1, wx.EXPAND)

        self.PopulateList()

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        #self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)

        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addEntry = wx.Button(self, -1, "Add Word")
        self.buttonSizer.Add(self.addEntry , 0, wx.ALIGN_RIGHT)

        self.Bind(wx.EVT_BUTTON, self.OnButtonAdd, self.addEntry)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.buttonSizer, 0, wx.EXPAND)
        self.sizer.Add(self.list, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)

        #Start
        self.Show()


    def PopulateList(self):
        self.list.ClearAll()
        
        # but since we want images on the column header we have to do it the hard way:
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info.m_image = -1
        info.m_format = 0
        info.m_text = "Word"
        self.list.InsertColumnInfo(0, info)
        
        entries = EntryDB.ReadEntries()[1]
        
        entryDict = {}
        
        for entry in entries:
            entryDict[entry[0]] = entry[1]
        
        for item in entryDict.iteritems():
            index = self.list.InsertStringItem(0, str(item[1]))
            self.list.SetItemData(index, item[0])

        self.list.SetColumnWidth(0, 100)

        # show how to select an item
        self.list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        self.currentItem = 0


    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()


    def OnItemSelected(self, event):
        ##print event.GetItem().GetTextColour()
        self.currentItem = event.m_itemIndex
        #print("OnItemSelected: %s, %s, %s\n" %
        #                   (self.currentItem,
        #                    self.list.GetItemText(self.currentItem),
        #                    self.list.GetItemData(self.currentItem)))#

        #if self.currentItem == 10:
        #    print("OnItemSelected: Veto'd selection\n")
            #event.Veto()  # doesn't work
            # this does
        #    self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

        event.Skip()

    """
    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        print("OnItemDeselected: %d" % evt.m_itemIndex)

        # Show how to reselect something we don't want deselected
        if evt.m_itemIndex == 11:
            wx.CallAfter(self.list.SetItemState, 11, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
    """

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        #print("OnItemActivated: %s\nTopItem: %s" %
        #                   (self.list.GetItemText(self.currentItem), self.list.GetTopItem()))

    def OnBeginEdit(self, event):
        print("OnBeginEdit")
        event.Allow()

    def OnItemDelete(self, event):
        print("OnItemDelete\n")

    def OnColClick(self, event):
        print("OnColClick: %d\n" % event.GetColumn())
        event.Skip()

    def OnColRightClick(self, event):
        item = self.list.GetColumn(event.GetColumn())
        print("OnColRightClick: %d %s\n" %
                           (event.GetColumn(), (item.GetText(), item.GetAlign(),
                                                item.GetWidth(), item.GetImage())))
        if self.list.HasColumnOrderSupport():
            print("OnColRightClick: column order: %d\n" %
                               self.list.GetColumnOrder(event.GetColumn()))


    def OnDoubleClick(self, event):
        
        #Start Main Window
        win = EntryUI.EntryUIFrame(self, self.list.GetItemData(self.currentItem))
        win.Show(True)
        self.frame = win
        
        event.Skip()

    def OnButtonAdd(self, event):
                
        #Start Main Window
        win = EntryUI.EntryUIFrame(self, '')
        win.Show(True)
        self.frame = win
        
        event.Skip()

    def OnRightClick(self, event):
        print("OnRightClick %s\n" % self.list.GetItemText(self.currentItem))

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "FindItem tests")
        menu.Append(self.popupID2, "Iterate Selected")
        menu.Append(self.popupID3, "ClearAll and repopulate")
        menu.Append(self.popupID4, "DeleteAllItems")
        menu.Append(self.popupID5, "GetItem")
        menu.Append(self.popupID6, "Edit")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()





























