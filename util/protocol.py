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
        return data

class JSONQueryStringProtocol(Protocol):
    def __init__(self):
        super(JSONQueryStringProtocol, self).__init__()
        self.label = "json"
    
    def encode(self, data):
        qs = self.label + '=' + json.dumps(data)
        qs = qs.replace (" ","%20")
        qs = qs.replace ('"',"%22")
        return qs

    def decode(self, data):
        dictionary = urlparse.parse_qs(data)
        qs_data = dictionary.get(self.label)
        ret = {}
        if qs_data is not None:
           if len(qs_data) > 0:
               str_val = qs_data[0]
               ret = json.loads(str_val)
        return ret

if __name__ == '__main__':
    qsProtocol = JSONQueryStringProtocol()
    data = {"Name": "Linus", "Age": 37, "Gender": "Male", "Adult": True}
    print(data)
    qs = qsProtocol.encode(data)
    print(qs)
    data2 = qsProtocol.decode(qs)
    print(data2)
