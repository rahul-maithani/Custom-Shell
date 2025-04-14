from tkinter import *
from backend import *
from filemang import *
from systeminfo import *

class shell:
    def __init__(self):
        self.window=Tk()
        self.backEndObj=shellBackend()
        self.mainWindow()
    def run(self):
        self.window.mainloop()
    
    def handleFileManagement(self,event):
        self.fileWindow=fileManWindow()
        self.fileWindow.run()
    
    def handleSystemInfo(self,event):
        self.systeminfoobj=SystemInfo()
        self.systeminfoobj.run()
        
    
    def mainWindow(self):
        self.window.title("Custom Shell")
        self.window.configure(width='800px',height='500px')

        header=Label(text="GUI Based Shell",font=('Helvetica',18,'bold'),borderwidth=2,relief='raised')
        header.place(relheight=.04,relwidth=1)
        
        shellPos=Label(text=f"Shell = {self.backEndObj.currentPos}",font=('Arial',14))
        shellPos.place(rely=.05,relwidth=.2,relheight=.02,relx=.01)


        self.fileManagementBtn=Button(self.window,text="File Management",font=('Arial',15,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.fileManagementBtn.place(rely=.08,relx=.01,relheight=.2,relwidth=.2)

        self.networkBtn=Button(self.window,text="Network",font=('Arial',15,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.networkBtn.place(rely=.08,relx=.22,relheight=.2,relwidth=.2)
        self.systeminfoBtn=Button(self.window,text="SystemInfo",font=('Arial',15,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.systeminfoBtn.place(rely=.08,relx=.43,relheight=.2,relwidth=.2)



        self.fileManagementBtn.bind("<Button-1>",self.handleFileManagement)
        self.systeminfoBtn.bind("<Button-1>",self.handleSystemInfo)


        # self.button=
try:
    app=shell()
    app.run()
except Exception as e:
    print(e)