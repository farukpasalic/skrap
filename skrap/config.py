import json
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    name: str
    xpath: str

@dataclass
class Config:
    url: str
    root_xpath: str
    processor: str
    limit: int
    next: str
    nodes: List[Node]
    node: Node = None

    @staticmethod
    def from_json(file_path):
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        nodes_data = data.pop('nodes', [])
        nodes = [Node(**node_data) for node_data in nodes_data]
        node_data = data.pop('node', None)
        node = Node(**node_data) if node_data else None
        next_data = data.pop('next', None)  # Handle the case where 'next' might not be present
        return Config(nodes=nodes, node=node, next=next_data, **data)