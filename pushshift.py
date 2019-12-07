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

def get_code_result(code):
    data = {
        'client_secret': '65025ef64a001966832f0d5b0c48e5ee3c4eca99',
        'source': code,
        'lang': 'PYTHON'
    }
    result = requests.post('https://api.hackerearth.com/v3/code/run/', data=data).text
    result = json.JSONDecoder().decode(result)
    print(result)
    if 'run_status' in result:
        if 'status' in result['run_status'] and result['run_status']['status'] == 'CE':
            error = html.escape(result['compile_status']).replace('\n', '<br/>').replace(' ', '&nbsp')
            print(error)
            return error, 'Compiler error...'
        elif 'signal' in result['run_status'] and result['run_status']['signal'] == 'SIGKILL':
            return result['run_status']['output_html'], 'Timed out after 5 seconds...'
        elif 'stderr' in result['run_status'] and len(result['run_status']['stderr']) > 0:
            result_str = result['run_status']['output_html'] + '<br/><br/>'
            result_str += html.escape(result['run_status']['stderr']).replace('\n', '<br/>').replace(' ', '&nbsp')
            return result_str, 'Check stderr...'
        else:
            return result['run_status']['output_html'], 'Success'
    else:
        return '', 'Source code can\'t be empty...'

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