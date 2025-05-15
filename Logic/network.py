from tkinter import *
from backend import *

class network():
    def __init__(self):
        self.backendObj=shellBackend()
        self.window=Tk()
        self.backendObj=shellBackend()
        self.inputType="xyz"
        self.mainWindow()

    def on_enter(self,event):
        inputRes=self.inputEntry.get()
        self.inputEntry.delete(0,END)
        self.inputFrame.place_forget()

        if(self.inputType=='ping'):
            self.outputArea.insert(END,f"\n{self.backendObj.pingRun(inputRes)}\n")
        elif(self.inputType=='getIp'):
            self.outputArea.insert(END,f"\nMyshell>{self.backendObj.getIp(inputRes)}\n")
        elif(self.inputType=='curl'):
            self.outputArea.insert(END,f'\nMyshell>{self.backendObj.curl(inputRes).stdout}\n')
        self.outputArea.yview(END)

    def handleCurl(self,event):
        self.inputType="curl"
        self.inputFrame.place(rely=.5,relx=.01,relheight=.09,relwidth=.98)
        self.inputText.config(text="Enter the url to curl:")
        

    def handlePingBtn(self,event):
        self.inputType="ping"
        self.inputFrame.place(rely=.5,relx=.01,relheight=.09,relwidth=.98)
        self.inputText.config(text="Enter the url,ip to ping:")

    def handleIpBtn(self,event):
        self.inputType="getIp"
        self.inputFrame.place(rely=.5,relx=.01,relheight=.09,relwidth=.98)
        self.inputText.config(text="Enter the url whoose ip you want to get:")

    def handletracertBtn(self,event):
        self.outputArea.insert(END,f"\nMyshell>{self.backendObj.tracertRun()}\n")
        self.outputArea.yview(END)
    def handleIpConfig(self,event):
        self.outputArea.insert(END,f'\nMyshell>{self.backendObj.ipconfig()}\n')
        self.outputArea.yview(END)
    def handleHostBtn(self,event):
        self.outputArea.insert(END,f"\nMyshell> Hostname : {self.backendObj.hostRun()}\n")
        self.outputArea.yview(END)
    def handleExit(self,event):
        self.window.after(1, self.window.destroy)
    def mainWindow(self):
        self.window.title("Network")
        self.window.configure(width='800px',height='500px')

        self.pingBtn=Button(self.window,text="Ping",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.pingBtn.place(relx=.01,relheight=.15,relwidth=.18)

        self.tracertBtn=Button(self.window,text="Tracert",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.tracertBtn.place(relx=.2,relwidth=.18,relheight=.15)
        self.hostBtn=Button(self.window,text="Host name",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.hostBtn.place(relx=.39,relwidth=.18,relheight=.15)

        self.getIpBtn=Button(self.window,text="Get Ip ",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.getIpBtn.place(relx=.58,relwidth=.18,relheight=.15)

        self.curlBtn=Button(self.window,text="Curl",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.curlBtn.place(relx=.77,relwidth=.18,relheight=.15)
        self.ipConfigBtn=Button(self.window,text="Ip Config",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.ipConfigBtn.place(relx=.01,relwidth=.18,relheight=.15,rely=.16)
        self.exitButton=Button(self.window,text="Exit",font=('Arial',12,'bold'),cursor='hand2',borderwidth=3,relief='ridge')
        self.exitButton.place(relx=.2,relwidth=.18,relheight=.15,rely=.16)



        self.inputFrame=Frame(self.window,border=1,relief='groove')
        self.inputFrame.place(rely=.5,relx=.01,relheight=.09,relwidth=.98)
        self.inputFrame.place_forget()
        self.inputText=Label(self.inputFrame,text="",font=('Times',16),padx=4,pady=4,anchor='w')
        self.inputText.place(relx=.01,rely=.1,relheight=.8,relwidth=.7)

        self.inputEntry=Entry(self.inputFrame,font=('Times',14),justify='center',borderwidth=1,relief='ridge',fg="black")
        self.inputEntry.place(relx=.72,rely=.1,relheight=.8,relwidth=.27)
        self.inputEntry.bind("<Return>",self.on_enter)

        self.outputArea=Text(self.window,font=('Times',16),padx=4,pady=4,borderwidth=3,relief='ridge',bg="black",fg="lime",insertbackground='lime')
        self.outputArea.place(relx=.01,rely=.6,relheight=.39,relwidth=.98)


        self.outputArea.insert(END,"Myshell> ")
        self.pingBtn.bind("<Button-1>",self.handlePingBtn)
        self.tracertBtn.bind("<Button-1>",self.handletracertBtn)
        self.exitButton.bind("<Button-1>",self.handleExit)
        self.hostBtn.bind("<Button-1>",self.handleHostBtn)
        self.getIpBtn.bind("<Button-1>",self.handleIpBtn)
        self.curlBtn.bind("<Button-1>",self.handleCurl)
        self.ipConfigBtn.bind("<Button-1>",self.handleIpConfig)

    def run(self):
        self.window.mainloop()

# obj=network()
# obj.run()