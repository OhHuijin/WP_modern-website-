import subprocess

class CodeRunner:
    returnCode = 0
    stdout = ""
    stderr = ""
    def __init__(self,code="print('Hello World')",lang="python3") -> None:
        self.code = code
        self.lang = lang
    
    """
    Run the code and store the output, error and return code
     """
    def run(self) -> int:
        if self.lang == "python3":
            f = open("temp.py","w")
            f.write(self.code)
            f.close()
            process = subprocess.run(["python3","temp.py"],capture_output=True,text=True)
            self.stdout = process.stdout
            self.stderr = process.stderr
            self.returnCode = process.returncode
        else:
            print("Language not supported")
   
    """
    Check if the code ran successfully
    """
    def isSuccessful(self) -> bool:
        return self.returnCode == 0
    
    """
    Return the output as a dictionary
    """
    def outputDict(self) -> dict:
        return {
            "stdout":self.stdout,
            "stderr":self.stderr,
            "returnCode":self.returnCode
        }