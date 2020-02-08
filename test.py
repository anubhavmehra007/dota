from dota_responses import *

name = encode_hero_name("earthshaker")
response = get_hero_response(name)
url = return_response_media_url(name, 'Who gave you permission to prance across the earth?')
download_resonse_mp3(url)