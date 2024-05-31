import subprocess
from time import sleep

from django.urls import include


class CodeRunner:
    returnCode = 0
    stdout = ""
    stderr = ""

    def __init__(self, code="print('Hello World')", lang="python3") -> None:
        self.code = code
        self.lang = lang

    """
    Run the code and store the output, error and return code
     """

    def run(self) -> int:
        if self.lang == "python3":
            if "import " in self.code or "open(" in self.code or "exec(" in self.code:
                self.stdout = "🤖 [PopBot] Illegal imports detected !"
                self.returnCode = 1
                return 1
            f = open("temp.py", "w")
            f.write(self.code)
            f.close()
            process = subprocess.Popen(
                ["python3", "temp.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                # Wait for 15 seconds for process to complete
                stdout_data, stderr_data = process.communicate(timeout=15)
                self.returnCode = process.returncode
            except subprocess.TimeoutExpired:
                # If the process is not completed in 15 seconds kill it
                process.kill()
                stdout_data, stderr_data = process.communicate()
                self.stdout = "🤖 [PopBot] Process took too long to complete !"
                self.returnCode = 2
                return 2

            self.stdout = stdout_data
            self.stderr = stderr_data
            return self.returnCode
        elif self.lang == "c":
            if "#include " in self.code or "system(" in self.code:
                self.stdout = "🤖 [PopBot] Illegal imports detected !"
                self.returnCode = 1
                return 1
            f = open("temp.c", "w")
            f.write("#include <stdio.h>\n")
            f.write("#include <stdlib.h>\n")
            f.write(self.code)
            f.close()
            process = subprocess.Popen(
                ["gcc", "temp.c", "-o", "temp"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout_data, stderr_data = process.communicate()
            self.returnCode = process.returncode
            self.stdout = stdout_data
            self.stderr = stderr_data
            print(">>>>", stderr_data, stdout_data, self.returnCode)
            if self.returnCode != 0:
                return self.returnCode
            process = subprocess.Popen(
                ["./temp"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:
                stdout_data, stderr_data = process.communicate(timeout=15)
                self.stdout += stdout_data
                self.stderr += stderr_data
                self.returnCode = process.returncode
                return self.returnCode
            except subprocess.TimeoutExpired:
                process.kill()
                stdout_data, stderr_data = process.communicate()
                self.stdout = "🤖 [PopBot] Process took too long to complete !"
                self.returnCode = 2
                self.stdout += stdout_data
                self.stderr += stderr_data
                return self.returnCode
        else:
            print("Language not supported")
            return 3

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
            "stdout": self.stdout,
            "stderr": self.stderr,
            "returnCode": self.returnCode,
        }

    def cleanAll(self):
        subprocess.Popen(["rm", "temp.py", "-f"])
        subprocess.Popen(["rm", "temp.c", "-f"])
        subprocess.Popen(["rm", "temp", "-f"])
        return 0
