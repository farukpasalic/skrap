from abc import ABC, abstractmethod
from typing import List

from lxml.html import HtmlElement
from skrap.config import Config, Node
from skrap.loader import BaseLoader

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, element: HtmlElement):
        pass


class SingleProcessor(BaseProcessor):

    def __init__(self, loader: BaseLoader,  config: Config):
        self.config = config
        self.loader = loader

    def process(self, callback=None):

        html = self.loader.process(self.config.url)
        element = html.xpath(self.config.root_xpath)

        data = {}
        for node in self.config.nodes:
            lst = element[0].xpath(node.xpath)
            if lst:
                el = lst[0]
                if isinstance(el, HtmlElement):
                    data[node.name] = lst[0].text_content().replace('\n', '').replace('\r', '').strip()
                else:
                    data[node.name] = el.replace('\n', '').replace('\r', '').strip()
        if callback:
            callback(data)
        return data


class ListProcessor(BaseProcessor):

    def __init__(self, loader: BaseLoader,  config: Config):
        self.config = config
        self.loader = loader

    def process(self, callback=None):

        data = []
        next_element = None
        url = self.config.url

        while True:
            if self.config.limit is not None and len(data) > self.config.limit:
                break

            html = self.loader.process(url)
            element = html.xpath(self.config.root_xpath)

            for e in element:
                partial = {}
                for n in self.config.nodes:
                    lst = e.xpath(n.xpath)
                    if lst:
                        el = lst[0]
                        if isinstance(el, HtmlElement):
                            partial[n.name] = lst[0].text_content().replace('\n', '').replace('\r', '').strip()
                        else:
                            partial[n.name] = el.replace('\n', '').replace('\r', '').strip()


                    data.append(partial)

                if callback:
                    callback(partial)

            if self.config.next:
                next_element = html.xpath(self.config.next)
                if next_element is not None:
                    url = None
                    if len(next_element) > 0:
                        url = next_element[0]
                if next_element is None:
                    break
            else:
                break

        self.loader.quit()
        return data[:self.config.limit]