from script import *
import numpy as np
import random


def get_all_tags(total_problems, problems_finished):
    """
    For all the problems in problemset, get their tags.
    """
    tags = []
    for problem in total_problems+problems_finished:
        tags = tags+problem['tags']
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
        for tag in problem['tags']:
            freq[tag] += 1
    for problem in problems_finished[:top_prob]:
        for tag in problem['tags']:
            freq[tag] += len(problems_finished)//10
    freq = {k: v-min(list(freq.values()))+1 for k, v in freq.items()}
    score = {k: sum(list(freq.values()))/v for k, v in freq.items()}
    unsolved_problems = []
    for problem in total_problems:
        if problem in problems_finished:
            continue
        problem['score'] = 0
        for tag in problem['tags']:
            problem['score'] += score[tag]
        unsolved_problems.append(problem)
    return unsolved_problems


def personalised_search(total_problems, problems_finished):
    """
    Get a problem personalised to a user.
    """
    unsolved_problems = get_unsolved_problems(
        total_problems, problems_finished)
    if len(unsolved_problems) > 0:
        problem = random.choices(
            unsolved_problems,
            weights=[prob['score'] for prob in unsolved_problems],
            k=1
        )[0]
        url = 'https://codeforces.com/contest/' + \
            str(problem['contestId'])+'/problem/'+problem['index']
        name = "Suggested Problem: "+problem['name']
        link = "Link: "+url
        progress = "Current Progress: " + \
            str(len(total_problems) - len(unsolved_problems)) + \
            '/'+str(len(total_problems)) + ' Problems'
        return name, link, progress, url
    else:
        print("\nAll problems from this range have been completed!\n")
        return None, None, None, None


if __name__ == "__main__":
    # Set parameters
    handle = "menavlikar.rutvij"
    min_rating = 2100
    max_rating = 2100

    contests = fetch_contests()
    total_problems = fetch_total_problems(contests, min_rating, max_rating)
    problems_finished = fetch_user_solves(handle)
    name, link, progress, url = personalised_search(
        total_problems, problems_finished)
    print(name)
    print(link)
    print(progress)
