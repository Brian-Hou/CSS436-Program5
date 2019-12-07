from flask import Flask, render_template, request
from botocore.errorfactory import ClientError
from boto3.dynamodb.conditions import Key, Attr
import boto3
import pushshift
import html



application = Flask(__name__)

AWS_REGION = "us-west-2"
table_name = "program5_email_table"
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
dynamo_table = dynamodb.Table(table_name)
client = boto3.client('ses',region_name=AWS_REGION)



list_of_email_recipients = []




def send_verification_email(email):
    client.verify_email_identity(
    EmailAddress=email
    )

def check_if_verified(email):
    response = client.list_verified_email_addresses()
    for identity in response['VerifiedEmailAddresses']:
        if identity == email:
            return True
    return False

    #  response = client.list_identities(
    # IdentityType='EmailAddress',
    # MaxItems=150
    # )
    # for identity in response['Identities']:
    #     if identity == email:
    #         return True
    # return False






# Creates the DynamoDB table if not already created
def create_dynamodb_table():


    params = {
        'TableName': table_name,
        'KeySchema': [
            {'AttributeName': "emailAddress", 'KeyType': "HASH"},  # Partition key
        ],
        'AttributeDefinitions': [
            {'AttributeName': "emailAddress", 'AttributeType': "S"},
            

        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }


    try:


        table = dynamodb.create_table(**params)

        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

        return table



    except:


        table = dynamodb.Table(table_name)
        return table
        pass


@application.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@application.route("/random", methods=['POST'])
def random():
    returned_data = pushshift.return_random_problem()
    data = html.unescape(returned_data['selftext'])
    data = pushshift.markdown_to_html(data)

    title = returned_data['title'] + '\n' 
    title_with_br = title.replace("\n", "<br />")

   

    return render_template("displayproblem.html", context=data, title=title_with_br)
   
    

@application.route("/generate", methods=['POST'])
def generate():
    difficulty_type = request.form["difficulty"]
    print(difficulty_type)
    difficulty_type_data = pushshift.difficulty_specified_problem(difficulty_type)
    print(difficulty_type_data)
    returned_difficulty_type_data = html.unescape(difficulty_type_data['selftext'])
    returned_difficulty_type_data = pushshift.markdown_to_html(returned_difficulty_type_data)

    
    title_type_with_br = difficulty_type_data['title'] + '\n' 
    title_type_with_br = title_type_with_br.replace("\n", "<br />")

    return render_template("displayproblem.html", context_two=returned_difficulty_type_data, title_two=title_type_with_br)

@application.route("/subscribe", methods=['POST'])
def subscribe():
    email_address = request.form["email"]
    print(email_address)
    dynamodb_table = create_dynamodb_table()

   
    response = dynamo_table.query(
        TableName=table_name,
        KeyConditionExpression=Key('emailAddress').eq(email_address)
    )

    Item = {}
    items = response['Items']
    if not items:
        Item["is_email_verified"] = False
        send_verification_email(email_address)
    
    if check_if_verified(email_address):
        Item['is_email_verified'] = True

    Item['emailAddress'] = email_address
    
    
    
    dynamodb_table.put_item(
                Item={**Item}
            )
    


    return render_template("index.html")

@application.route("/email", methods=['POST'])
def send_emails_to_subscribers():
    SENDER = "Brian Hou and Kevin Hsu <bhou@uw.edu>"
    SUBJECT = "CSS436 Program5 Daily Reddit Programming Link"
    CHARSET = "UTF-8"


    BODY_TEXT = ("Go to the following link <CSS436Program5.us-west-2.elasticbeanstalk.com> to access your daily programming practice problems!"
            )
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Daily Programming Link</h1>
    <p> Hello! Click on the following link to access your daily programming practice problems!
        <a href='CSS436Program5.us-west-2.elasticbeanstalk.com'>Link to Daily Programming Practice</a> 
    </p>
    </body>
    </html>
                """ 

    response = dynamo_table.scan()
    Item = {}
    for i in response['Items']:
        if check_if_verified(i['emailAddress']):
            response = dynamo_table.query(
            TableName=table_name,
            KeyConditionExpression=Key('emailAddress').eq(i['emailAddress'])
            )
            if response:
                Item['emailAddress'] = i['emailAddress']
                Item['is_verified_email'] = True
                dynamodb.Table(table_name).put_item(
                Item={**Item}
                )
            list_of_email_recipients.append(i['emailAddress'])
    
    for email in list_of_email_recipients:
        RECIPIENT = email
        
        

        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    
        
    return render_template("index.html")


if __name__ == '__main__':

    application.run(debug=True)
    
    
