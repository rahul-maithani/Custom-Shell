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
            res=subprocess.check_output(["powershell", "-Command", "ls"]).strip().decode('utf-8')
            return res
        except Exception as e:
            print(f"Error: {e}")
            return 0
        

        
# try:
#     obj=shellBackend()
#     obj.getls()
# except Exception as e:
#     print(e)