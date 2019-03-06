from result.json import JsonCommandSink
from typing import Dict, List
from uuid import uuid4
from collections import OrderedDict
import json


class WebResult(object):

    def __init__(self, operation: str):
        self.operation = operation
        self.sink = JsonCommandSink()
        self.key = str(uuid4())

    def render(self) -> str:
        content = self.sink.container
        rendered = self.render_object(content)
        return rendered

    def render_object(self, content: OrderedDict) -> str:
        result = '<div>'
        for name, item in content.items():
            if isinstance(item, OrderedDict):
                result += '<pre>' + name + '</pre>'
                result += '<div class="children">' + self.render_object(item) + '</div>'
            elif isinstance(item, list):
                result += '<pre>' + name + '</pre>'
                result += '<div class="children">' + self.render_list(item) + '</div>'
            else:
                result += '<pre>' + name + ': ' + item + '</pre>'
        return result + '</div>'

    def render_list(self, item_list: List[str]) -> str:
        result = ''
        for item in item_list:
            result += '<pre>' + item + '</pre>'
        return result

    def as_json(self) -> str:
        return json.dumps(self.sink.container, indent=4, sort_keys=False)


_results: Dict[str, WebResult] = {}


def next_result(operation: str) -> WebResult:
    result = WebResult(operation)
    _results[result.key] = result
    return result


def get_result(key: str) -> WebResult:
    return _results[key]
