import typing
import praw
import argparse

reddit = praw.Reddit('bot1', user_agent='testscript by /u/css436program5')

difficulties = ['Easy', 'Intermediate', 'Hard']

def getSubmission(difficulty: str):
    def getRandomSubmission():
        aRandomSubmission = reddit.subreddit('dailyprogrammer').random()
        while 'Challenge' not in aRandomSubmission.title:
            aRandomSubmission = reddit.subreddit('dailyprogrammer').random()
        return aRandomSubmission

    if difficulty not in difficulties:
        return getRandomSubmission()
    else:
        candidate = getRandomSubmission()
        while difficulty not in candidate.title:
            candidate = getRandomSubmission()
        return candidate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose your difficulty.')
    parser.add_argument('--difficulty', action='store', dest='difficulty')

    result = parser.parse_args()
    difficulty = result.difficulty

    submission = getSubmission(difficulty)
    print(submission.title)