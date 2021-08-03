import requests
import webbrowser
import subprocess

min_rating=1600
max_rating=2100
handle="tusharc31"


### Returns list of contests from which questions are to be picked
def fetch_contests():
    data = requests.get("https://codeforces.com/api/contest.list").json()
    contests = []
    for i in data['result']:
        if "ducational" in i['name']:
            contests.append(i['id'])
        if "ICPC" in i['name']:
            contests.append(i['id'])
    return contests


### Returns desirable questions in sorted order
def fetch_all_questions():
    data = requests.get("https://codeforces.com/api/problemset.problems").json()
    qlist=[]
    for i in data['result']['problems']:
        if i['contestId'] in contests:
            try:
                if i['rating']>=min_rating and i['rating']<=max_rating:
                    qlist.append(i)
            except:
                pass

    for i in range(len(qlist)):
        for j in range(len(qlist)):
            if qlist[i]['rating']>qlist[j]['rating'] and i<j:
                a=qlist[i]
                qlist[i]=qlist[j]
                qlist[j]=a
            elif qlist[i]['contestId']<qlist[j]['contestId'] and i<j:
                a=qlist[i]
                qlist[i]=qlist[j]
                qlist[j]=a
    return qlist


### Return questions already solved by the user
def fetch_user_solves():
    questions_finished = []
    data = requests.get("https://codeforces.com/api/user.status?handle="+handle).json()
    for i in data['result']:
        if i['verdict']=="OK":
            questions_finished.append(i['problem'])
    return questions_finished


### Search and print the most relevant question
def search():
    found_status=False
    todo=None
    done=0
    for i in qlist:
        if i in questions_finished:
            done+=1
        elif found_status is False:
            todo=i
            found_status=True
    url='https://codeforces.com/contest/'+str(todo['contestId'])+'/problem/'+todo['index']
    print("\nSolve: "+todo['name'])
    print("Link: "+url)
    print("Progress: "+str(done)+'/'+str(len(qlist))+'\n')  
    return url 


# Launches cpp file with template code and opens the question found in browser
def environment(url):
    subprocess.call(["code", "1.cpp"])
    webbrowser.open(url)


# Calling relevent functions
contests=fetch_contests()
qlist=fetch_all_questions()
questions_finished = fetch_user_solves()
url=search()
environment(url)