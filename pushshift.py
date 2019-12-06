import requests
import json
import random
import html

def return_random_problem():
    difficulty = ['easy', 'medium', 'hard']

    difficulty_len = len(difficulty)

    random_index = random.randrange(0, difficulty_len)

    difficulty_type = difficulty[random_index]

    json_string = requests.get(r'https://api.pushshift.io/reddit/search/submission/?subreddit=dailyprogrammer&title=' + difficulty_type + r'%20challenge&size=500').text

    data = json.JSONDecoder().decode(json_string)['data']

    res_len = len(data)

    index = random.randrange(0, res_len)

    target = data[index]['id']

    json_string = requests.get('https://api.pushshift.io/reddit/search/submission/?ids=' + target).text

    data = json.JSONDecoder().decode(json_string)['data'][0]
    
    return data

    #return data['title'] + '\n' + html.unescape(data['selftext'])

def difficulty_specified_problem(difficulty_type):


    json_string = requests.get(r'https://api.pushshift.io/reddit/search/submission/?subreddit=dailyprogrammer&title=' + difficulty_type + r'%20challenge&size=500').text

    data = json.JSONDecoder().decode(json_string)['data']

    res_len = len(data)

    index = random.randrange(0, res_len)

    target = data[index]['id']

    json_string = requests.get('https://api.pushshift.io/reddit/search/submission/?ids=' + target).text

    data = json.JSONDecoder().decode(json_string)['data'][0]
    
    return data

    #return data['title'] + '\n' + html.unescape(data['selftext'])


def markdown_to_html(markdown_string):
    

    return requests.post('https://api.github.com/markdown', json={'text': markdown_string}).text



# difficulty = 'easy'     # or intermediate or hard

# json_string = requests.get(r'https://api.pushshift.io/reddit/search/submission/?subreddit=dailyprogrammer&title=' + difficulty + r'%20challenge&size=500').text

# data = json.JSONDecoder().decode(json_string)['data']

# res_len = len(data)

# index = random.randrange(0, res_len)

# target = data[index]['id']

# json_string = requests.get('https://api.pushshift.io/reddit/search/submission/?ids=' + target).text

# data = json.JSONDecoder().decode(json_string)['data'][0]

# print(data['title'] + '\n' + html.unescape(data['selftext']))

# # https://github.com/pushshift/api