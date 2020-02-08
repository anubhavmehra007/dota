from dota_responses import *


li = get_hero_list()

li2 = [beautify_hero_name(hero) for hero in li]
li2 = [hero.upper() for hero in li2]
li2 = [encode_hero_name(hero) for hero in li2]
for i in range(0,len(li)):
    if li[i] != li2[i]:
        print(f"{li[i]}   {li2[i]}")