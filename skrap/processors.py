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

    def __init__(self, loader: BaseLoader,  config: Config, parse_method=None):
        self.config = config
        self.loader = loader
        if parse_method:
            self.parse_method = parse_method
        else:
            self.parse_method = self.default_parse

    def default_parse(self, element: HtmlElement):
        return element.text_content().replace('\n', '').replace('\r', '').strip()

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
                    if node.xpath:
                        lst = element.xpath(node.xpath)
                    else:
                        lst = [element]

                    if lst:
                        el = lst[0]
                        if isinstance(el, HtmlElement):
                            partial[node.name] = self.parse_method(el)


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