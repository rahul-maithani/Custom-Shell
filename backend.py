import os
import subprocess

class shellBackend:
    def __init__(self):
        self.currentPos=self.getCurrentPos().strip().decode('utf-8')
        self.currentPos=self.currentPos.split("\n")[-1]

    def getCurrentPos(self):
        try:
            res=subprocess.check_output(["powershell", "-Command", "pwd"])
            return res
        except Exception as e:
            print(f"Error: {e}")
            return 0
    def getls(self):
        try:
            res="command - ls\n"+subprocess.check_output(["powershell", "-Command", "ls"]).strip().decode('utf-8')
            return res
        except Exception as e:
            print(f"Error: {e}")
            return 0
    def createnewFile(self,file_name):
        return os.system(f'type nul > {file_name}')
    def createNewFolder(self,folder_name):
        return os.system(f'mkdir {folder_name}')
    
    def deleteFile(self,file_name):
        return os.system(f"del {file_name}")
    def deleteFolder(self,folder_name):
        return os.system(f"rmdir {folder_name}")
    def pingRun(self,url):
        res=subprocess.run(["ping","-n","4",f"{url}"],capture_output=True, text=True)
        return res.stdout
    def tracertRun(self):
        res=subprocess.run(["tracert"],capture_output=True, text=True)
        print(res)
        return res.stdout
# try:
#     obj=shellBackend()
#     obj.getls()
# except Exception as e:
#     print(e)