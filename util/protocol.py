from abc import ABCMeta, abstractmethod

import urlparse
import json

class Protocol:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def encode(self, data):
        pass

    @abstractmethod
    def decode(self, data):
        pass


class QueryStringProtocol(Protocol):
    def __init__(self):
        super(QueryStringProtocol, self).__init__()
    
    def encode(self, data):
        qs = ""
        for key in data.keys():
            value = data[key]
            qs = qs + key + "=" + str(value) + "&"
        return qs

    def decode(self, data):
        dictionary = urlparse.parse_qs(data)
        for key in dictionary.keys():
            value = dictionary[key]
            dictionary[key] = value[0]
        return dictionary

class JSONQueryStringProtocol(Protocol):
    def __init__(self):
        super(JSONQueryStringProtocol, self).__init__()
    
    def encode(self, data):
        qs = "data=" + json.dumps(data)
        return qs

    def decode(self, data):
        dictionary = urlparse.parse_qs(data)
        qs_data = dictionary["data"]
        d = json.loads(qs_data[0])
        return d

if __name__ == '__main__':
    qsProtocol = JSONQueryStringProtocol()
    data = {"Name": "Linus", "Age": 37, "Gender": "Male", "Adult": True}
    print(data)
    qs = qsProtocol.encode(data)
    print(qs)
    data2 = qsProtocol.decode(qs)
    print(data2)
