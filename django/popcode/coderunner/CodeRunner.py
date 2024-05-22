import subprocess

class CodeRunner:
	def __init__(self,code="print('Hello World')",lang="python3") -> None:
		self.code = code
		self.lang = lang
	
	def run(self) -> int:
		if self.lang == "python3":
			f = open("temp.py","w")
			f.write(self.code)
			f.close()
			status = subprocess.call(["python3","temp.py"])
			return status
		return -1