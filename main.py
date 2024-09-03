from skrap.config import Config
from skrap.skrap import Skrap
import json

config = Config.from_json('conf/example1_article.json')

skrap = Skrap(config)

def callback(data):
    print(json.dumps(data, indent=4))

skrap.skrap(callback=callback)





