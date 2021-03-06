__author__ = 'neha'

import json, urllib2

portfolio = "55c4532650eb684e072a2335"

payload = {
    "type" : "creatives",
    "command" : "create-new-portfolio",
    "data" : {
        "title" : "Bits of Bombay",
        "owner" : "55b3e5485301fb1fea825909",
        "description" : "Images of the city that always moves.",
        "category" : ["Photography"],
        "sub-category" : ["Art Direction"],
        "tags" : ["Art", "Illustration", "Portrait", "Photo"]
    }
}

payload2 = {
    "node" : portfolio,
    "type" : "creatives",
    "command" : "update-portfolio",
    "data" : {
        "title" : "B.i.t.s of Bombay",
        "description" : "Images of the city that always moves and never sleeps."
    }
}

payload3 = {
    "node" : portfolio,
    "type" : "creatives",
    "command" : "update-category",
    "action" : "remove",
    "data" : {
        "category" : "Architectural Photography"
    }
}

payload4 = {
    "node" : portfolio,
    "type" : "creatives",
    "command" : "update-sub-category",
    "action" : "add",
    "data" : {
        "subcategory" : "Black and White Photography"
    }
}

payload5 = {
    "node" : portfolio,
    "type" : "creatives",
    "command" : "update-tags",
    "action" : "remove",
    "data" : {
        "tag" : "Illustration"
    }
}



url = "http://localhost:4900/editors/invoke"

request = urllib2.Request(url)
request.add_header('Content-type', 'application/json')
response = urllib2.urlopen(request, json.dumps(payload5))

print str(json.load(response))
