import requests
import json
from requests.structures import CaseInsensitiveDict

url = "http://aiasvm1.amcl.tuc.gr:8085/GorgiasQuery"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Basic amlvZ2hvOkxhZGFuaWVsYTU="
headers["Content-Type"] = "application/json"



dat={
  "gorgiasFiles":["example1/assistant.pl"],
  "resultSize": 10
}
#print(json.loads(data))
#resp = requests.post(url, headers=headers, data=data)
#print(json.loads(resp.text)["hasResult"])

def Allow(facts,num):
    dat["facts"]=facts
    #print(facts)
    query="allow("+num+")"
    #print(query)
    dat["query"]=query
    resp = requests.post(url, headers=headers, data=json.dumps(dat))

    return json.loads(resp.text)["hasResult"]


#print(Allow())