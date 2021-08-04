import requests
import webbrowser
import subprocess

# Set parameters
handle = "tourist"
min_rating = 1800
max_rating = 1900


# Returns list of contestIDs from which questions are to be picked
def fetch_contests():
    data = requests.get("https://codeforces.com/api/contest.list").json()
    contests = []
    for i in data['result']:
        if "ducational" in i['name']:
            contests.append(i['id'])
        if "ICPC" in i['name']:
            contests.append(i['id'])
    return contests


# Returns desirable questions in sorted order
def fetch_total_questions(contests):
    data = requests.get(
        "https://codeforces.com/api/problemset.problems").json()
    total_questions = []
    for i in data['result']['problems']:
        if i['contestId'] in contests:
            try:
                if i['rating'] >= min_rating and i['rating'] <= max_rating:
                    total_questions.append(i)
            except:
                pass
    total_questions.sort(key=lambda x: x["rating"])
    return total_questions


# Return questions already solved by the user
def fetch_user_solves():
    questions_finished = []
    data = requests.get(
        "https://codeforces.com/api/user.status?handle="+handle).json()
    for i in data['result']:
        if i['verdict'] == "OK":
            questions_finished.append(i['problem'])
    return questions_finished


# Search and print the most relevant question
def search(total_questions, questions_finished):
    found_status = False
    todo = None
    done = 0
    for i in total_questions:
        if i in questions_finished:
            done += 1
        elif found_status is False:
            todo = i
            found_status = True
    url = 'https://codeforces.com/contest/' + \
        str(todo['contestId'])+'/problem/'+todo['index']
    print("\nSuggested Problem: "+todo['name'])
    print("Link: "+url)
    print("Current Progress: "+str(done)+'/' +
          str(len(total_questions))+' Questions\n')
    return url


# Launches cpp file with template code and opens the question found in browser
def setup(url):
    # uncomment if you wish to open 1.cpp in vs code
    # subprocess.call(["code", "1.cpp"])
    webbrowser.open(url)


# Calling relevent functions
_contests = fetch_contests()
_total_questions = fetch_total_questions(_contests)
_questions_finished = fetch_user_solves()
_url = search(_total_questions, _questions_finished)
setup(_url)
