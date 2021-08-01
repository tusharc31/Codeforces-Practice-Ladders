import requests
import json

min_rating=1600
max_rating=2100

data = requests.get("https://codeforces.com/api/contest.list").json()
print(data['result'])

contests = []

for i in data['result']:
    if "ducational" in i['name']:
        contests.append(i['id'])
    if "ICPC" in i['name']:
        contests.append(i['id'])

data = requests.get("https://codeforces.com/api/problemset.problems").json()
cnt=0

qlist=[]
qdump={}

for i in data['result']['problems']:
    if i['contestId'] in contests:
       try:
           if i['rating']>=min_rating and i['rating']<=max_rating:
               cnt+=1
               qlist.append(i)
       except:
           pass

qdump['data']=qlist

json_object = json.dumps(qdump, indent = 4)
with open("data.json", "w") as outfile:
    outfile.write(json_object)
