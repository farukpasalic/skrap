from skrap.config import Config, Node
from skrap.loader import HTMLLoader, SeleniumLoader
import time


class Skrap:
    def __init__(self, config: Config, loader=None):
        self.config = config
        self.url = config.url
        self.root_xpath = config.root_xpath
        self.processor_name = config.processor
        self.config_nodes = config.nodes
        self.html = None
        self.root = None

        self.processor = None
        self.loader = loader
        self.init_processors(config)

    def init_processors(self, config: Config):
        if self.processor_name == 'single':
            from skrap.processors import SingleProcessor
            self.processor = SingleProcessor(self.loader, config)
        if self.processor_name == 'list':
            from skrap.processors import ListProcessor
            self.processor = ListProcessor(self.loader, config)



    def skrap(self, callback=None):
        return self.processor.process(callback=callback)

    def test(self, xpa):
        tree = self.loader.process(self.url)
        xp_parts = xpa.split('/')
        xp_parts = xp_parts[1:]
        for i in range(1, len(xp_parts)):
            xp = '/' + '/'.join(xp_parts[:i+1])
            print(xp)
            if len(tree.xpath(xp)) > 0:
                print("Ok")
                print(tree.xpath(xp))
            else:
                print("Empty")
            time.sleep(0.01)
