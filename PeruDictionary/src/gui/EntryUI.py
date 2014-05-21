import wx

#Import UI elements
import DictConstants
from database import DictDB, EntryDB
        
largeBoxHeight = 8
largeBoxWidth = 10

class EntryUIFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    def __init__(self, parent, EntryID):
        """Constructor"""
        wx.Frame.__init__(self, parent, wx.ID_ANY,"Peru Dictionary",size=(1200,800))
        
        self.SetBackgroundColour("WHITE")
        self.CenterOnScreen()
        self.CreateStatusBar()
        self.SetStatusText("I love you!")
        self.EntryID = EntryID
        
        if self.EntryID != '':
            self.EntryFields = EntryDB.ReadEntry(self.EntryID)[1][0]
        else:
            self.EntryFields = []

        # Prepare the menu bar test
        menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        menu1.Append(101, "&Close", "Close")
        menuBar.Append(menu1, "&File")
        
        menu2 = wx.Menu()
        menu2.Append(201, "&About", "Program Information")
        menuBar.Append(menu2, "&About")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.CloseWindow, id=101)
        self.Bind(wx.EVT_MENU, self.AboutInfo, id=201)
        
        fieldList = self.fieldList = []

        Word = self.Word = wx.TextCtrl(self, size=(400,-1),name="Word")
        fieldList.append((wx.StaticText(self, label="Word :"), Word))
        
        Source = self.Source = wx.TextCtrl(self, size=(400,-1))
        fieldList.append((wx.StaticText(self, label="Source :"), Source))
        
        Definition = self.Definition = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        fieldList.append((wx.StaticText(self, label="Definition :"), Definition))
        
        Notes = self.Notes = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        fieldList.append((wx.StaticText(self, label="Notes :"), Notes))

        space = 6
        infoSizer = wx.GridBagSizer(hgap=space, vgap=space)
        
        row = 1        
        infoSizer.Add(fieldList[0][0],    (row,1))
        infoSizer.Add(fieldList[0][1],    (row,2))
        row = row + 1
            
        infoSizer.Add(fieldList[1][0],    (row,1))
        infoSizer.Add(fieldList[1][1],    (row,2))
        row = row + 1
            
        infoSizer.Add(fieldList[2][0],    (row,1))
        infoSizer.Add(fieldList[2][1],    (row,2), (largeBoxHeight,largeBoxWidth), wx.EXPAND)
        row = row + largeBoxHeight
            
        infoSizer.Add(fieldList[3][0],    (row,1))
        infoSizer.Add(fieldList[3][1],    (row,2), (largeBoxHeight,largeBoxWidth), wx.EXPAND)
        row = row + largeBoxHeight

        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.saveButton = wx.Button(self, -1, "Save")
        self.buttonSizer.Add(self.saveButton, 0, wx.ALIGN_RIGHT)
        
        self.Bind(wx.EVT_BUTTON, self.OnButtonSave, self.saveButton)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(infoSizer, 1, wx.EXPAND)
        self.sizer.Add(self.buttonSizer, 0, wx.EXPAND)
        
        if self.EntryID != '':
            self.PopulateFields()
        
        self.SetSizer(self.sizer)
        self.Layout()

        self.Show()
        
    def OnButtonSave(self, evt):
        self.saveEntry()
        self.Parent.PopulateList()

    def CloseWindow(self, event):
        self.Close()

    def AboutInfo(self, event):
        dlg = wx.MessageDialog(self, 'Work in progress', 'About', wx.OK )
        dlg.ShowModal()
        dlg.Destroy()
            
    def PopulateFields(self):
        self.Word.WriteText(self.EntryFields[DictConstants.ENTRY_FIELDS.index('Word')])
        self.Source.WriteText(self.EntryFields[DictConstants.ENTRY_FIELDS.index('Source')])
        self.Definition.WriteText(self.EntryFields[DictConstants.ENTRY_FIELDS.index('Definition')])
        self.Notes.WriteText(self.EntryFields[DictConstants.ENTRY_FIELDS.index('Notes')])

    def getEntryInfo(self):    
        return [str(self.EntryID),
                str(self.Word.GetValue()),
                str(self.Source.GetValue()),
                str(self.Definition.GetValue()),
                str(self.Notes.GetValue())]
        
    def saveEntry(self):
        database = DictDB.DictDB()
        
        try:
            EntryDB.InsertUpdateEntry(database, self.getEntryInfo())
                
        except:
            print("Database Error!")
            database.rollback()            
            return        
        
        database.commit()
        database.closeDB()
        
        
        
        
        
        
