import requests
import config

from dota import dota_responses
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

def get_private_messages(last_id= None):
    try:
        token_object = get_access_token_object()
        access_token = token_object['access_token']
        token_type = token_object['token_type']
        
        res = requests.get(url_auth+"message/inbox", headers = {'User-Agent': 'bot-script by shifu_bot', 'Authorization': token_type.capitalize()+" "+access_token },params = {'before': last_id})

        if res.status_code != 200:
            raise Exception(f"Error getting messages, status returned {res.status_code}")
        
        for children in res.json()['data']['children']:
            data = children['data']
            fullname= children['kind']+"_"+data['id']
            body = data['body']
            author = data['author']
            message = f" Hello {author}, This is bot. This is an automated reply. You wrote : {body}"
            last_id = fullname
            res = requests.post(url_auth+"api/comment", headers = {'User-Agent': 'bot-script by shifu_bot', 'Authorization': token_type.capitalize()+" "+access_token}, data = {'api_type': 'json', 'text': message, 'thing_id': fullname})
            if res.status_code != 200:
                raise Exception(f"Error sending messages, response returned {res.json()}")   
            

        return last_id

    except Exception as e:
        print(e)


