from flask import Flask, render_template
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
    print(data + title)


    return render_template("displayproblem.html", context=data_with_br, title=title_with_br)

   
    

@app.route("/generate", methods=['POST'])
def generate():
    return "index.html"

@app.route("/subscribe", methods=['POST'])
def subscribe():
    return "index.html"



if __name__ == '__main__':
    data = pushshift.return_random_problem()
    print(type(data))
    application.run(debug=True, port=5001)
    
