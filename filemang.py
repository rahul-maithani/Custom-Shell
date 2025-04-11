from tkinter import *
from backend import *

class fileManWindow():
    def __init__(self):
        self.window=Tk()
        self.mainWindow()
    def handleShowFile(self,event):
        self.backendObj=shellBackend()
        self.outputArea.insert(END,f"\n{self.backendObj.getls()}\n")
    def mainWindow(self):
        self.window.title("File Management Window")
        self.window.configure(width='800px',height='500px')

        self.showFiles=Button(self.window,text="Run 'ls' command",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.showFiles.place(relx=.01,relheight=.15,relwidth=.2)

        self.outputArea=Text(self.window,font=('Times',16),padx=4,pady=4,borderwidth=3,relief='ridge',bg="black",fg="white",insertbackground="white")
        self.outputArea.place(relx=.01,rely=.5,relheight=.45,relwidth=.98)

        self.outputArea.insert(END,"Myshell> ")
        self.showFiles.bind("<Button-1>",self.handleShowFile)

    def run(self):
        self.window.mainloop()

        
        
        # self.button=
# try:
#     app=fileManWindow()
#     app.run()
# except Exception as e:
#     print(e)