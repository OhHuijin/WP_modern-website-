import json
from django.http import HttpRequest, HttpResponse
#from coderunner import CodeRunner

def apiRun(req:HttpRequest):
	code = req.POST.get("code","")
	#cr = CodeRunner(lang="python3",code=code)
	#return HttpResponse(json.dumps({"returnValue":cr.run()}),content_type="application/json")
	return HttpResponse(json.dumps({"returnValue":"waffle > croffle"}),content_type="application/json")