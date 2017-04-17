import argparse
import urllib2
#import urllib.request

class HTTPQuery:
    def __init__(self):
        pass
    
    def query(self, myurl):
        proxy_support = urllib2.ProxyHandler({})
        opener = urllib2.build_opener(proxy_support)
        
        response_code = -1
        response = "Error"
        
        try:
            conn = opener.open(myurl)
            response_code = conn.getcode()
            response = conn.read()
        except urllib2.HTTPError, err:
            response_code = err.code
            response = "Error"
        except urllib2.URLError, err:
            response_code = -1
            response = err.reason
            
        return response, response_code 
    
if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description="Run commands")
    parser.add_argument('-q', '--query', default=False, action="store_true",
                        help="Query server")
    parser.add_argument('-host', '--host', type=str, default="localhost",
                        help="Host")
    parser.add_argument('-p', '--port', default=8000, type=int,
                        help="Port")
    parser.add_argument('-protocol', '--protocol', type=str, default="http",
                        help="Protocol")
    parser.add_argument('-page', '--page', type=str, default="index.html",
                        help="Page")
    parser.add_argument('-qs', '--query-string', type=str, default="",
                        help="Query string")
    args = parser.parse_args()
        
    if args.query == True:
        myurl = args.protocol + "://" + args.host + ":" + str(args.port) + "/" + args.page + "?" + args.query_string
        client = DDBMModelClientHandler()
        response, response_code = client.query(myurl)
        print(response_code)
        print(response)
    
