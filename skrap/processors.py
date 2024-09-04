from abc import ABC, abstractmethod
from typing import List

from lxml.html import HtmlElement
from skrap.config import Config, Node
from skrap.loader import BaseLoader
from lxml import html as H

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
        cnt = 0;
        while True:

            html = self.loader.process(url)
            elements = html.xpath(self.config.root_xpath)
            results = {}

            for element in elements:
                results[element] = {}

            for element in results.keys():
                if isinstance(element, str):
                    print(f"Root element is a string: {element}")
                    continue

                partial = results[element]
                for node in self.config.nodes:
                    lst = element.xpath(node.xpath)

                    if isinstance(lst, str):
                        lst = [H.fromstring("<p>" + lst + "</p>")]

                    if lst:
                        el = lst[0]
                        if isinstance(el, HtmlElement):
                            partial[node.name] = el.text_content().replace('\n', '').replace('\r', '').strip()


                if (self.config.limit is None) or (self.config.limit is not None and cnt < self.config.limit):
                    if callback:
                        callback(partial)

                    data.append(partial)
                    cnt += 1

            if self.config.limit is not None and cnt >= self.config.limit:
                break


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
        return data[:cnt]