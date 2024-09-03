from skrap.config import Config
from skrap.skrap import Skrap
import json

config = Config.from_json('conf/ebay_1.json')

skrap = Skrap(config)

def callback(el, data):
    print(el)
    print(el.attrib)
    print(json.dumps(data, indent=4))

data = skrap.skrap(callback=callback)
print(json.dumps(data, indent=4))





