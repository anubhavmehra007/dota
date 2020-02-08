import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import pickle
from urllib.parse import quote
url = "https://dota2.gamepedia.com/"
def get_hero_list():
    first_hero = '/Abaddon'
    last_hero = '/Zeus'
    try:
        res = requests.get(url+'Heroes')
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            links = soup.find_all('a')
            hrefs = [link.get('href') for link in links if not (link.get('href') == '/Intelligence' or link.get('href') == '/Agility')]
            heroes = hrefs[hrefs.index(first_hero):hrefs.index(last_hero)+1]
            heroes = [hero[1:] for hero in heroes]
            return heroes

        else:
            raise Exception("Some error came in fetching hero list")
    except Exception as e:
        print(str(e))

def prepare_response_from_text(text):
    text = [c for c in text if ord(c) < 255]
    text = ''.join(text)          
    while text.startswith('Link'):
        text = text.strip(' Link')
    tests = ['u' , 'r ']
    for i in range(30, 301, 30):
        tests.append(str(i)+' ')
    for test in tests:
        if text.startswith(test):
            text = text.strip(test)

    return text

def get_hero_response(hero):
    try:
        res = requests.get(url+hero+'/Responses')
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            links = soup.find_all('li')
            responses_link = [link for link in links if len(link.find_all('audio')) > 0]
            responses = {}
            for link in responses_link:
                text = prepare_response_from_text(link.get_text())
                
                responses[text] = [a.get('href') for a in link.find_all('a') if a.get('href') != None and '.mp3' in a.get('href')]
            
            return responses
        else:
            raise Exception(f"Error in fetching respose urls for Hero {hero}")
    except Exception as e:
        print(e)

def download_resonse_mp3(response):
    try:
        
        name = response.split('/')[-1]
        res = requests.get(response)
        if res.status_code == 200:
            with open(name, 'wb') as f:
                f.write(res.content)
        else:
            raise Exception(f"Error in fetching data for reposnse {response}")
    except Exception as e:
        print(str(e))


def return_response_media_url(hero, response):
    for k,v in get_hero_response(hero).items():
        if k ==  response:
            return v[0]
    return 'Not Found'
        

def beautify_hero_name(hero):
    hero = unquote(hero)
    if '_' in hero:
        hero = hero.split('_')
        hero = ' '.join(hero)
    return hero

def make_all_data():
    dota = []
    for hero in get_hero_list():
        hero_name = beautify_hero_name(hero)
        response = get_hero_response(hero)
        hero_data = {'name': hero_name, 'response_data':response}
        dota.append(hero_data)
    return dota

def encode_hero_name(hero):
    if " " in hero:
        hero = hero.split(" ")
        hero ="_".join(hero)
    hero = quote(hero)
    return hero

def make_data_file():
    with open('dota.dat', 'wb') as f:
        pickle.dump(make_all_data(),f)

    print("Data File Saved")

def load_data_file(filname):
    with open(filename) as f:
        dota = pickle.load(f)
    return dota



    
    
