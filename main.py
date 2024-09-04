from skrap.config import Config
from skrap.skrap import Skrap, SeleniumLoader
import json
from lxml import html as H

#config = Config.from_json('conf/example1_article.json')
#config = Config.from_json('conf/example2_wiki_table.json')
#config = Config.from_json('conf/example3_link_list.json')
#config = Config.from_json('conf/example4_google.json')

config = Config.from_json('conf/scrum_guide.json')

loader = SeleniumLoader(driver_path=r"C:\Users\User\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

def collect_attribs(element):
    all_classes = []
    all_attribs = {}

    # Collect attributes of the current element
    all_classes.extend(element.classes)
    all_attribs.update(dict(element.attrib))

    # Recursively collect attributes of child elements
    for child in element.iterchildren():
        ac, aa = collect_attribs(child)
        all_classes.extend(ac)
        all_attribs.update(aa)


    return all_classes, all_attribs
def parse(element):

    if isinstance(element, str):
        element = [H.fromstring("<p>" + element + "</p>")]

    txt = element.text_content().replace('\n', '').replace('\r', '').strip()
    all_classes, all_attribs = collect_attribs(element)
    return {
        'text': txt,
        'classes': all_classes,
        'attribs': all_attribs,
        'tag': element.tag
    }

skrap = Skrap(config, loader=loader)

c = 0
def callback(data):
    global c
    print(json.dumps(data, indent=4))
    c += 1
    print(f"C: {c}")


skrap.skrap(callback=callback)





