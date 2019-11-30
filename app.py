from flask import Flask, render_template, request
import boto3
import pushshift
import html



application = app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/random", methods=['POST'])
def random():
    returned_data = pushshift.return_random_problem()
    data = html.unescape(returned_data['selftext'])
    data_with_br = data.replace("\n", "<br />")
    title = returned_data['title'] + '\n' 
    title_with_br = title.replace("\n", "<br />")
    #print(data + title)


    return render_template("displayproblem.html", context=data_with_br, title=title_with_br)

   
    

@app.route("/generate", methods=['POST'])
def generate():
    difficulty_type = request.form["difficulty"]
    print(difficulty_type)
    difficulty_type_data = pushshift.difficulty_specified_problem(difficulty_type)
    print(difficulty_type_data)
    returned_difficulty_type_data = html.unescape(difficulty_type_data['selftext'])
    returned_difficulty_type_data = returned_difficulty_type_data.replace("\n", "<br />")
    title_type_with_br = difficulty_type_data['title'] + '\n' 
    title_type_with_br = title_type_with_br.replace("\n", "<br />")

    return render_template("displayproblem.html", context_two=returned_difficulty_type_data, title_two=title_type_with_br)

@app.route("/subscribe", methods=['POST'])
def subscribe():
    return "index.html"



if __name__ == '__main__':
    data = pushshift.return_random_problem()
    print(type(data))
    application.run(debug=True, port=5001)
    
