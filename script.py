import requests
import webbrowser
import subprocess

# Set parameters
handle = "tourist"
min_rating = 1800
max_rating = 1900


# Returns list of contest IDs from which problems are to be picked
def fetch_contests():
    data = requests.get("https://codeforces.com/api/contest.list").json()
    contests = []
    for i in data['result']:
        if "ducational" in i['name']:
            contests.append(i['id'])
        if "ICPC" in i['name'] and "otlin" not in i['name']:
            contests.append(i['id'])
    return contests


# Returns desirable problems in sorted order
def fetch_total_problems(contests):
    data = requests.get(
        "https://codeforces.com/api/problemset.problems").json()
    total_problems = []
    for i in data['result']['problems']:
        if i['contestId'] in contests:
            try:
                if i['rating'] >= min_rating and i['rating'] <= max_rating:
                    total_problems.append(i)
            except:
                pass
    total_problems.sort(key=lambda x: x["rating"])
    return total_problems


# Return problems already solved by the user
def fetch_user_solves():
    problems_finished = []
    data = requests.get(
        "https://codeforces.com/api/user.status?handle="+handle).json()
    for i in data['result']:
        if i['verdict'] == "OK":
            problems_finished.append(i['problem'])
    return problems_finished


# Search and print the most relevant problem
def search(total_problems, problems_finished):
    found_status = False
    todo = None
    done = 0
    for i in total_problems:
        if i in problems_finished:
            done += 1
        elif found_status is False:
            todo = i
            found_status = True
    url = 'https://codeforces.com/contest/' + \
        str(todo['contestId'])+'/problem/'+todo['index']
    print("\nSuggested Problem: "+todo['name'])
    print("Link: "+url)
    print("Current Progress: "+str(done)+'/' +
          str(len(total_problems))+' Problems\n')
    return url


# Launches cpp file with template code and opens the problem found in browser
def setup(url):
    # uncomment if you wish to open 1.cpp in vs code
    # subprocess.call(["code", "1.cpp"])
    webbrowser.open(url)


# Calling relevent functions
_contests = fetch_contests()
_total_problems = fetch_total_problems(_contests)
_problems_finished = fetch_user_solves()
_url = search(_total_problems, _problems_finished)
setup(_url)
