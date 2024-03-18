import random
import sys
import webbrowser

import requests

# import subprocess

# Scraping Functions


def fetch_contests():
    """
    Returns list of contest IDs from which problems are to be picked
    """
    data = requests.get("https://codeforces.com/api/contest.list").json()
    contests = []
    for i in data["result"]:
        if "ducational" in i["name"]:
            contests.append(i["id"])
        if "ICPC" in i["name"] and "otlin" not in i["name"]:
            contests.append(i["id"])
    return contests


def fetch_total_problems(contests, min_rating, max_rating):
    """
    Returns desirable problems in sorted order
    """
    data = requests.get("https://codeforces.com/api/problemset.problems").json()
    total_problems = []
    for i in data["result"]["problems"]:
        if i["contestId"] in contests:
            try:
                if i["rating"] >= min_rating and i["rating"] <= max_rating:
                    total_problems.append(i)
            except:
                pass
    total_problems.reverse()
    total_problems.sort(key=lambda x: x["rating"])
    return total_problems


def fetch_user_solves(handle):
    """
    Return problems already solved by the user
    """
    problems_finished = []
    data = requests.get(
        "https://codeforces.com/api/user.status?handle=" + handle
    ).json()
    try:
        for i in data["result"]:
            if i["verdict"] == "OK":
                problems_finished.append(i["problem"])
    except:
        pass
    return problems_finished


# Pre-processing Functions


def get_all_tags(total_problems, problems_finished):
    """
    For all the problems in problemset, get their tags.
    """
    tags = []
    for problem in total_problems + problems_finished:
        tags = tags + problem["tags"]
    tags = list(set(tags))
    return tags


def get_unsolved_problems(total_problems, problems_finished, top_prob=5):
    """
    Get all the unsolved problems with their selection score updated.
    """
    tags = get_all_tags(total_problems, problems_finished)
    freq = {}
    for tag in tags:
        freq[tag] = 0
    for problem in problems_finished:
        for tag in problem["tags"]:
            freq[tag] += 1
    for problem in problems_finished[:top_prob]:
        for tag in problem["tags"]:
            freq[tag] += (
                len(problems_finished) // 10
            )  # Increase frequency of tags of recently solved problems to be selected less often
    freq = {
        k: v - min(list(freq.values())) + 1 for k, v in freq.items()
    }  # Normalise the frequency of tags
    score = {
        k: sum(list(freq.values())) / v for k, v in freq.items()
    }  # Calculate the selection score of each tag
    unsolved_problems = []
    for problem in total_problems:
        if problem in problems_finished:
            continue
        problem["score"] = 0
        for tag in problem["tags"]:
            problem["score"] += score[
                tag
            ]  # Add the selection score of each tag to calculate the problem score
        unsolved_problems.append(problem)
    return unsolved_problems


# Main Search Function


def personalised_search(total_problems, problems_finished):
    """
    Get a problem personalised to a user.
    """
    unsolved_problems = get_unsolved_problems(total_problems, problems_finished)
    if len(unsolved_problems) > 0:
        problem = random.choices(
            unsolved_problems,
            weights=[prob["score"] for prob in unsolved_problems],
            k=1,
        )[
            0
        ]  # Select a problem randomly based on its score
        url = (
            "https://codeforces.com/contest/"
            + str(problem["contestId"])
            + "/problem/"
            + problem["index"]
        )
        name = "Suggested Problem: " + problem["name"]
        link = "Link: " + url
        progress = (
            "Current Progress: "
            + str(len(total_problems) - len(unsolved_problems))
            + "/"
            + str(len(total_problems))
            + " Problems"
        )
        return name, link, progress, url
    else:
        print("\nAll problems from this range have been completed!\n")
        return None, None, None, None


if __name__ == "__main__":
    # Set parameters
    handle = None
    min_rating = None
    max_rating = None
    for i in range(1, len(sys.argv) - 1):
        if sys.argv[i] == "-handle":
            handle = sys.argv[i + 1]
        elif sys.argv[i] == "-min":
            min_rating = int(sys.argv[i + 1])
        elif sys.argv[i] == "-max":
            max_rating = int(sys.argv[i + 1])
        elif (
            sys.argv[i] == handle
            or (min_rating is not None and sys.argv[i] == str(min_rating))
            or (max_rating is not None and sys.argv[i] == str(max_rating))
        ):
            continue
        else:
            print(
                "Usage: python3 personalised.py -handle <handle> -min <min_rating> -max <max_rating>"
            )
            raise SystemExit
    if handle is None or min_rating is None or max_rating is None:
        print(
            "Usage: python3 personalised.py -handle <handle> -min <min_rating> -max <max_rating>"
        )
        raise SystemExit

    contests = fetch_contests()
    total_problems = fetch_total_problems(contests, min_rating, max_rating)
    problems_finished = fetch_user_solves(handle)
    name, link, progress, url = personalised_search(total_problems, problems_finished)
    print(name)
    print(link)
    print(progress)
    if url is not None:
        webbrowser.open(url)
