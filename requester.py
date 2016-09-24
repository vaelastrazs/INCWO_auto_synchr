from __future__ import print_function 

import requests

class Requester(Thread):
    
    method = None
    url = None
    xml = None
    
    """ Thread principale pour mettre a jour le catalogue incwo"""

    def __init__(self, method, url, xml):
        Thread.__init__(self)
        self.method = method
        self.url = url
        self.xml = xml

    def run(self):
        r = None
        headers = {'content-type': 'application/xml'}
        if self.method == "get":
            r = requests.get(url, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
        elif self.method == "post":
            r = requests.post(url, data=xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
        elif self.method == "put":
            r = requests.put(url, data=xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
        elif self.method == "delete":
            r = requests.delete(url, data=xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
        if r != None:
            if r.status_code != 200:
                print(r.text)