#encoding=utf-8

base = """
<!DOCTYPE html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"0>
    <title>Ejemplo WSGI</title>
    <style type="text/css" media="screen">
    body {
        margin-top: 1.0em;
        background-color: #fafafa;
        font-family: "Trebuchet MS", Helvetica, sans-serif;
        font-size: 3.5em;
        color: #444;
        margin: 0 auto;
        width: 700px;
    }
    </style>
</head>
<body>
    %(content)s
</body>
"""

from wsgiref.simple_server import make_server
from cgi import parse_qs
from uuid import uuid1
from datetime import datetime
import re, os


class Request(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

def echo(request):
    return request.GET['with'][0] + '\n'

def words(request, prefix):
    limit = request.GET['limit'] if 'limit' in request.GET else 10
    raw_results = os.popen("look %s"%prefix).readlines()[:limit]
    return ",\n".join([word.replace('\n','') for word in raw_results])

def application(environ, start_response): 
    
    #interpretamos el environ
    request = Request()
    request.update({
        'path'  : environ['PATH_INFO'],
        'method': environ['REQUEST_METHOD'],
        'accept': environ['HTTP_ACCEPT'] if 'HTTP_ACCEPT' in environ else 'text/html',
        'GET'   : parse_qs(environ['QUERY_STRING']) if environ['REQUEST_METHOD'] == 'GET' else {}
    })

    #reaccionamos a la ruta
    raw_response = ""
    if request.path == '/echo':
        raw_response = echo(request)
    elif re.match(r'/words/with/\w+', request.path):
        prefix = re.match(r'/words/with/(\w+)', request.path).group(1)
        raw_response = words(request, prefix)
    else:
        raw_response = """
                         No sé qué hacer con la ruta 
                         <strong>%s</strong>
                       """ % request.path
    
    if request.accept == 'text/plain':
        response = raw_response
    else:
        response = base % {'content': raw_response}
    #respondemos
    start_response(
          "200 OK",
          [('Content-Type', request.accept),
           ('Content-Length', str(len(response)))]
          )

    return [response]

from wsgiref.simple_server import make_server

daemon = make_server('127.0.0.1', 8000, application)

daemon.serve_forever()
