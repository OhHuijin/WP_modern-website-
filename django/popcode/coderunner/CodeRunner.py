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
