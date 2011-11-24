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

def application(environ, start_response): 
    
    #interpretamos el environ
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    accept = environ['HTTP_ACCEPT'] if 'HTTP_ACCEPT' in environ else 'text/html'
    POST, GET = {}, {}
    if method == 'GET':
        GET  = parse_qs(environ['QUERY_STRING'])

    #reaccionamos a la ruta
    raw_response = ""
    if path == '/echo':
        raw_response = GET['with'][0] + '\n'
    elif re.match(r'/words/with/\w+', path):
        prefix = re.match(r'/words/with/(\w+)', path).group(1)
        limit = GET['limit'] if 'limit' in GET else 10
        raw_results = os.popen("look %s"%prefix).readlines()[:limit]
        raw_response =  ",\n".join([word.replace('\n','') for word in raw_results])
    else:
        raw_response = """
                         No sé qué hacer con la ruta 
                         <strong>%s</strong>
                       """ % path
    
    if accept == 'text/plain':
        response = raw_response
    else:
        response = base % {'content': raw_response}
    #respondemos
    start_response(
          "200 OK",
          [('Content-Type', accept),
           ('Content-Length', str(len(response)))]
          )

    return [response]

from wsgiref.simple_server import make_server

daemon = make_server('127.0.0.1', 8000, application)

daemon.serve_forever()
