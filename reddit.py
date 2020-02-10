import requests
import config
import time

from dota_responses import *
url_a = "https://www.reddit.com/"
url_auth = "https://oauth.reddit.com/"


def get_access_token_object():
    try:
        res = requests.post(url_a+"api/v1/access_token", headers = {'User-Agent':'bot-script by shifu_bot'}, data={'grant_type':'password','username':config.username, 'password':config.password, 'scope': '*'}, auth=(config.id, config.secret))
        if res.status_code != 200:
            raise Exception(f"Error getting access token, status returned {res.status_code}")
        js = res.json()
        return js
    except Exception as e:
        print(e)

def get_private_messages(token_object, last_id= None):
    try:
        token_object = get_access_token_object()
        access_token = token_object['access_token']
        token_type = token_object['token_type']
        
        res = requests.get(url_auth+"message/inbox", headers = {'User-Agent': 'bot-script by shifu_bot', 'Authorization': token_type.capitalize()+" "+access_token },params = {'before': last_id})

        if res.status_code != 200:
            raise Exception(f"Error getting messages, status returned {res.status_code}")
        return res.json()['data']['children']
    except Exception as e:
        print(e)

def reply_to_private_messages(token_object, message_list, last_id):
    try:
        token_object = get_access_token_object()
        access_token = token_object['access_token']
        token_type = token_object['token_type']
        last_id = message_list[0]['kind']+"_"+message_list[0]['data']['id']
        for children in message_list:
            data = children['data']
            fullname= children['kind']+"_"+data['id']
            body = data['body']
            author = data['author']
            message = f"Hello {author}. This is a reply to your message containing the following: {body}. Thank you for messaging me. I am a bot under construction. My master says hello."
            
            res = requests.post(url_auth+"api/comment", headers = {'User-Agent': 'bot-script by shifu_bot', 'Authorization': token_type.capitalize()+" "+access_token}, data = {'api_type': 'json', 'text': message, 'thing_id': fullname})
            if res.status_code != 200:
                raise Exception(f"Error sending messages, response returned {res.json()}")   
            

        return last_id

    except Exception as e:
        print(e)

token_object = get_access_token_object()
start = time.time()
try:
    f = open("last_id.txt", "r")
    last_id = f.readline().strip('\n')
except:
    last_id = None   
finally:
    f.close()
timeout  = 1

while True:
    try:
        
        current = time.time()
        if current - start >= token_object['expires_in']:
            token_object = get_access_token_object()
            start = time.time()
            print("Token Renewed")
        message_list = get_private_messages(token_object, last_id)
        if len(message_list) > 0:
            print("Message List Fetched...Replying...")
            last_id = reply_to_private_messages(token_object, message_list, last_id)
            print(f"Replied until id {last_id} ")
        time.sleep(timeout*60)
    except KeyboardInterrupt:
        with open("last_id.txt","w") as f:
            f.write(last_id+"\n")
        break
    except Exception as e:
        print(e)
        


