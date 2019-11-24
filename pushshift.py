import requests
import json
import random

difficulty = 'easy'     # or intermediate or hard

json_string = requests.get(r'https://api.pushshift.io/reddit/search/submission/?subreddit=dailyprogrammer&title=' + difficulty + r'%20challenge&size=500').text

data = json.JSONDecoder().decode(json_string)['data']

res_len = len(data)

index = random.randrange(0, res_len)

target = data[index]['id']

json_string = requests.get('https://api.pushshift.io/reddit/search/submission/?ids=' + target).text

data = json.JSONDecoder().decode(json_string)['data']

print(data[0])

# https://github.com/pushshift/api