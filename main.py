from skrap.config import Config
from skrap.skrap import Skrap, SeleniumLoader
import json

#config = Config.from_json('conf/example1_article.json')
#config = Config.from_json('conf/example2_wiki_table.json')
#config = Config.from_json('conf/example3_link_list.json')
#config = Config.from_json('conf/example4_google.json')

config = Config.from_json('conf/scrum_guide.json')

loader = SeleniumLoader(driver_path=r"C:\Users\User\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

skrap = Skrap(config, loader=loader)

c = 0
def callback(data):
    global c
    print(json.dumps(data, indent=4))
    c += 1
    print(f"C: {c}")


data = skrap.skrap(callback=callback)
print("-------------------------------------------------------------------------------")
print(json.dumps(data, indent=4))
print(len(data))




